import asyncio
import logging
from dataclasses import dataclass

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramRetryAfter
from aiogram.types import ChatFullInfo

log = logging.getLogger(__name__)

_MEMBER = {ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}


@dataclass(frozen=True)
class ChatRef:
    id: int
    title: str
    link: str


async def _get_member(bot: Bot, chat_id: int, user_id: int):
    for _ in range(5):
        try:
            return await bot.get_chat_member(chat_id, user_id)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
    raise RuntimeError("get_chat_member: juda ko'p RetryAfter")


async def is_member(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await _get_member(bot, chat_id, user_id)
    except TelegramBadRequest as e:
        # Bot o'sha chatda admin bo'lmasa ham shu xato keladi
        log.warning("get_chat_member(%s, %s) xato: %s", chat_id, user_id, e)
        return False
    if member.status in _MEMBER:
        return True
    if member.status == ChatMemberStatus.RESTRICTED:
        return bool(getattr(member, "is_member", False))
    return False


async def missing_chats(bot: Bot, chats: list[ChatRef], user_id: int) -> list[ChatRef]:
    return [c for c in chats if not await is_member(bot, c.id, user_id)]


async def bot_is_admin(bot: Bot, chat_id: int) -> bool:
    try:
        me = await bot.me()
        member = await bot.get_chat_member(chat_id, me.id)
    except TelegramAPIError:
        return False
    return member.status in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}


async def chat_link(bot: Bot, chat: ChatFullInfo) -> str | None:
    if chat.username:
        return f"https://t.me/{chat.username}"
    if chat.invite_link:
        return chat.invite_link
    try:
        return await bot.export_chat_invite_link(chat.id)
    except TelegramAPIError:
        return None
