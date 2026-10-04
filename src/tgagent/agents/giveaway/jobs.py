"""Fon vazifa: vaqti kelgan rozigrishlarni yakunlash va g'oliblarni aniqlash."""

import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BufferedInputFile, ReplyParameters
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.agents.giveaway import draw, keyboards, service, texts
from tgagent.agents.giveaway.models import Giveaway, GiveawayStatus, Winner
from tgagent.channels.telegram_bot.chats import ChatRef, is_member
from tgagent.channels.telegram_bot.notify import notify_users
from tgagent.config import Settings

log = logging.getLogger(__name__)

POLL_SECONDS = 30


def required_chats(g: Giveaway, main_chat: ChatRef) -> list[ChatRef]:
    """Asosiy kanal + homiylar (takrorlarsiz)."""
    chats = [main_chat]
    chats += [ChatRef(s.chat_id, s.title, s.link) for s in g.sponsors if s.chat_id != main_chat.id]
    return chats


async def draw_loop(bot: Bot, sm: async_sessionmaker, settings: Settings, main_chat: ChatRef):
    while True:
        try:
            async with sm() as s:
                ids = await service.due_giveaway_ids(s)
            for gid in ids:
                await finalize(bot, sm, settings, main_chat, gid)
        except Exception:
            log.exception("draw_loop xatosi")
        await asyncio.sleep(POLL_SECONDS)


async def finalize(bot: Bot, sm: async_sessionmaker, settings: Settings, main_chat: ChatRef, giveaway_id: int):
    # 1) Ro'yxatni qotirish va hash hisoblash (qisqa tranzaksiya)
    async with sm() as s:
        g = await s.get(Giveaway, giveaway_id)
        if g is None or g.status not in (GiveawayStatus.ACTIVE, GiveawayStatus.DRAWING):
            return
        if g.status == GiveawayStatus.DRAWING:
            # Oldingi urinish g'oliblarni yozib bo'lgan bo'lsa — faqat yopamiz
            if await s.scalar(select(Winner.id).where(Winner.giveaway_id == g.id).limit(1)):
                g.status = GiveawayStatus.FINISHED
                await s.commit()
                return
        parts = await service.list_participants(s, g.id)
        entries = [(p.number, p.user_id) for p in parts]
        g.list_hash = draw.participants_hash(entries)
        g.status = GiveawayStatus.DRAWING
        await s.commit()
        chats = required_chats(g, main_chat)

    log.info("Rozigrish #%s: %s ishtirokchi, g'olib aniqlanmoqda", giveaway_id, len(parts))

    # 2) Tartib bo'yicha yurib, obunasi saqlanganlarni olamiz (tarmoq so'rovlari — sessiyasiz)
    by_number = {p.number: p for p in parts}
    chosen, skipped = [], []
    for number in draw.rank(g.seed, g.list_hash, by_number):
        if len(chosen) >= g.winners_count:
            break
        p = by_number[number]
        ok = True
        for c in chats:
            if not await is_member(bot, c.id, p.user_id):
                ok = False
                break
        (chosen if ok else skipped).append(p)

    # 3) G'oliblarni yozish
    async with sm() as s:
        g = await s.get(Giveaway, giveaway_id)
        winners = []
        for place, (p, prize) in enumerate(zip(chosen, g.prizes), 1):
            w = Winner(
                giveaway=g,  # sessiya yopilgach ham winner_congrats() uchun kerak
                participant_id=p.id,
                user_id=p.user_id,
                place=place,
                prize_type=prize.type,
                prize_amount=prize.amount,
                prize_name=prize.name,
                claim_step=service.first_claim_step(prize.type),
            )
            s.add(w)
            winners.append(w)
        g.status = GiveawayStatus.FINISHED
        await s.commit()

    # 4) E'lon, g'oliblarga xabar, egasiga hisobot
    await _announce(bot, g, parts, chosen, skipped, entries)
    for w, p in zip(winners, chosen):
        try:
            await bot.send_message(p.user_id, texts.winner_congrats(w))
        except TelegramAPIError:
            await notify_users(
                bot, settings.owner_ids, texts.WINNER_DM_FAILED.format(link=texts.user_link(p.user_id, p.full_name))
            )
    await notify_users(bot, settings.owner_ids, texts.draw_summary(g, len(parts), len(chosen)))


async def _announce(bot: Bot, g: Giveaway, parts, chosen, skipped, entries):
    if not parts:
        await bot.send_message(g.chat_id, texts.NO_PARTICIPANTS.format(title=g.title))
        return
    text = texts.results_post(
        g,
        total=len(parts),
        winners=[(i, p.user_id, p.full_name, p.number) for i, p in enumerate(chosen, 1)],
        skipped=[p.number for p in skipped],
    )
    reply = ReplyParameters(message_id=g.message_id, allow_sending_without_reply=True) if g.message_id else None
    markup = None
    if chosen:
        me = await bot.me()
        markup = keyboards.claim(f"https://t.me/{me.username}?start=w{g.id}")
    await bot.send_message(g.chat_id, text, reply_parameters=reply, reply_markup=markup)
    await bot.send_document(
        g.chat_id,
        BufferedInputFile(draw.participants_file(entries), filename=f"rozigrish_{g.id}_ishtirokchilar.txt"),
        caption="Ishtirokchilar ro'yxati (raqam:user_id). sha256(fayl) = ro'yxat hash.",
    )
