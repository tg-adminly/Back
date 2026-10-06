"""Fon vazifa: avtomatik rejimda vaqti kelganda qatnashishni yopish, obunani qayta tekshirish va g'olibni aniqlash.

Jonli rejimda vaqt — faqat eslatma: qatnashish ochiq qoladi, egasi yoki muharrir o'yinni istalgan paytda
boshlaydi (close_now → actions.reveal_next).
"""

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass
from html import escape

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ReplyParameters
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.agents.giveaway import draw, service, texts
from tgagent.agents.giveaway.models import Giveaway, GiveawayStatus, Participant
from tgagent.channels.telegram_bot.chats import ChatRef, bot_is_admin, missing_chats
from tgagent.channels.telegram_bot.notify import notify_users
from tgagent.config import Settings
from tgagent.core.db import utcnow

log = logging.getLogger(__name__)

POLL_SECONDS = 30
CHECK_CONCURRENCY = 8

# Jonli o'yin amallari (tekshiruv, keyingi g'olib, e'lon) bir rozigrishda bir vaqtda bitta bajariladi
draw_locks: defaultdict[int, asyncio.Lock] = defaultdict(asyncio.Lock)


@dataclass
class CheckProgress:
    total: int
    done: int = 0


# Hozir ketayotgan obuna tekshiruvlari (giveaway_id -> progress)
checks: dict[int, CheckProgress] = {}
# Oxirgi tekshiruv xato bilan tugagan bo'lsa — sababi (panelda ko'rsatiladi)
check_errors: dict[int, str] = {}


class CheckError(Exception):
    """Tekshiruvni boshlab bo'lmadi (Telegram HTML matni)."""


def required_chats(g: Giveaway, main_chat: ChatRef) -> list[ChatRef]:
    """Asosiy kanal + homiylar (takrorlarsiz)."""
    chats = [main_chat]
    chats += [ChatRef(s.chat_id, s.title, s.link) for s in g.sponsors if s.chat_id != main_chat.id]
    return chats


def staff_ids(settings: Settings) -> list[int]:
    """Egasi + muharrirlar (takrorlarsiz) — jonli o'yinni ular o'tkazadi."""
    return list(dict.fromkeys([*settings.owner_ids, *settings.editor_ids]))


def live_url(settings: Settings, giveaway_id: int) -> str:
    return f"{settings.panel_url.rstrip('/')}/giveaways/{giveaway_id}/live"


async def draw_loop(bot: Bot, sm: async_sessionmaker, settings: Settings, main_chat: ChatRef):
    while True:
        try:
            async with sm() as s:
                due = await service.due_giveaway_ids(s)
                reminders = await service.due_reminder_ids(s)
            for gid in due:
                await close_participation(bot, sm, settings, main_chat, gid)
            for gid in reminders:
                await remind(bot, sm, settings, gid)
        except Exception:
            log.exception("draw_loop xatosi")
        await asyncio.sleep(POLL_SECONDS)


async def remind(bot: Bot, sm: async_sessionmaker, settings: Settings, giveaway_id: int):
    """Jonli rejim: vaqt keldi — egasi va muharrirga eslatma. Qatnashish ochiq qoladi."""
    async with sm() as s:
        g = await s.get(Giveaway, giveaway_id)
        if g is None or g.status != GiveawayStatus.ACTIVE or g.auto_draw or g.reminded_at:
            return
        g.reminded_at = utcnow()
        await s.commit()
        count = await service.participants_count(s, g.id)
    await notify_users(bot, staff_ids(settings), texts.live_reminder(g, count, live_url(settings, g.id)))


async def freeze(sm: async_sessionmaker, giveaway_id: int) -> tuple[Giveaway, list[Participant]] | None:
    """Qatnashishni yopadi va ro'yxatni qotiradi. Ishtirokchi bo'lmasa — darhol FINISHED."""
    async with sm() as s:
        g = await s.get(Giveaway, giveaway_id)
        if g is None or g.status != GiveawayStatus.ACTIVE:
            return None
        parts = await service.list_participants(s, g.id)
        g.list_hash = draw.participants_hash((p.number, p.user_id) for p in parts)
        g.status = GiveawayStatus.DRAWING if parts else GiveawayStatus.FINISHED
        await s.commit()
    log.info("Rozigrish #%s: qatnashish yopildi, %s ishtirokchi", giveaway_id, len(parts))
    return g, parts


async def close_participation(bot: Bot, sm: async_sessionmaker, settings: Settings, main_chat: ChatRef, giveaway_id: int):
    """Qatnashishni yopadi va oxirigacha olib boradi (fonda yoki botdagi «Hozir yakunlash»)."""
    frozen = await freeze(sm, giveaway_id)
    if frozen:
        await _after_close(bot, sm, settings, main_chat, *frozen, notify=True)


_close_tasks: set[asyncio.Task] = set()


async def close_now(bot: Bot, sm: async_sessionmaker, settings: Settings, main_chat: ChatRef, giveaway_id: int, *, notify: bool) -> bool:
    """Qatnashishni shu zahoti yopadi; obuna tekshiruvi (va avtomatik rejimda aniqlash) fonda davom etadi.

    Qaytgan paytda tekshiruv allaqachon `checks` da — jonli sahifa jarayonni darhol ko'radi.
    """
    frozen = await freeze(sm, giveaway_id)
    if frozen is None:
        return False
    task = asyncio.create_task(_after_close(bot, sm, settings, main_chat, *frozen, notify=notify))
    _close_tasks.add(task)
    task.add_done_callback(_close_tasks.discard)
    await asyncio.sleep(0)  # check_subscriptions birinchi await'gacha yuradi va `checks` ni to'ldiradi
    return True


async def _after_close(
    bot: Bot,
    sm: async_sessionmaker,
    settings: Settings,
    main_chat: ChatRef,
    g: Giveaway,
    parts: list[Participant],
    *,
    notify: bool,
):
    """Obunani qayta tekshiradi; avtomatik rejimda g'olibni aniqlab e'lon qiladi, jonli rejimda — xabar beradi."""
    if not parts:
        reply = ReplyParameters(message_id=g.message_id, allow_sending_without_reply=True) if g.message_id else None
        try:
            await bot.send_message(g.chat_id, texts.NO_PARTICIPANTS.format(title=escape(g.title)), reply_parameters=reply)
        except TelegramAPIError:
            log.exception("Rozigrish #%s: natijani yuborib bo'lmadi", g.id)
        return
    try:
        excluded = await check_subscriptions(bot, sm, main_chat, g.id)
    except Exception:
        log.exception("Rozigrish #%s: obunani tekshirib bo'lmadi", g.id)
        excluded = None
    url = live_url(settings, g.id)
    if g.auto_draw:
        # actions jobs'ni import qiladi — aylanma importdan qochish uchun shu yerda
        from tgagent.agents.giveaway.actions import run_auto_draw

        try:
            await run_auto_draw(bot, settings, sm, main_chat, g.id)
        except Exception as e:
            log.exception("Rozigrish #%s: avtomatik aniqlab bo'lmadi", g.id)
            error = getattr(e, "message", None) or escape(str(e))
            await notify_users(bot, staff_ids(settings), texts.auto_draw_failed(g, error, url))
        return
    if notify:
        await notify_users(bot, staff_ids(settings), texts.live_ready(g, len(parts), excluded, url))


async def check_subscriptions(bot: Bot, sm: async_sessionmaker, main_chat: ChatRef, giveaway_id: int) -> int:
    """Jonli o'yindan oldin hamma ishtirokchining obunasini qayta tekshiradi.

    Chiqib ketganlar SubscriptionMiss ga yoziladi (qaysi kanal) va randomga tushmaydi;
    qayta obuna bo'lganlar ro'yxatdan chiqadi. O'yin boshlangach (birinchi pick) ishlamaydi.
    Chiqib ketganlar sonini qaytaradi.
    """
    if giveaway_id in checks:
        raise CheckError(texts.CHECK_RUNNING)
    # Darhol belgilanadi (await'dan oldin) — panel jarayonni shu zahoti ko'radi, ikkinchi tekshiruv boshlanmaydi
    progress = checks[giveaway_id] = CheckProgress(total=0)
    check_errors.pop(giveaway_id, None)
    try:
        async with draw_locks[giveaway_id]:
            async with sm() as s:
                g = await s.get(Giveaway, giveaway_id)
                if g is None or g.status != GiveawayStatus.DRAWING:
                    raise CheckError(texts.NOT_DRAWING)
                if await service.list_picks(s, giveaway_id):
                    raise CheckError(texts.CHECK_TOO_LATE)
                parts = await service.list_participants(s, giveaway_id)
                chats = required_chats(g, main_chat)
            progress.total = len(parts)
            # Bot admin bo'lmasa hamma "obunasiz" chiqadi — bunday natijani yozmaymiz
            for c in chats:
                if not await bot_is_admin(bot, c.id):
                    raise CheckError(texts.BOT_NOT_ADMIN_IN.format(title=escape(c.title)))

            sem = asyncio.Semaphore(CHECK_CONCURRENCY)
            misses: dict[int, list[str]] = {}

            async def check(p):
                async with sem:
                    missing = await missing_chats(bot, chats, p.user_id)
                if missing:
                    misses[p.id] = [c.title for c in missing]
                progress.done += 1

            await asyncio.gather(*(check(p) for p in parts))
            async with sm() as s:
                await service.save_misses(s, giveaway_id, misses)
                await s.commit()
    except CheckError as e:
        check_errors[giveaway_id] = e.args[0]
        raise
    except Exception:
        check_errors[giveaway_id] = texts.CHECK_FAILED
        raise
    finally:
        del checks[giveaway_id]
    log.info("Rozigrish #%s: obuna tekshirildi, %s/%s chiqib ketgan", giveaway_id, len(misses), len(parts))
    return len(misses)
