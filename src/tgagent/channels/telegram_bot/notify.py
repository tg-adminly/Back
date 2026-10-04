import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import InlineKeyboardMarkup

log = logging.getLogger(__name__)


async def notify_users(bot: Bot, user_ids: list[int], text: str, reply_markup: InlineKeyboardMarkup | None = None):
    for uid in user_ids:
        try:
            await bot.send_message(uid, text, reply_markup=reply_markup)
        except TelegramAPIError as e:
            log.warning("Xabar yuborilmadi %s: %s", uid, e)
