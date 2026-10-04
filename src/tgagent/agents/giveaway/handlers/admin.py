"""Egasi (Owner) uchun boshqaruv: rozigrish yaratish, boshqarish, to'lovlar."""

from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, MessageOriginChannel
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.agents.giveaway import keyboards as kb
from tgagent.agents.giveaway import actions, service, texts
from tgagent.agents.giveaway.models import Giveaway
from tgagent.agents.giveaway.validators import parse_local_datetime, parse_prize
from tgagent.config import Settings
from tgagent.core.crypto import Vault
from tgagent.core.db import utcnow


class CreateGiveaway(StatesGroup):
    title = State()
    description = State()
    winners = State()
    prizes = State()
    ends_at = State()
    sponsors = State()
    confirm = State()


class Payout(StatesGroup):
    proof = State()


def build_router(settings: Settings) -> Router:
    router = Router(name="giveaway_admin")
    owners = set(settings.owner_ids)
    router.message.filter(F.chat.type == ChatType.PRIVATE, F.from_user.id.in_(owners))
    router.callback_query.filter(F.from_user.id.in_(owners))

    # --- Umumiy ---

    @router.message(Command("bekor"))
    async def cancel(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(texts.CANCELLED, reply_markup=kb.owner_menu())

    @router.message(CommandStart(magic=F.args.is_(None)))
    @router.message(Command("menu"))
    async def menu(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(texts.OWNER_WELCOME, reply_markup=kb.owner_menu())

    # --- Rozigrish yaratish ---

    @router.message(StateFilter(None), F.text == texts.BTN_NEW)
    async def new_giveaway(message: Message, state: FSMContext):
        await state.set_state(CreateGiveaway.title)
        await message.answer(texts.ASK_TITLE)

    @router.message(CreateGiveaway.title, F.text)
    async def got_title(message: Message, state: FSMContext):
        await state.update_data(title=message.text.strip()[:255])
        await state.set_state(CreateGiveaway.description)
        await message.answer(texts.ASK_DESCRIPTION)

    @router.message(CreateGiveaway.description, F.text)
    async def got_description(message: Message, state: FSMContext):
        await state.update_data(description=message.text.strip())
        await state.set_state(CreateGiveaway.winners)
        await message.answer(texts.ASK_WINNERS)

    @router.message(CreateGiveaway.winners, F.text)
    async def got_winners(message: Message, state: FSMContext):
        text = message.text.strip()
        if not text.isdigit() or not 1 <= int(text) <= 100:
            await message.answer(texts.BAD_WINNERS)
            return
        await state.update_data(winners=int(text), prizes=[], prize_msg_id=None)
        await state.set_state(CreateGiveaway.prizes)
        await message.answer(texts.ask_place_prize(1, int(text)))

    # Har bir o'rin sovrini alohida; «Qolganlariga ham» tugmasi qolgan o'rinlarni oxirgi sovrin bilan to'ldiradi
    @router.message(CreateGiveaway.prizes, F.text)
    async def got_prize(message: Message, state: FSMContext, bot: Bot):
        prize = parse_prize(message.text)
        if prize is None:
            await message.answer(texts.BAD_PRIZE)
            return
        data = await state.get_data()
        if data["prize_msg_id"]:
            try:
                await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=data["prize_msg_id"])
            except TelegramAPIError:
                pass
        prizes = data["prizes"] + [prize.to_dict()]
        await state.update_data(prizes=prizes)
        if len(prizes) < data["winners"]:
            ask = await message.answer(
                texts.ask_place_prize(len(prizes) + 1, data["winners"]), reply_markup=kb.same_prize(prize)
            )
            await state.update_data(prize_msg_id=ask.message_id)
            return
        await state.set_state(CreateGiveaway.ends_at)
        await message.answer(texts.ASK_ENDS_AT)

    @router.callback_query(CreateGiveaway.prizes, kb.WizardCB.filter(F.action == "same_prize"))
    async def same_prize(cb: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        prizes = data["prizes"]
        prizes += [prizes[-1]] * (data["winners"] - len(prizes))
        await state.update_data(prizes=prizes, prize_msg_id=None)
        await state.set_state(CreateGiveaway.ends_at)
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.message.answer(texts.ASK_ENDS_AT)
        await cb.answer()

    @router.message(CreateGiveaway.ends_at, F.text)
    async def got_ends_at(message: Message, state: FSMContext):
        ends_at = parse_local_datetime(message.text, settings.tz)
        if ends_at is None or ends_at <= utcnow():
            await message.answer(texts.BAD_ENDS_AT)
            return
        await state.update_data(ends_at=ends_at.isoformat(), sponsor_ids=[], sponsor_titles=[])
        await state.set_state(CreateGiveaway.sponsors)
        await message.answer(texts.ASK_SPONSORS, reply_markup=kb.sponsors_done())

    @router.message(CreateGiveaway.sponsors)
    async def got_sponsor(message: Message, state: FSMContext, bot: Bot, sm: async_sessionmaker):
        explicit_link = None
        if isinstance(message.forward_origin, MessageOriginChannel):
            ref: int | str = message.forward_origin.chat.id
        elif message.text:
            parts = message.text.split()
            ref = int(parts[0]) if parts[0].lstrip("-").isdigit() else parts[0]
            if len(parts) > 1 and parts[1].startswith("https://t.me/"):
                explicit_link = parts[1]
        else:
            await message.answer(texts.SPONSOR_NOT_FOUND)
            return
        try:
            sponsor = await actions.add_sponsor(bot, settings, sm, ref, explicit_link)
        except actions.ActionError as e:
            await message.answer(e.message)
            return
        title = sponsor.title
        data = await state.get_data()
        if sponsor.id not in data["sponsor_ids"]:
            data["sponsor_ids"].append(sponsor.id)
            data["sponsor_titles"].append(title)
            await state.update_data(sponsor_ids=data["sponsor_ids"], sponsor_titles=data["sponsor_titles"])
        await message.answer(texts.sponsor_added(data["sponsor_titles"]), reply_markup=kb.sponsors_done())

    @router.callback_query(CreateGiveaway.sponsors, kb.WizardCB.filter(F.action == "sponsors_done"))
    async def sponsors_done(cb: CallbackQuery, state: FSMContext):
        await cb.message.edit_reply_markup(reply_markup=None)
        data = await state.get_data()
        preview = _draft_giveaway(data)
        await state.set_state(CreateGiveaway.confirm)
        await cb.message.answer(texts.PREVIEW_HEADER)
        await cb.message.answer(
            texts.giveaway_post(preview, settings.tz, data["sponsor_titles"]), reply_markup=kb.publish_confirm()
        )
        await cb.answer()

    @router.callback_query(CreateGiveaway.confirm, kb.WizardCB.filter(F.action == "cancel"))
    async def publish_cancel(cb: CallbackQuery, state: FSMContext):
        await state.clear()
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.message.answer(texts.CANCELLED, reply_markup=kb.owner_menu())
        await cb.answer()

    @router.callback_query(CreateGiveaway.confirm, kb.WizardCB.filter(F.action == "publish"))
    async def publish(cb: CallbackQuery, state: FSMContext, bot: Bot, sm: async_sessionmaker):
        data = await state.get_data()
        draft = _draft_giveaway(data)
        await cb.message.edit_reply_markup(reply_markup=None)
        try:
            g = await actions.publish_giveaway(
                bot,
                settings,
                sm,
                title=draft.title,
                description=draft.description,
                prizes=draft.prizes,
                ends_at=draft.ends_at,
                sponsor_ids=data["sponsor_ids"],
            )
        except actions.ActionError as e:
            await cb.message.answer(e.message)
            await cb.answer()
            return
        await state.clear()
        await cb.message.answer(texts.PUBLISHED.format(id=g.id), reply_markup=kb.owner_menu())
        await cb.answer()

    # --- Faol rozigrishlar ---

    @router.message(StateFilter(None), F.text == texts.BTN_LIST)
    async def list_active(message: Message, sm: async_sessionmaker):
        async with sm() as s:
            items = [(g, await service.participants_count(s, g.id)) for g in await service.active_giveaways(s)]
        if not items:
            await message.answer(texts.NO_ACTIVE)
            return
        for g, count in items:
            await message.answer(texts.active_item(g, count, settings.tz), reply_markup=kb.manage(g.id))

    @router.callback_query(kb.ManageCB.filter())
    async def manage(cb: CallbackQuery, callback_data: kb.ManageCB, sm: async_sessionmaker):
        gid = callback_data.giveaway_id
        if not callback_data.confirmed:
            prompt = texts.CONFIRM_FINISH if callback_data.action == "finish" else texts.CONFIRM_CANCEL
            await cb.message.answer(prompt.format(id=gid), reply_markup=kb.manage_confirm(callback_data.action, gid))
            await cb.answer()
            return
        async with sm() as s:
            if callback_data.action == "finish":
                ok, reply = await service.finish_now(s, gid), texts.FINISH_SCHEDULED
            else:
                ok, reply = await service.cancel_giveaway(s, gid), texts.GIVEAWAY_CANCELLED
        if not ok:
            await cb.answer(texts.NOT_ACTIVE, show_alert=True)
            return
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.message.answer(reply.format(id=gid))
        await cb.answer()

    # --- To'lovlar ---

    @router.message(StateFilter(None), F.text == texts.BTN_PAYOUTS)
    async def payouts(message: Message, sm: async_sessionmaker, vault: Vault):
        async with sm() as s:
            winners = await service.open_payouts(s)
        if not winners:
            await message.answer(texts.NO_PAYOUTS)
            return
        for w in winners:
            await message.answer(texts.payout_card(w, vault), reply_markup=kb.payout(w))

    @router.callback_query(kb.PaidCB.filter())
    async def paid(cb: CallbackQuery, callback_data: kb.PaidCB, state: FSMContext):
        await state.set_state(Payout.proof)
        await state.update_data(winner_id=callback_data.winner_id)
        await cb.message.answer(texts.ASK_PROOF)
        await cb.answer()

    @router.message(Payout.proof, F.photo | F.text | F.document)
    async def got_proof(message: Message, state: FSMContext, bot: Bot, sm: async_sessionmaker):
        winner_id = (await state.get_data())["winner_id"]
        await state.clear()
        try:
            delivered = await actions.deliver_prize(bot, sm, winner_id, message.copy_to)
        except actions.ActionError as e:
            await message.answer(e.message, reply_markup=kb.owner_menu())
            return
        if not delivered:
            await message.answer(texts.PROOF_FAILED, reply_markup=kb.owner_menu())
            return
        await message.answer(texts.PROOF_SENT, reply_markup=kb.owner_menu())

    return router


def _draft_giveaway(data: dict) -> Giveaway:
    """FSM ma'lumotidan saqlanmagan Giveaway (ko'rib chiqish uchun)."""
    return Giveaway(
        title=data["title"],
        description=data["description"],
        prizes_data=data["prizes"],
        ends_at=datetime.fromisoformat(data["ends_at"]),
        commit_hash="…",
    )
