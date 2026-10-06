"""Telegram'ga tegadigan egasi amallari. Bot menyusi ham, veb-panel ham shularni chaqiradi."""

from collections.abc import Awaitable, Callable
from datetime import datetime
from html import escape

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ReplyParameters
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.agents.giveaway import keyboards as kb
from tgagent.agents.giveaway import service, texts
from tgagent.agents.giveaway import jobs
from tgagent.agents.giveaway.jobs import required_chats
from tgagent.agents.giveaway.models import (
    DrawPick,
    Giveaway,
    GiveawayStatus,
    Participant,
    Prize,
    PrizeType,
    SponsorChannel,
    SubscriptionMiss,
    Winner,
    WinnerStatus,
)
from tgagent.channels.telegram_bot.chats import ChatRef, bot_is_admin, chat_link, missing_chats
from tgagent.channels.telegram_bot.notify import notify_users
from tgagent.config import Settings


class ActionError(Exception):
    """Egasiga ko'rsatiladigan xato (Telegram HTML matni)."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


async def add_sponsor(
    bot: Bot, settings: Settings, sm: async_sessionmaker, ref: int | str, explicit_link: str | None = None
) -> SponsorChannel:
    """Kanalni tekshiradi (bot admin, link bor) va homiylar ro'yxatiga yozadi."""
    try:
        chat = await bot.get_chat(ref)
    except TelegramAPIError:
        raise ActionError(texts.SPONSOR_NOT_FOUND) from None
    if chat.id == settings.main_chat_id:
        raise ActionError(texts.SPONSOR_IS_MAIN)
    title = chat.title or str(chat.id)
    if not await bot_is_admin(bot, chat.id):
        raise ActionError(texts.SPONSOR_NOT_ADMIN.format(title=escape(title)))
    link = explicit_link or await chat_link(bot, chat)
    if not link:
        raise ActionError(texts.SPONSOR_NO_LINK.format(chat_id=chat.id))
    async with sm() as s:
        return await service.upsert_sponsor(s, chat.id, title, link)


async def publish_giveaway(
    bot: Bot,
    settings: Settings,
    sm: async_sessionmaker,
    *,
    title: str,
    description: str,
    prizes: list[Prize],
    ends_at: datetime,
    sponsor_ids: list[int],
) -> Giveaway:
    """Rozigrishni bazaga yozadi va asosiy kanalga post chiqaradi."""
    async with sm() as s:
        g = await service.create_giveaway(
            s,
            title=title,
            description=description,
            prizes=prizes,
            ends_at=ends_at,
            chat_id=settings.main_chat_id,
            sponsor_ids=sponsor_ids,
        )
        sponsors = [ChatRef(sp.chat_id, sp.title, sp.link) for sp in g.sponsors]
        try:
            post = await bot.send_message(
                g.chat_id,
                texts.giveaway_post(g, settings.tz, [sp.title for sp in sponsors]),
                reply_markup=kb.giveaway_post(sponsors, g.id, list_url=kb.participants_url(settings.panel_url, g.id)),
            )
        except TelegramAPIError as e:
            g.status = GiveawayStatus.CANCELLED
            await s.commit()
            raise ActionError(texts.PUBLISH_FAILED.format(error=escape(str(e)))) from None
        g.message_id = post.message_id
        await s.commit()
    return g


async def deliver_prize(bot: Bot, sm: async_sessionmaker, winner_id: int, send_proof: Callable[[int], Awaitable]) -> bool:
    """Yutuqni topshirilgan deb yopadi va g'olibga chek + tabrik yuboradi.

    `send_proof(chat_id)` chekni yuboradi (bot: xabar nusxasi, panel: yuklangan fayl).
    g'olibga yetib bordimi — shuni qaytaradi; holat baribir yopiladi.
    """
    async with sm() as s:
        w = await s.get(Winner, winner_id)
        if w is None or w.status != WinnerStatus.INFO_RECEIVED:
            raise ActionError(texts.NOT_ACTIVE)
        caption = texts.PRIZE_SENT_MONEY if w.prize_type == PrizeType.MONEY else texts.PRIZE_SENT_ITEM
        service.mark_done(w)
        await s.commit()
    try:
        await send_proof(w.user_id)
        await bot.send_message(w.user_id, caption)
    except TelegramAPIError:
        return False
    return True


# --- Jonli o'yin ---


async def reveal_next(bot: Bot, sm: async_sessionmaker, main_chat: ChatRef, giveaway_id: int) -> list[DrawPick]:
    """Navbatdagi g'olibni chiqaradi (draw.rank tartibida).

    Obunadan chiqib ketganlar ham yoziladi (place=None, qaysi kanal — SubscriptionMiss) va o'tkaziladi —
    ekranda shu ham ko'rsatiladi. Oxirgi element — g'olib (agar nomzod qolgan bo'lsa).
    """
    if giveaway_id in jobs.checks:
        raise ActionError(texts.CHECK_RUNNING)
    async with jobs.draw_locks[giveaway_id]:
        async with sm() as s:
            g = await s.get(Giveaway, giveaway_id)
            if g is None or g.status != GiveawayStatus.DRAWING:
                raise ActionError(texts.NOT_DRAWING)
            chats = required_chats(g, main_chat)
        # Bot biror kanalda admin bo'lmasa, hamma "obunasiz" chiqib qoladi — efirda bunday xato bo'lmasin
        for c in chats:
            if not await bot_is_admin(bot, c.id):
                raise ActionError(texts.BOT_NOT_ADMIN_IN.format(title=escape(c.title)))

        new: list[DrawPick] = []
        while True:
            async with sm() as s:
                picks = await service.list_picks(s, giveaway_id)
                place = sum(p.place is not None for p in picks) + 1
                if place > g.winners_count:
                    if new:
                        break
                    raise ActionError(texts.ALL_PLACES_FILLED)
                cand = await service.next_candidate(s, g, picks)
            if cand is None:
                if new:
                    break
                raise ActionError(texts.NO_MORE_CANDIDATES)

            missing = await missing_chats(bot, chats, cand.user_id)
            ok = not missing
            async with sm() as s:
                pick = DrawPick(giveaway_id=giveaway_id, participant_id=cand.id, place=place if ok else None)
                s.add(pick)
                if missing:
                    s.add(SubscriptionMiss(participant_id=cand.id, giveaway_id=giveaway_id, chats=[c.title for c in missing]))
                await s.commit()
                await s.refresh(pick, ["participant"])
            new.append(pick)
            if ok:
                break
        return new


async def announce_results(bot: Bot, settings: Settings, sm: async_sessionmaker, giveaway_id: int) -> None:
    """Jonli o'yinda chiqqan g'oliblarni kanalga e'lon qiladi, Winner yozuvlarini yaratadi va g'oliblarga yozadi."""
    async with jobs.draw_locks[giveaway_id]:
        async with sm() as s:
            g = await s.get(Giveaway, giveaway_id)
            if g is None or g.status != GiveawayStatus.DRAWING:
                raise ActionError(texts.NOT_DRAWING)
            picks = await service.list_picks(s, giveaway_id)
            won = [p for p in picks if p.place is not None]
            if len(won) < g.winners_count and await service.next_candidate(s, g, picks) is not None:
                raise ActionError(texts.DRAW_NOT_DONE)
            total = await service.participants_count(s, giveaway_id)

        # Avval post: chiqmasa, holat o'zgarmaydi va qayta urinish mumkin
        text = texts.results_post(
            g,
            total=total,
            winners=[(p.place, p.participant.user_id, p.participant.full_name, p.participant.number) for p in won],
            skipped=[p.participant.number for p in picks if p.place is None],
        )
        reply = ReplyParameters(message_id=g.message_id, allow_sending_without_reply=True) if g.message_id else None
        markup = None
        if won:
            me = await bot.me()
            markup = kb.claim(f"https://t.me/{me.username}?start=w{g.id}", kb.participants_url(settings.panel_url, g.id))
        try:
            await bot.send_message(g.chat_id, text, reply_parameters=reply, reply_markup=markup)
        except TelegramAPIError as e:
            raise ActionError(texts.ANNOUNCE_FAILED.format(error=escape(str(e)))) from None

        async with sm() as s:
            g = await s.get(Giveaway, giveaway_id)
            winners: list[tuple[Winner, Participant]] = []
            for p, prize in zip(won, g.prizes):
                w = Winner(
                    giveaway=g,  # sessiya yopilgach ham winner_congrats() uchun kerak
                    participant_id=p.participant_id,
                    user_id=p.participant.user_id,
                    place=p.place,
                    prize_type=prize.type,
                    prize_amount=prize.amount,
                    prize_name=prize.name,
                    claim_step=service.first_claim_step(prize.type),
                )
                s.add(w)
                winners.append((w, p.participant))
            g.status = GiveawayStatus.FINISHED
            await s.commit()

    for w, p in winners:
        try:
            await bot.send_message(p.user_id, texts.winner_congrats(w))
        except TelegramAPIError:
            await notify_users(
                bot, settings.owner_ids, texts.WINNER_DM_FAILED.format(link=texts.user_link(p.user_id, p.full_name))
            )
    await notify_users(bot, settings.owner_ids, texts.draw_summary(g, total, len(winners)))
