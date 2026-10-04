"""Ishtirokchilar: kanal postidan qatnashish (popup), g'olibdan ma'lumot yig'ish."""

import asyncio
import logging
import re
import time

from aiogram import Bot, F, Router
from aiogram.enums import ChatType, ContentType
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.agents.giveaway import keyboards as kb
from tgagent.agents.giveaway import service, texts
from tgagent.agents.giveaway.jobs import required_chats
from tgagent.agents.giveaway.models import ClaimStep, Giveaway, GiveawayStatus, Winner, WinnerStatus
from tgagent.agents.giveaway.validators import normalize_card, normalize_phone
from tgagent.channels.telegram_bot.chats import ChatRef, missing_chats
from tgagent.channels.telegram_bot.notify import notify_users
from tgagent.config import Settings
from tgagent.core.crypto import Vault, mask_card
from tgagent.core.db import utcnow

CLAIM_LINK = re.compile(r"^w(\d+)$")
log = logging.getLogger(__name__)

# Foydalanuvchi yozishi mumkin bo'lgan xabarlar. Qolganlari (pin, taymer va h.k.) — xizmat xabarlari, javob bermaymiz
USER_CONTENT = {
    ContentType.TEXT, ContentType.CONTACT, ContentType.PHOTO, ContentType.DOCUMENT, ContentType.STICKER,
    ContentType.VOICE, ContentType.VIDEO, ContentType.VIDEO_NOTE, ContentType.ANIMATION, ContentType.AUDIO,
}


def build_router(settings: Settings) -> Router:
    router = Router(name="giveaway_participant")
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    counter = JoinCounter()
    throttle = ReplyThrottle()
    staff = set(settings.owner_ids) | set(settings.editor_ids)
    # Egasi/muharrir g'olib bo'lsa, ularning oddiy xabarlari karta deb o'qilmasin:
    # ma'lumot faqat «Yutuqni olish» orqali kirgandan keyin qabul qilinadi
    staff_claiming: set[int] = set()

    # --- Qatnashish: kanal postidagi tugma, popup javob (botga kirish shart emas) ---

    @router.callback_query(kb.JoinCB.filter())
    async def join(cb: CallbackQuery, callback_data: kb.JoinCB, bot: Bot, sm: async_sessionmaker, main_chat: ChatRef):
        gid = callback_data.giveaway_id
        text, created = await _try_join(bot, sm, main_chat, gid, cb.from_user)
        await cb.answer(text, show_alert=True)
        if created:
            counter.schedule(bot, sm, gid)

    # --- G'olib: natija postidagi «Yutuqni olish» → botga kiradi ---

    @router.message(CommandStart(deep_link=True))
    async def start_claim(message: Message, command: CommandObject, sm: async_sessionmaker):
        match = CLAIM_LINK.match(command.args or "")
        if not match:
            await message.answer(texts.DEFAULT_REPLY)
            return
        async with sm() as s:
            w = await s.scalar(
                select(Winner).where(Winner.giveaway_id == int(match.group(1)), Winner.user_id == message.from_user.id)
            )
            if w is None:
                await message.answer(texts.NOT_A_WINNER)
            elif w.status == WinnerStatus.AWAITING_INFO:
                staff_claiming.add(message.from_user.id)
                # Suhbat davom etayotgan bo'lsa ham savolni qaytadan beramiz — keyingi xabar joriy qadamga tushadi
                markup = kb.share_phone() if w.claim_step == ClaimStep.PHONE else None
                await message.answer(_claim_prompt(w), reply_markup=markup)
            else:
                await message.answer(texts.CLAIM_ALREADY_DONE)

    # --- G'olibdan ma'lumot yig'ish (holat DB da, restartdan keyin ham davom etadi) ---

    @router.message()
    async def claim_or_default(message: Message, bot: Bot, sm: async_sessionmaker, vault: Vault):
        uid = message.from_user.id
        # Matnning o'zi logga yozilmaydi (karta bo'lishi mumkin) — faqat turi
        log.info("Shaxsiy xabar: user=%s turi=%s", uid, message.content_type)
        if message.content_type not in USER_CONTENT:
            return

        async def hint(text: str, markup=None) -> None:
            # Xato/yo'riqnoma javoblari — bir foydalanuvchiga tez-tez takrorlanmaydi
            if throttle.allow(uid):
                await message.answer(text, reply_markup=markup)

        if uid in staff and uid not in staff_claiming:
            await hint(texts.STAFF_UNKNOWN)
            return
        async with sm() as s:
            w = await service.pending_claim(s, uid)
            if w is None:
                await hint(texts.DEFAULT_REPLY)
                return

            step = w.claim_step
            reply, markup = None, None
            text = (message.text or "").strip()

            if step == ClaimStep.CARD:
                card = normalize_card(text)
                if not card:
                    await hint(texts.BAD_CARD)
                    return
                w.card_enc, w.card_masked = vault.encrypt(card), mask_card(card)
                w.claim_step, reply = ClaimStep.CARD_HOLDER, texts.ASK_CARD_HOLDER
            elif step == ClaimStep.CARD_HOLDER:
                if not text:
                    await hint(texts.NEED_TEXT)
                    return
                w.card_holder_enc = vault.encrypt(text[:255])
                w.claim_step = None
            elif step == ClaimStep.FULL_NAME:
                if not text:
                    await hint(texts.NEED_TEXT)
                    return
                w.full_name_enc = vault.encrypt(text[:255])
                w.claim_step, reply, markup = ClaimStep.PHONE, texts.ASK_PHONE, kb.share_phone()
            elif step == ClaimStep.PHONE:
                raw = message.contact.phone_number if message.contact else text
                phone = normalize_phone(raw)
                if not phone:
                    await hint(texts.BAD_PHONE, kb.share_phone())
                    return
                w.phone_enc = vault.encrypt(phone)
                w.claim_step, reply, markup = ClaimStep.ADDRESS, texts.ASK_ADDRESS, ReplyKeyboardRemove()
            elif step == ClaimStep.ADDRESS:
                if not text:
                    await hint(texts.NEED_TEXT)
                    return
                w.address_enc = vault.encrypt(text[:1000])
                w.claim_step = None

            finished = w.claim_step is None
            if finished:
                w.status = WinnerStatus.INFO_RECEIVED
            await s.commit()

        throttle.reset(uid)
        if not finished:
            await message.answer(reply, reply_markup=markup)
            return
        staff_claiming.discard(uid)
        await message.answer(texts.CLAIM_DONE, reply_markup=ReplyKeyboardRemove())
        await notify_users(bot, settings.owner_ids, texts.payout_card(w, vault), reply_markup=kb.payout(w))

    return router


async def _try_join(bot: Bot, sm: async_sessionmaker, main_chat: ChatRef, giveaway_id: int, user: User):
    """(popup matni, yangi qo'shildimi) qaytaradi."""
    async with sm() as s:
        g = await s.get(Giveaway, giveaway_id)
        if g is None:
            return texts.GIVEAWAY_NOT_FOUND, False
        if g.status != GiveawayStatus.ACTIVE or g.ends_at <= utcnow():
            return texts.GIVEAWAY_CLOSED, False
        existing = await service.get_participant(s, g.id, user.id)
        if existing:
            return texts.already_joined(existing.number), False

    missing = await missing_chats(bot, required_chats(g, main_chat), user.id)
    if missing:
        return texts.not_subscribed([c.title for c in missing]), False

    async with sm() as s:
        p, created = await service.add_participant(s, g.id, user.id, user.full_name, user.username)
    return (texts.joined(p.number) if created else texts.already_joined(p.number)), created


def _claim_prompt(w: Winner) -> str:
    """Joriy qadam uchun savol (g'olib botga keyinroq kirganda)."""
    return {
        ClaimStep.CARD: texts.winner_congrats(w),
        ClaimStep.FULL_NAME: texts.winner_congrats(w),
        ClaimStep.CARD_HOLDER: texts.ASK_CARD_HOLDER,
        ClaimStep.PHONE: texts.ASK_PHONE,
        ClaimStep.ADDRESS: texts.ASK_ADDRESS,
    }[w.claim_step]


class ReplyThrottle:
    """Bir foydalanuvchiga xato javobini WINDOW soniyada ko'pi bilan bir marta yuboradi."""

    WINDOW = 30

    def __init__(self):
        self._last: dict[int, float] = {}

    def allow(self, user_id: int) -> bool:
        now = time.monotonic()
        if now - self._last.get(user_id, -self.WINDOW) < self.WINDOW:
            return False
        self._last[user_id] = now
        return True

    def reset(self, user_id: int) -> None:
        self._last.pop(user_id, None)


class JoinCounter:
    """Post tugmasidagi ishtirokchilar sonini yangilaydi.

    Har bosishda tahrirlasak Telegram limitiga tushamiz, shuning uchun bir necha soniyada bir marta.
    """

    DELAY = 5

    def __init__(self):
        self._pending: dict[int, asyncio.Task] = {}

    def schedule(self, bot: Bot, sm: async_sessionmaker, giveaway_id: int) -> None:
        if giveaway_id not in self._pending:
            self._pending[giveaway_id] = asyncio.create_task(self._run(bot, sm, giveaway_id))

    async def _run(self, bot: Bot, sm: async_sessionmaker, giveaway_id: int) -> None:
        try:
            await asyncio.sleep(self.DELAY)
            del self._pending[giveaway_id]  # shu paytdan keyingi qo'shilishlar yangi yangilanishni rejalaydi
            async with sm() as s:
                g = await s.get(Giveaway, giveaway_id)
                count = await service.participants_count(s, giveaway_id)
            if g is None or g.status != GiveawayStatus.ACTIVE or not g.message_id:
                return
            sponsors = [ChatRef(sp.chat_id, sp.title, sp.link) for sp in g.sponsors]
            await bot.edit_message_reply_markup(
                chat_id=g.chat_id, message_id=g.message_id, reply_markup=kb.giveaway_post(sponsors, g.id, count)
            )
        except TelegramRetryAfter as e:
            log.info("Hisoblagich: RetryAfter %ss", e.retry_after)
            await asyncio.sleep(e.retry_after)
            self.schedule(bot, sm, giveaway_id)
        except TelegramBadRequest:
            pass  # "message is not modified" va h.k.
        except Exception:
            log.exception("Hisoblagichni yangilab bo'lmadi")
        finally:
            if self._pending.get(giveaway_id) is asyncio.current_task():
                del self._pending[giveaway_id]
