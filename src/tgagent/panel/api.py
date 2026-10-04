"""Panel JSON API. Hamma yo'llar /api ostida, faqat Owner/Editor sessiyasi bilan."""

import html
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated

from aiogram import Bot
from aiogram.types import BufferedInputFile
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.agents.giveaway import actions, service, texts
from tgagent.agents.giveaway.models import (
    Giveaway,
    GiveawayStatus,
    Participant,
    Prize,
    PrizeType,
    SponsorChannel,
    Winner,
    WinnerStatus,
    giveaway_sponsors,
)
from tgagent.agents.giveaway.validators import parse_prize
from tgagent.channels.telegram_bot.chats import ChatRef
from tgagent.config import Settings
from tgagent.core.crypto import Vault
from tgagent.core.db import utcnow
from tgagent.panel import auth
from tgagent.panel import texts as ptexts

MAX_PROOF_BYTES = 10 * 1024 * 1024
_TAG = re.compile(r"<[^>]+>")


@dataclass
class Deps:
    settings: Settings
    bot: Bot
    sm: async_sessionmaker
    vault: Vault
    main_chat: ChatRef
    logins: auth.LoginRequests


def deps(request: Request) -> Deps:
    return request.app.state.deps


def plain(text: str) -> str:
    """Bot matnidagi HTML teglarini olib tashlaydi (panelda oddiy matn ko'rsatiladi)."""
    return html.unescape(_TAG.sub("", text))


async def current_staff(request: Request, d: Annotated[Deps, Depends(deps)]) -> auth.Staff:
    staff = await auth.session_staff(d.sm, d.settings, request.cookies.get(auth.COOKIE))
    if staff is None:
        raise HTTPException(401, ptexts.API_NOT_LOGGED_IN)
    # CSRF: brauzer boshqa saytdan bunday sarlavhali so'rov yubora olmaydi
    if request.method not in ("GET", "HEAD") and request.headers.get("x-panel") != "1":
        raise HTTPException(403, ptexts.API_FORBIDDEN)
    return staff


async def owner(staff: Annotated[auth.Staff, Depends(current_staff)]) -> auth.Staff:
    if not staff.is_owner:
        raise HTTPException(403, ptexts.API_OWNER_ONLY)
    return staff


D = Annotated[Deps, Depends(deps)]
Owner = Annotated[auth.Staff, Depends(owner)]

router = APIRouter(prefix="/api")


# --- Kirish ---


@router.post("/auth/start")
async def auth_start(d: D):
    token = d.logins.create()
    me = await d.bot.me()
    return {"token": token, "bot_url": f"https://t.me/{me.username}?start=login_{token}", "ttl": auth.LOGIN_TTL}


@router.get("/auth/poll")
async def auth_poll(token: str, request: Request, response: Response, d: D):
    req = d.logins.get(token)
    if req is None:
        return {"status": "expired"}
    if req.user_id is None:
        return {"status": "pending"}
    d.logins.pop(token)
    if auth.staff_role(d.settings, req.user_id) is None:
        return {"status": "expired"}
    raw = await auth.create_session(d.sm, req.user_id, req.user_name)
    response.set_cookie(
        auth.COOKIE,
        raw,
        max_age=int(auth.SESSION_TTL.total_seconds()),
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https" or d.settings.panel_url.startswith("https"),
    )
    return {"status": "ok"}


@router.post("/auth/logout")
async def auth_logout(request: Request, response: Response, d: D, _: Annotated[auth.Staff, Depends(current_staff)]):
    await auth.delete_session(d.sm, request.cookies[auth.COOKIE])
    response.delete_cookie(auth.COOKIE)
    return {"ok": True}


@router.get("/me")
async def me(staff: Annotated[auth.Staff, Depends(current_staff)], d: D):
    return {
        "user_id": staff.user_id,
        "name": staff.name,
        "role": staff.role,
        "channel": {"title": d.main_chat.title, "link": d.main_chat.link},
        "timezone": d.settings.timezone,
    }


# --- Ko'rinishlar ---


def prize_out(p: Prize) -> dict:
    return {**p.to_dict(), "label": plain(texts.prize_text(p))}


def post_url(d: Deps, g: Giveaway) -> str | None:
    if not g.message_id:
        return None
    link = d.main_chat.link
    if link.startswith("https://t.me/") and "+" not in link and "joinchat" not in link:
        return f"{link}/{g.message_id}"
    return f"https://t.me/c/{str(g.chat_id).removeprefix('-100')}/{g.message_id}"


def giveaway_out(d: Deps, g: Giveaway, participants: int) -> dict:
    finished = g.status == GiveawayStatus.FINISHED
    return {
        "id": g.id,
        "title": g.title,
        "description": g.description,
        "status": g.status,
        "prizes": [prize_out(p) for p in g.prizes],
        "winners_count": g.winners_count,
        "participants": participants,
        "ends_at": g.ends_at.isoformat(),
        "created_at": g.created_at.isoformat(),
        "sponsors": [sponsor_out(s) for s in g.sponsors],
        "post_url": post_url(d, g),
        "commit_hash": g.commit_hash,
        # seed faqat natija e'lon qilingach ochiladi (commit-reveal)
        "seed": g.seed if finished else None,
        "list_hash": g.list_hash if finished else None,
    }


def sponsor_out(s: SponsorChannel) -> dict:
    return {"id": s.id, "title": s.title, "link": s.link, "chat_id": s.chat_id}


def winner_out(w: Winner) -> dict:
    p = w.participant
    return {
        "id": w.id,
        "giveaway_id": w.giveaway_id,
        "giveaway_title": w.giveaway.title,
        "place": w.place,
        "prize": prize_out(w.prize),
        "user_id": w.user_id,
        "name": p.full_name,
        "username": p.username,
        "number": p.number,
        "status": w.status,
        "claim_step": w.claim_step,
        "card_masked": w.card_masked,
        "done_at": w.done_at.isoformat() if w.done_at else None,
    }


# --- Bosh sahifa ---


@router.get("/stats")
async def stats(d: D, _: Owner):
    async with d.sm() as s:
        active = await service.active_giveaways(s)
        counts = await service.participant_counts(s)
        payouts = await service.open_payouts(s)
    return {
        "active_giveaways": len(active),
        "active_participants": sum(counts.get(g.id, 0) for g in active),
        "awaiting_info": sum(w.status == WinnerStatus.AWAITING_INFO for w in payouts),
        "ready_to_pay": sum(w.status == WinnerStatus.INFO_RECEIVED for w in payouts),
    }


# --- Rozigrishlar ---


class GiveawayIn(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=3000)
    prizes: list[str] = Field(min_length=1, max_length=100)  # har o'rin uchun: "500 ming", "iPhone 15" ...
    ends_at: str  # mahalliy vaqt, "2026-10-15T20:00"
    sponsor_ids: list[int] = []


@dataclass
class ParsedGiveaway:
    prizes: list[Prize]
    ends_at: datetime | None
    errors: dict[str, str]


def parse_giveaway(d: Deps, body: GiveawayIn) -> ParsedGiveaway:
    errors: dict[str, str] = {}
    prizes = []
    for i, raw in enumerate(body.prizes):
        p = parse_prize(raw)
        if p is None:
            errors[f"prizes.{i}"] = ptexts.API_BAD_PRIZE
        else:
            prizes.append(p)
    try:
        ends_at = datetime.fromisoformat(body.ends_at).replace(tzinfo=d.settings.tz)
    except ValueError:
        ends_at = None
    if ends_at is None or ends_at <= utcnow():
        errors["ends_at"] = ptexts.API_BAD_ENDS_AT
    if not body.title.strip():
        errors["title"] = ptexts.API_REQUIRED
    if not body.description.strip():
        errors["description"] = ptexts.API_REQUIRED
    return ParsedGiveaway(prizes, ends_at, errors)


async def _sponsors(d: Deps, ids: list[int]) -> list[SponsorChannel]:
    async with d.sm() as s:
        found = (await s.scalars(select(SponsorChannel).where(SponsorChannel.id.in_(ids)))).all()
    by_id = {sp.id: sp for sp in found}
    return [by_id[i] for i in ids if i in by_id]


@router.post("/giveaways/preview")
async def giveaway_preview(body: GiveawayIn, d: D, _: Owner):
    """Post ko'rinishi + xatolar (forma to'ldirilayotganda chaqiriladi)."""
    parsed = parse_giveaway(d, body)
    sponsors = await _sponsors(d, body.sponsor_ids)
    html_text = None
    if not parsed.errors:
        draft = Giveaway(
            title=body.title.strip(),
            description=body.description.strip(),
            prizes_data=[p.to_dict() for p in parsed.prizes],
            ends_at=parsed.ends_at,
            commit_hash="…",
        )
        html_text = texts.giveaway_post(draft, d.settings.tz, [sp.title for sp in sponsors])
    return {
        "errors": parsed.errors,
        "prizes": [prize_out(p) if p else None for p in map(parse_prize, body.prizes)],
        "post_html": html_text,
    }


@router.post("/giveaways")
async def giveaway_create(body: GiveawayIn, d: D, _: Owner):
    parsed = parse_giveaway(d, body)
    if parsed.errors:
        raise HTTPException(422, {"errors": parsed.errors})
    sponsors = await _sponsors(d, body.sponsor_ids)
    try:
        g = await actions.publish_giveaway(
            d.bot,
            d.settings,
            d.sm,
            title=body.title.strip(),
            description=body.description.strip(),
            prizes=parsed.prizes,
            ends_at=parsed.ends_at,
            sponsor_ids=[sp.id for sp in sponsors],
        )
    except actions.ActionError as e:
        raise HTTPException(400, plain(e.message)) from None
    return {"id": g.id}


@router.get("/giveaways")
async def giveaway_list(d: D, _: Owner, status: GiveawayStatus | None = None):
    async with d.sm() as s:
        items = await service.list_giveaways(s, status)
        counts = await service.participant_counts(s)
    return [giveaway_out(d, g, counts.get(g.id, 0)) for g in items]


@router.get("/giveaways/{gid}")
async def giveaway_detail(gid: int, d: D, _: Owner):
    async with d.sm() as s:
        g = await s.get(Giveaway, gid)
        if g is None:
            raise HTTPException(404, plain(texts.GIVEAWAY_NOT_FOUND))
        count = await service.participants_count(s, gid)
        winners = await service.list_winners(s, gid)
    return {**giveaway_out(d, g, count), "winners": [winner_out(w) for w in winners]}


@router.get("/giveaways/{gid}/participants")
async def giveaway_participants(gid: int, d: D, _: Owner, q: str = "", offset: int = 0, limit: int = 50):
    limit = min(max(limit, 1), 200)
    query = select(Participant).where(Participant.giveaway_id == gid)
    if q.strip():
        like = f"%{q.strip().lstrip('@')}%"
        query = query.where(Participant.full_name.ilike(like) | Participant.username.ilike(like))
    async with d.sm() as s:
        rows = (await s.scalars(query.order_by(Participant.number).offset(max(offset, 0)).limit(limit + 1))).all()
    return {
        "items": [
            {
                "number": p.number,
                "user_id": p.user_id,
                "name": p.full_name,
                "username": p.username,
                "joined_at": p.joined_at.isoformat(),
            }
            for p in rows[:limit]
        ],
        "has_more": len(rows) > limit,
    }


@router.post("/giveaways/{gid}/finish")
async def giveaway_finish(gid: int, d: D, _: Owner):
    async with d.sm() as s:
        if not await service.finish_now(s, gid):
            raise HTTPException(400, plain(texts.NOT_ACTIVE))
    return {"ok": True}


@router.post("/giveaways/{gid}/cancel")
async def giveaway_cancel(gid: int, d: D, _: Owner):
    async with d.sm() as s:
        if not await service.cancel_giveaway(s, gid):
            raise HTTPException(400, plain(texts.NOT_ACTIVE))
    return {"ok": True}


# --- Homiylar ---


class SponsorIn(BaseModel):
    ref: str = Field(min_length=1, max_length=255)  # @username, -100... ID yoki t.me/username
    link: str | None = None  # yopiq kanal uchun taklif havolasi


def sponsor_ref(raw: str) -> int | str:
    raw = raw.strip()
    if raw.lstrip("-").isdigit():
        return int(raw)
    m = re.fullmatch(r"(?:https?://)?t\.me/([A-Za-z0-9_]{4,})/?", raw)
    return "@" + m.group(1) if m else raw


@router.get("/sponsors")
async def sponsor_list(d: D, _: Owner):
    async with d.sm() as s:
        return [sponsor_out(sp) for sp in await service.list_sponsors(s)]


@router.post("/sponsors")
async def sponsor_add(body: SponsorIn, d: D, _: Owner):
    link = (body.link or "").strip() or None
    if link and not link.startswith("https://t.me/"):
        raise HTTPException(400, ptexts.API_BAD_LINK)
    try:
        sp = await actions.add_sponsor(d.bot, d.settings, d.sm, sponsor_ref(body.ref), link)
    except actions.ActionError as e:
        raise HTTPException(400, plain(e.message)) from None
    return sponsor_out(sp)


@router.delete("/sponsors/{sid}")
async def sponsor_delete(sid: int, d: D, _: Owner):
    async with d.sm() as s:
        sp = await s.get(SponsorChannel, sid)
        if sp is None:
            raise HTTPException(404, ptexts.API_NOT_FOUND)
        in_use = await s.scalar(
            select(Giveaway.id)
            .join(giveaway_sponsors, giveaway_sponsors.c.giveaway_id == Giveaway.id)
            .where(giveaway_sponsors.c.sponsor_id == sid, Giveaway.status == GiveawayStatus.ACTIVE)
            .limit(1)
        )
        if in_use:
            raise HTTPException(400, ptexts.API_SPONSOR_IN_USE.format(id=in_use))
        await s.execute(delete(giveaway_sponsors).where(giveaway_sponsors.c.sponsor_id == sid))
        await s.delete(sp)
        await s.commit()
    return {"ok": True}


# --- To'lovlar ---


@router.get("/payouts")
async def payout_list(d: D, _: Owner, status: str = "open"):
    async with d.sm() as s:
        if status == "done":
            winners = (
                await s.scalars(
                    select(Winner).where(Winner.status == WinnerStatus.DONE).order_by(Winner.done_at.desc()).limit(100)
                )
            ).all()
        else:
            winners = await service.open_payouts(s)
    return [winner_out(w) for w in winners]


@router.get("/payouts/{wid}/details")
async def payout_details(wid: int, d: D, _: Owner):
    """Shifrlangan ma'lumotni ochib beradi — faqat egasi, faqat so'ralganda."""
    async with d.sm() as s:
        w = await s.get(Winner, wid)
    if w is None:
        raise HTTPException(404, ptexts.API_NOT_FOUND)
    if w.status != WinnerStatus.INFO_RECEIVED:
        return {}
    dec = d.vault.decrypt
    if w.prize.type == PrizeType.MONEY:
        return {"card": dec(w.card_enc), "card_holder": dec(w.card_holder_enc)}
    return {"full_name": dec(w.full_name_enc), "phone": dec(w.phone_enc), "address": dec(w.address_enc)}


@router.post("/payouts/{wid}/deliver")
async def payout_deliver(
    wid: int,
    d: D,
    _: Owner,
    note: Annotated[str, Form(max_length=1000)] = "",
    proof: Annotated[UploadFile | None, File()] = None,
):
    """«To'landi / Yuborildi»: chek (rasm/fayl) va/yoki izoh (masalan BTS trek raqami) g'olibga ketadi."""
    data = await proof.read(MAX_PROOF_BYTES + 1) if proof else b""
    if len(data) > MAX_PROOF_BYTES:
        raise HTTPException(400, ptexts.API_FILE_TOO_BIG)
    note = note.strip()
    if not data and not note:
        raise HTTPException(400, ptexts.API_NEED_PROOF)
    caption = html.escape(note) if note else None

    async def send(chat_id: int):
        if not data:
            await d.bot.send_message(chat_id, caption)
            return
        file = BufferedInputFile(data, filename=proof.filename or "chek")
        if (proof.content_type or "").startswith("image/"):
            await d.bot.send_photo(chat_id, file, caption=caption)
        else:
            await d.bot.send_document(chat_id, file, caption=caption)

    try:
        delivered = await actions.deliver_prize(d.bot, d.sm, wid, send)
    except actions.ActionError as e:
        raise HTTPException(400, plain(e.message)) from None
    return {"ok": True, "delivered": delivered}
