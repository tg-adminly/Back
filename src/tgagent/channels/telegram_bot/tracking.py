"""Bot qaysi kanallarda admin ekanini eslab qoladi (panelda yopiq kanalni tanlash uchun)."""

from aiogram import Router
from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.types import ChatMemberUpdated
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgagent.channels.telegram_bot.models import BotChat

_ADMIN = {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}


async def remember_chat(session: AsyncSession, chat_id: int, title: str, username: str | None) -> None:
    row = await session.scalar(select(BotChat).where(BotChat.chat_id == chat_id))
    if row is None:
        session.add(BotChat(chat_id=chat_id, title=title, username=username))
    else:
        row.title, row.username = title, username
    await session.commit()


async def forget_chat(session: AsyncSession, chat_id: int) -> None:
    await session.execute(delete(BotChat).where(BotChat.chat_id == chat_id))
    await session.commit()


async def list_chats(session: AsyncSession) -> list[BotChat]:
    return list((await session.scalars(select(BotChat).order_by(BotChat.title))).all())


def build_router() -> Router:
    router = Router(name="bot_chats")

    @router.my_chat_member()
    async def on_my_status(event: ChatMemberUpdated, sm: async_sessionmaker):
        chat = event.chat
        if chat.type not in {ChatType.CHANNEL, ChatType.SUPERGROUP}:
            return
        async with sm() as s:
            if event.new_chat_member.status in _ADMIN:
                await remember_chat(s, chat.id, chat.title or str(chat.id), chat.username)
            else:
                await forget_chat(s, chat.id)

    return router
