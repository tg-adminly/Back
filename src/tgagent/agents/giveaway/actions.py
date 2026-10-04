"""Telegram'ga tegadigan egasi amallari. Bot menyusi ham, veb-panel ham shularni chaqiradi."""

from collections.abc import Awaitable, Callable
from datetime import datetime
from html import escape

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.agents.giveaway import keyboards as kb
from tgagent.agents.giveaway import service, texts
from tgagent.agents.giveaway.models import Giveaway, GiveawayStatus, Prize, PrizeType, SponsorChannel, Winner, WinnerStatus
from tgagent.channels.telegram_bot.chats import ChatRef, bot_is_admin, chat_link
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
                reply_markup=kb.giveaway_post(sponsors, g.id),
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
