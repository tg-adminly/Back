"""O'qitish chati: namunalar, agent javobi, uslub qo'llanma versiyalari."""

import asyncio

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgagent.agents.content import media, prompts
from tgagent.agents.content.models import (
    ProposalStatus,
    Sample,
    SampleSource,
    StyleGuide,
    TrainMessage,
)
from tgagent.core.llm import LLM, Image, Msg

HISTORY = 30  # agentga beriladigan oxirgi chat xabarlari
MAX_NEW_SAMPLES = 20  # bir javobda tahlil qilinadigan yangi namunalar
_lock = asyncio.Lock()  # bir vaqtda bitta javob (ikki xodim birdan yozsa ham)


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
    """Namuna qo'shadi va chatda ko'rsatadi. Agent hali javob bermaydi — xodim «tahlil qil» deguncha yig'iladi."""
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


async def reply(sm: async_sessionmaker, llm: LLM, *, channel: str, author: str, text: str, media_dir: str) -> TrainMessage:
    """Xodim xabarini saqlaydi, agent javobini (va qo'llanma taklifini) qaytaradi."""
    async with _lock:
        async with sm() as s:
            if text.strip():
                s.add(TrainMessage(role="user", author=author, text=text.strip()))
                await s.commit()
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
        if not text.strip():
            messages.append(Msg("user", "Analyze the new samples above and update the style guide if needed."))

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
