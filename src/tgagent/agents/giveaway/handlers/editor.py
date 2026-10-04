"""Kontent muharriri (Editor). 2-bosqichda: post qoralamalari, uslub qo'llanma, jadval."""

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgagent.agents.giveaway import texts
from tgagent.config import Settings


def build_router(settings: Settings) -> Router:
    router = Router(name="giveaway_editor")
    router.message.filter(F.chat.type == ChatType.PRIVATE, F.from_user.id.in_(set(settings.editor_ids) - set(settings.owner_ids)))

    @router.message(CommandStart(magic=F.args.is_(None)))
    async def start(message: Message):
        await message.answer(texts.EDITOR_WELCOME)

    return router
