"""Kontent agenti API: o'qitish chati, uslub qo'llanma, namunalar. Egasi va muharrir uchun."""

from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import select

from tgagent.agents.content import media, trainer
from tgagent.agents.content.models import Sample, SampleSource, StyleGuide, TrainMessage
from tgagent.panel.api import D, Staff

router = APIRouter(prefix="/api/content")

NOT_FOUND = "Topilmadi."
EMPTY_SAMPLE = "Post matni yoki rasmi bo'lishi kerak."
TOO_MANY_IMAGES = "Bitta postda ko'pi bilan 10 ta rasm bo'ladi (Telegram albomi)."
EMPTY_MESSAGE = "Xabar bo'sh."
ALREADY_DECIDED = "Bu taklif bo'yicha qaror allaqachon qabul qilingan."
EMPTY_GUIDE = "Qo'llanma bo'sh bo'lmasin."


def sample_out(x: Sample | None) -> dict | None:
    if x is None:
        return None
    return {
        "id": x.id, "source": x.source, "source_name": x.source_name, "text": x.text,
        "images": [f"/api/content/media/{name}" for name in x.images], "image_note": x.image_note,
        "image_desc": x.image_desc, "analysis": x.analysis, "added_by": x.added_by,
        "created_at": x.created_at.isoformat(),
    }


def message_out(m: TrainMessage) -> dict:
    return {
        "id": m.id, "role": m.role, "author": m.author, "text": m.text,
        "sample": sample_out(m.sample),
        "sample_deleted": m.role == "user" and not m.text and m.sample is None,  # namuna o'chirilgan
        "proposal": m.proposal, "proposal_note": m.proposal_note, "proposal_status": m.proposal_status,
        "created_at": m.created_at.isoformat(),
    }


def guide_out(g: StyleGuide) -> dict:
    return {"id": g.id, "text": g.text, "note": g.note, "author": g.author, "created_at": g.created_at.isoformat()}


# --- AI holati ---


@router.get("/usage")
async def usage(d: D, _: Staff):
    s = d.settings
    enabled = d.llm is not None and d.llm.enabled
    return {
        "enabled": enabled, "model": s.llm_model, "limit": s.llm_monthly_limit,
        "month_cost": await d.llm.month_cost() if d.llm else 0.0,
    }


# --- O'qitish chati ---


@router.get("/chat")
async def chat(d: D, _: Staff):
    async with d.sm() as s:
        msgs = await trainer.history(s)
    return {"messages": [message_out(m) for m in msgs], "thinking": trainer.thinking(),
            "error": trainer.responder.error}


@router.post("/chat/message")
async def chat_message(
    d: D,
    staff: Staff,
    text: Annotated[str, Form(max_length=5000)] = "",
    sample: Annotated[bool, Form()] = False,  # namuna post (rasm biriktirilsa — doim namuna)
    source: Annotated[SampleSource, Form()] = SampleSource.OTHER,
    source_name: Annotated[str, Form(max_length=255)] = "",
    image_note: Annotated[str, Form(max_length=1000)] = "",
    images: Annotated[list[UploadFile], File()] = [],  # noqa: B006 — FastAPI har so'rovga yangisini beradi
):
    """Chatga xabar yoki namuna post. Agent fonda javob beradi — panel `GET /chat` ni so'rab turadi."""
    if len(images) > media.MAX_ALBUM:
        raise HTTPException(400, TOO_MANY_IMAGES)
    files = [b for f in images if (b := await f.read(media.MAX_BYTES + 1))]
    if not text.strip() and not files:
        raise HTTPException(400, EMPTY_SAMPLE if sample else EMPTY_MESSAGE)
    names: list[str] = []
    try:
        for data in files:
            names.append(media.save_image(d.settings.media_dir, data))
    except media.BadImage as e:
        for name in names:
            media.delete_image(d.settings.media_dir, name)
        raise HTTPException(400, str(e)) from None
    async with d.sm() as s:
        if sample or names:
            msg = await trainer.add_sample(s, text=text, author=staff.name, source=source,
                                           source_name=source_name.strip() or None, images=names,
                                           image_note=image_note)
        else:
            msg = await trainer.add_message(s, text=text, author=staff.name)
    await trainer.kick(d.sm, d.llm, channel=d.main_chat.title, media_dir=d.settings.media_dir)
    return message_out(msg)


@router.post("/chat/retry")
async def chat_retry(d: D, _: Staff):
    """Xatodan keyin (masalan AI vaqtincha javob bermadi) javobni qayta so'rash."""
    await trainer.kick(d.sm, d.llm, channel=d.main_chat.title, media_dir=d.settings.media_dir)
    return {"ok": True}


class DecisionIn(BaseModel):
    accept: bool
    text: str | None = Field(None, max_length=20000)  # xodim tuzatgan qo'llanma matni


@router.post("/chat/{mid}/decide")
async def chat_decide(mid: int, body: DecisionIn, d: D, staff: Staff):
    async with d.sm() as s:
        msg = await s.get(TrainMessage, mid)
        if msg is None or msg.proposal is None:
            raise HTTPException(404, NOT_FOUND)
        if body.accept and body.text is not None and not body.text.strip():
            raise HTTPException(400, EMPTY_GUIDE)
        if msg.proposal_status != "pending":
            raise HTTPException(409, ALREADY_DECIDED)
        g = await trainer.decide(s, mid, accept=body.accept, author=staff.name, text=body.text)
        return {"ok": True, "guide": guide_out(g) if g else None}


# --- Uslub qo'llanma ---


@router.get("/guide")
async def guide(d: D, _: Staff):
    async with d.sm() as s:
        versions = (await s.scalars(select(StyleGuide).order_by(StyleGuide.id.desc()).limit(50))).all()
    return {"current": guide_out(versions[0]) if versions else None, "versions": [guide_out(g) for g in versions]}


class GuideIn(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    note: str = Field("", max_length=500)


@router.put("/guide")
async def guide_save(body: GuideIn, d: D, staff: Staff):
    if not body.text.strip():
        raise HTTPException(400, EMPTY_GUIDE)
    async with d.sm() as s:
        g = await trainer.save_guide(s, body.text, body.note.strip() or "Qo'lda tahrirlandi", staff.name)
        return guide_out(g)


@router.post("/guide/{vid}/restore")
async def guide_restore(vid: int, d: D, staff: Staff):
    async with d.sm() as s:
        old = await s.get(StyleGuide, vid)
        if old is None:
            raise HTTPException(404, NOT_FOUND)
        g = await trainer.save_guide(s, old.text, f"#{vid}-versiyaga qaytarildi", staff.name)
        return guide_out(g)


# --- Namunalar ---


@router.get("/samples")
async def samples(d: D, _: Staff):
    async with d.sm() as s:
        rows = (await s.scalars(select(Sample).order_by(Sample.id.desc()))).all()
    return [sample_out(x) for x in rows]


@router.delete("/samples/{sid}")
async def sample_delete(sid: int, d: D, _: Staff):
    async with d.sm() as s:
        x = await s.get(Sample, sid)
        if x is None:
            raise HTTPException(404, NOT_FOUND)
        names = list(x.images)
        await s.delete(x)
        await s.commit()
    for name in names:
        media.delete_image(d.settings.media_dir, name)
    return {"ok": True}


@router.get("/media/{name}")
async def media_file(name: str, d: D, _: Staff):
    path = media.image_path(d.settings.media_dir, name)
    if path is None:
        raise HTTPException(404, NOT_FOUND)
    return FileResponse(path, media_type="image/jpeg", headers={"cache-control": "private, max-age=86400"})
