"""O'qitish chati: namunalar, agent javobi, uslub qo'llanma versiyalari."""

import asyncio
import logging
from dataclasses import dataclass

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgagent.agents.content import media, prompts
from tgagent.agents.content.models import (
    ProposalStatus,
    Sample,
    SampleSource,
    StyleGuide,
    TrainMessage,
)
from tgagent.core.llm import FAILED, LLM, NO_KEY, Image, LlmError, Msg

log = logging.getLogger(__name__)

HISTORY = 30  # agentga beriladigan oxirgi chat xabarlari
MAX_NEW_SAMPLES = 20  # bir javobda tahlil qilinadigan yangi namunalar


async def current_guide(session: AsyncSession) -> StyleGuide | None:
    return await session.scalar(select(StyleGuide).order_by(StyleGuide.id.desc()).limit(1))


async def save_guide(session: AsyncSession, text: str, note: str | None, author: str) -> StyleGuide:
    g = StyleGuide(text=text.strip(), note=note, author=author)
    session.add(g)
    await session.commit()
    return g


async def add_sample(session: AsyncSession, *, text: str, author: str, source: SampleSource = SampleSource.OTHER,
                     source_name: str | None = None, images: list[str] | None = None, image_note: str | None = None,
                     chat_id: int | None = None, message_id: int | None = None) -> TrainMessage:
    """Namuna qo'shadi va chatda ko'rsatadi (agent javobini `kick` boshlaydi)."""
    sample = Sample(source=source, source_name=source_name, text=text.strip(), images=images or [],
                    image_note=(image_note or "").strip() or None, chat_id=chat_id, message_id=message_id,
                    added_by=author)
    session.add(sample)
    await session.flush()
    msg = TrainMessage(role="user", author=author, sample_id=sample.id, sample=sample)
    session.add(msg)
    await session.commit()
    return msg


async def pending_samples(session: AsyncSession) -> list[Sample]:
    return list((await session.scalars(
        select(Sample).where(Sample.analysis.is_(None)).order_by(Sample.id).limit(MAX_NEW_SAMPLES)
    )).all())


async def history(session: AsyncSession, limit: int = 200) -> list[TrainMessage]:
    rows = (await session.scalars(select(TrainMessage).order_by(TrainMessage.id.desc()).limit(limit))).all()
    return list(reversed(rows))


def _history_text(m: TrainMessage) -> str:
    if m.sample_id is not None:
        s = m.sample
        if s is None:
            return "[sample post — deleted]"
        head = f"[sample post #{s.id} from {s.source_name or s.source}]"
        body = (s.text or "(no text)")[:500]
        extra = f"\nPhotos ({len(s.images)}): {s.image_desc}" if s.image_desc else ""
        return f"{head}\n{body}{extra}"
    text = m.text
    if m.proposal_status:
        text += f"\n[proposed a style guide change: {m.proposal_note} — editor {m.proposal_status}]"
    return text


async def add_message(session: AsyncSession, *, text: str, author: str) -> TrainMessage:
    msg = TrainMessage(role="user", author=author, text=text.strip(), sample=None)
    session.add(msg)
    await session.commit()
    return msg


async def _unanswered(session: AsyncSession) -> bool:
    """Agent oxirgi javobidan keyin xodim yozgan xabar yoki tahlil qilinmagan namuna bormi."""
    last_reply = await session.scalar(select(func.max(TrainMessage.id)).where(TrainMessage.role == "assistant"))
    newer = await session.scalar(select(func.count()).select_from(TrainMessage).where(
        TrainMessage.role == "user", TrainMessage.id > (last_reply or 0)))
    return bool(newer) or bool(await pending_samples(session))


async def reply(sm: async_sessionmaker, llm: LLM, *, channel: str, media_dir: str) -> TrainMessage:
    """Oxirgi javobdan keyingi xabarlarga agent javobi (va qo'llanma taklifi). Yangi namunalar rasmi bilan beriladi."""
    async with sm() as s:
        guide = await current_guide(s)
        past = (await s.scalars(select(TrainMessage).order_by(TrainMessage.id.desc()).limit(HISTORY))).all()
        new = await pending_samples(s)

    messages = [Msg("system", prompts.TRAINER_SYSTEM.format(channel=channel)),
                Msg("system", prompts.guide_block(guide.text if guide else None))]
    new_ids = {x.id for x in new}
    for m in reversed(past):
        if m.sample_id in new_ids:
            continue  # yangilari pastda rasmi bilan beriladi
        messages.append(Msg("assistant" if m.role == "assistant" else "user", _history_text(m)))
    for x in new:
        photos = [Image(data) for name in x.images if (data := media.read_image(media_dir, name))]
        messages.append(Msg("user", prompts.sample_block(x.id, x.source_name or x.source, x.text, x.image_note,
                                                         len(photos)), photos))
    messages.append(Msg("system", prompts.RESPOND))

    out = await llm.complete_json(messages, purpose="content.train", schema=prompts.TRAINER_SCHEMA)

    async with sm() as s:
        notes = {n["id"]: n for n in out.get("samples", [])}
        for x in new:
            n = notes.get(x.id)
            await s.execute(update(Sample).where(Sample.id == x.id).values(
                analysis=(n["analysis"] if n else "") or "-", image_desc=(n["image_desc"] if n else None) or None,
            ))
        msg = TrainMessage(role="assistant", author="AI", text=out["reply"], sample=None)
        proposal = (out.get("guide") or "").strip()
        if proposal and proposal != (guide.text if guide else ""):
            # Eski javobsiz takliflar endi eskirgan (yangisi joriy qo'llanmadan kelib chiqqan)
            await s.execute(update(TrainMessage).where(TrainMessage.proposal_status == ProposalStatus.PENDING)
                            .values(proposal_status=ProposalStatus.SUPERSEDED))
            msg.proposal = proposal
            msg.proposal_note = (out.get("guide_note") or "")[:500] or None
            msg.proposal_status = ProposalStatus.PENDING
        s.add(msg)
        await s.commit()
        return msg


# --- Fon javobi: xodim yozaveradi, agent navbat bilan javob beradi (chat kabi) ---


@dataclass
class _Responder:
    task: asyncio.Task | None = None
    again: bool = False  # agent ishlayotganda yangi xabar keldi
    error: str | None = None  # oxirgi xato (panelda ko'rsatiladi)


responder = _Responder()


def thinking() -> bool:
    return responder.task is not None and not responder.task.done()


async def kick(sm: async_sessionmaker, llm: LLM | None, *, channel: str, media_dir: str) -> None:
    """Agentni javob berishga undaydi. Allaqachon yozayotgan bo'lsa — keyingi javobida yangi xabarlarni ham oladi."""
    responder.error = None
    if llm is None or not llm.enabled:
        responder.error = NO_KEY
        return
    if thinking():
        responder.again = True
        return
    responder.task = asyncio.create_task(_respond_loop(sm, llm, channel, media_dir))
    await asyncio.sleep(0)


async def _respond_loop(sm: async_sessionmaker, llm: LLM, channel: str, media_dir: str) -> None:
    try:
        while True:
            responder.again = False
            async with sm() as s:
                pending = await _unanswered(s)
            if not pending:
                if responder.again:
                    continue
                break  # bundan keyin await yo'q — kick() «tugadi» deb ko'radi
            await reply(sm, llm, channel=channel, media_dir=media_dir)
    except LlmError as e:
        responder.error = str(e)
    except Exception:
        log.exception("O'qitish chati: agent javob bermadi")
        responder.error = FAILED


async def decide(session: AsyncSession, message_id: int, *, accept: bool, author: str,
                 text: str | None = None) -> StyleGuide | None:
    """Taklifni qabul qiladi (xodim tuzatgan matn bilan bo'lishi mumkin) yoki rad etadi."""
    msg = await session.get(TrainMessage, message_id)
    if msg is None or msg.proposal_status != ProposalStatus.PENDING:
        return None
    msg.proposal_status = ProposalStatus.ACCEPTED if accept else ProposalStatus.REJECTED
    if not accept:
        await session.commit()
        return None
    edited = text is not None and text.strip() != (msg.proposal or "").strip()
    note = msg.proposal_note or "AI taklifi"
    return await save_guide(session, text if edited else msg.proposal, f"{note} ({author} tuzatib qabul qildi)"
                            if edited else note, "AI" if not edited else author)
