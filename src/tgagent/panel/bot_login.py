"""Botdagi qism: saytdagi «Kirish» havolasi → egasi botda tasdiqlaydi."""

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandObject, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from tgagent.config import Settings
from tgagent.panel import texts
from tgagent.panel.auth import LoginRequests

LOGIN_PREFIX = "login_"


class LoginCB(CallbackData, prefix="plogin"):
    token: str


def build_router(settings: Settings, logins: LoginRequests) -> Router:
    router = Router(name="panel_login")
    staff = set(settings.owner_ids) | set(settings.editor_ids)
    router.message.filter(F.chat.type == ChatType.PRIVATE, F.from_user.id.in_(staff))
    router.callback_query.filter(F.from_user.id.in_(staff))

    @router.message(CommandStart(deep_link=True, magic=F.args.startswith(LOGIN_PREFIX)))
    async def login_link(message: Message, command: CommandObject):
        token = command.args.removeprefix(LOGIN_PREFIX)
        if logins.get(token) is None:
            await message.answer(texts.LOGIN_EXPIRED)
            return
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=texts.BTN_LOGIN_CONFIRM, callback_data=LoginCB(token=token).pack())]]
        )
        await message.answer(texts.LOGIN_ASK, reply_markup=markup)

    @router.callback_query(LoginCB.filter())
    async def login_confirm(cb: CallbackQuery, callback_data: LoginCB):
        ok = logins.confirm(callback_data.token, cb.from_user.id, cb.from_user.full_name)
        await cb.message.edit_text(texts.LOGIN_DONE if ok else texts.LOGIN_EXPIRED)
        await cb.answer()

    return router
