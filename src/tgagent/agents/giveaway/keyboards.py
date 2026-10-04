from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgagent.agents.giveaway import texts
from tgagent.agents.giveaway.models import Prize, PrizeType, Winner, WinnerStatus
from tgagent.channels.telegram_bot.chats import ChatRef


class WizardCB(CallbackData, prefix="wiz"):
    action: str  # same_prize | sponsors_done | publish | cancel


class ManageCB(CallbackData, prefix="gm"):
    action: str  # finish | cancel
    giveaway_id: int
    confirmed: bool = False


class JoinCB(CallbackData, prefix="join"):
    giveaway_id: int


class PaidCB(CallbackData, prefix="paid"):
    winner_id: int


def owner_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_NEW)],
            [KeyboardButton(text=texts.BTN_LIST), KeyboardButton(text=texts.BTN_PAYOUTS)],
        ],
        resize_keyboard=True,
    )


def same_prize(prize: Prize) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=texts.btn_same_for_rest(prize), callback_data=WizardCB(action="same_prize"))
    return b.as_markup()


def sponsors_done() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=texts.BTN_DONE, callback_data=WizardCB(action="sponsors_done"))
    return b.as_markup()


def publish_confirm() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=texts.BTN_PUBLISH, callback_data=WizardCB(action="publish"))
    b.button(text=texts.BTN_CANCEL, callback_data=WizardCB(action="cancel"))
    b.adjust(1)
    return b.as_markup()


def giveaway_post(sponsors: list[ChatRef], giveaway_id: int, count: int = 0) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for s in sponsors:
        b.button(text=f"➕ {s.title}", url=s.link)
    b.button(text=texts.join_button(count), callback_data=JoinCB(giveaway_id=giveaway_id))
    b.adjust(1)
    return b.as_markup()


def claim(url: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=texts.BTN_CLAIM, url=url)
    return b.as_markup()


def manage(giveaway_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=texts.BTN_FINISH_NOW, callback_data=ManageCB(action="finish", giveaway_id=giveaway_id))
    b.button(text=texts.BTN_CANCEL_GIVEAWAY, callback_data=ManageCB(action="cancel", giveaway_id=giveaway_id))
    b.adjust(2)
    return b.as_markup()


def manage_confirm(action: str, giveaway_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=texts.BTN_YES, callback_data=ManageCB(action=action, giveaway_id=giveaway_id, confirmed=True))
    return b.as_markup()


def share_phone() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=texts.BTN_SHARE_PHONE, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def payout(w: Winner) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if w.status == WinnerStatus.INFO_RECEIVED:
        label = texts.BTN_PAID if w.prize_type == PrizeType.MONEY else texts.BTN_SENT
        b.button(text=label, callback_data=PaidCB(winner_id=w.id))
    return b.as_markup()
