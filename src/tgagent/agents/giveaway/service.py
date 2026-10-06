"""Rozigrish bo'yicha DB amallari (Telegram'ga bog'liq emas)."""

from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from tgagent.agents.giveaway import draw
from tgagent.agents.giveaway.models import (
    ClaimStep,
    DrawPick,
    Giveaway,
    GiveawayStatus,
    Participant,
    Prize,
    PrizeType,
    SponsorChannel,
    SubscriptionMiss,
    Winner,
    WinnerStatus,
)
from tgagent.core.db import utcnow


async def upsert_sponsor(session: AsyncSession, chat_id: int, title: str, link: str) -> SponsorChannel:
    sponsor = await session.scalar(select(SponsorChannel).where(SponsorChannel.chat_id == chat_id))
    if sponsor is None:
        sponsor = SponsorChannel(chat_id=chat_id, title=title, link=link)
        session.add(sponsor)
    else:
        sponsor.title, sponsor.link = title, link
    await session.commit()
    return sponsor


async def create_giveaway(
    session: AsyncSession,
    *,
    title: str,
    description: str,
    prizes: list[Prize],
    ends_at: datetime,
    chat_id: int,
    sponsor_ids: list[int],
    auto_draw: bool = False,
) -> Giveaway:
    seed = draw.new_seed()
    sponsors = (await session.scalars(select(SponsorChannel).where(SponsorChannel.id.in_(sponsor_ids)))).all()
    giveaway = Giveaway(
        title=title,
        description=description,
        prizes_data=[p.to_dict() for p in prizes],
        ends_at=ends_at,
        seed=seed,
        commit_hash=draw.commit_of(seed),
        chat_id=chat_id,
        sponsors=list(sponsors),
        auto_draw=auto_draw,
    )
    session.add(giveaway)
    await session.commit()
    return giveaway


async def get_participant(session: AsyncSession, giveaway_id: int, user_id: int) -> Participant | None:
    return await session.scalar(
        select(Participant).where(Participant.giveaway_id == giveaway_id, Participant.user_id == user_id)
    )


async def add_participant(
    session: AsyncSession, giveaway_id: int, user_id: int, full_name: str, username: str | None
) -> tuple[Participant, bool]:
    """Ishtirokchini qo'shadi. (participant, yangi_qo'shildimi) qaytaradi."""
    for _ in range(5):
        existing = await get_participant(session, giveaway_id, user_id)
        if existing:
            return existing, False
        last = await session.scalar(
            select(func.max(Participant.number)).where(Participant.giveaway_id == giveaway_id)
        )
        participant = Participant(
            giveaway_id=giveaway_id,
            user_id=user_id,
            number=(last or 0) + 1,
            full_name=full_name[:255],
            username=username,
        )
        session.add(participant)
        try:
            await session.commit()
            return participant, True
        except IntegrityError:
            await session.rollback()  # raqam band bo'ldi yoki parallel qo'shildi — qayta urinamiz
    raise RuntimeError("Ishtirokchini qo'shib bo'lmadi")


async def participants_count(session: AsyncSession, giveaway_id: int) -> int:
    return await session.scalar(
        select(func.count()).select_from(Participant).where(Participant.giveaway_id == giveaway_id)
    ) or 0


async def list_participants(session: AsyncSession, giveaway_id: int) -> list[Participant]:
    return list(
        (
            await session.scalars(
                select(Participant).where(Participant.giveaway_id == giveaway_id).order_by(Participant.number)
            )
        ).all()
    )


async def active_giveaways(session: AsyncSession) -> list[Giveaway]:
    return list(
        (
            await session.scalars(
                select(Giveaway).where(Giveaway.status == GiveawayStatus.ACTIVE).order_by(Giveaway.ends_at)
            )
        ).all()
    )


async def due_giveaway_ids(session: AsyncSession, now: datetime | None = None) -> list[int]:
    """Avtomatik rejim: vaqti kelgan — bot o'zi yopib, g'olibni aniqlaydi."""
    now = now or utcnow()
    return list(
        (
            await session.scalars(
                select(Giveaway.id).where(
                    Giveaway.status == GiveawayStatus.ACTIVE,
                    Giveaway.auto_draw.is_(True),
                    Giveaway.ends_at <= now,
                )
            )
        ).all()
    )


async def due_reminder_ids(session: AsyncSession, now: datetime | None = None) -> list[int]:
    """Jonli rejim: vaqti kelgan, lekin hali eslatilmagan. Qatnashish yopilmaydi — o'yinni egasi boshlaydi."""
    now = now or utcnow()
    return list(
        (
            await session.scalars(
                select(Giveaway.id).where(
                    Giveaway.status == GiveawayStatus.ACTIVE,
                    Giveaway.auto_draw.is_(False),
                    Giveaway.reminded_at.is_(None),
                    Giveaway.ends_at <= now,
                )
            )
        ).all()
    )


def first_claim_step(prize_type: PrizeType) -> ClaimStep:
    return ClaimStep.CARD if prize_type == PrizeType.MONEY else ClaimStep.FULL_NAME


async def pending_claim(session: AsyncSession, user_id: int) -> Winner | None:
    """G'olibdan hali ma'lumot kutilayotgan eng eski yutuq."""
    return await session.scalar(
        select(Winner)
        .where(Winner.user_id == user_id, Winner.status == WinnerStatus.AWAITING_INFO)
        .order_by(Winner.id)
        .limit(1)
    )


async def open_payouts(session: AsyncSession) -> list[Winner]:
    return list(
        (
            await session.scalars(
                select(Winner)
                .where(Winner.status.in_([WinnerStatus.AWAITING_INFO, WinnerStatus.INFO_RECEIVED]))
                .order_by(Winner.status.desc(), Winner.id)
            )
        ).all()
    )


def mark_done(winner: Winner) -> None:
    """Yutuq topshirildi: shaxsiy ma'lumotlar tozalanadi (karta faqat maskalangan holda qoladi)."""
    winner.status = WinnerStatus.DONE
    winner.done_at = utcnow()
    winner.card_enc = winner.card_holder_enc = None
    winner.full_name_enc = winner.phone_enc = winner.address_enc = None


async def cancel_giveaway(session: AsyncSession, giveaway_id: int) -> Giveaway | None:
    """Faol yoki g'olib aniqlanayotgan (hali e'lon qilinmagan) rozigrishni bekor qiladi."""
    g = await session.get(Giveaway, giveaway_id)
    if g is None or g.status not in (GiveawayStatus.ACTIVE, GiveawayStatus.DRAWING):
        return None
    g.status = GiveawayStatus.CANCELLED
    await session.commit()
    return g


async def list_giveaways(session: AsyncSession, status: GiveawayStatus | None = None) -> list[Giveaway]:
    q = select(Giveaway).order_by(Giveaway.id.desc())
    if status:
        q = q.where(Giveaway.status == status)
    return list((await session.scalars(q)).all())


async def participant_counts(session: AsyncSession) -> dict[int, int]:
    rows = await session.execute(select(Participant.giveaway_id, func.count()).group_by(Participant.giveaway_id))
    return dict(rows.all())


async def list_winners(session: AsyncSession, giveaway_id: int) -> list[Winner]:
    return list(
        (await session.scalars(select(Winner).where(Winner.giveaway_id == giveaway_id).order_by(Winner.place))).all()
    )


async def list_sponsors(session: AsyncSession) -> list[SponsorChannel]:
    return list((await session.scalars(select(SponsorChannel).order_by(SponsorChannel.title))).all())


# --- Jonli o'yin ---


async def list_picks(session: AsyncSession, giveaway_id: int) -> list[DrawPick]:
    return list(
        (await session.scalars(select(DrawPick).where(DrawPick.giveaway_id == giveaway_id).order_by(DrawPick.id))).all()
    )


async def subscription_misses(session: AsyncSession, giveaway_id: int) -> dict[int, list[str]]:
    """participant_id -> obuna bo'lmagan kanallar nomi."""
    rows = await session.scalars(select(SubscriptionMiss).where(SubscriptionMiss.giveaway_id == giveaway_id))
    return {m.participant_id: m.chats for m in rows}


async def save_misses(session: AsyncSession, giveaway_id: int, misses: dict[int, list[str]]) -> None:
    """Tekshiruv natijasi bilan almashtiradi (qayta obuna bo'lganlar ro'yxatdan chiqadi)."""
    await session.execute(delete(SubscriptionMiss).where(SubscriptionMiss.giveaway_id == giveaway_id))
    session.add_all(SubscriptionMiss(participant_id=pid, giveaway_id=giveaway_id, chats=chats) for pid, chats in misses.items())


async def set_miss(session: AsyncSession, participant: Participant, chats: list[str]) -> None:
    """Bitta ishtirokchining obuna holatini yangilaydi («Qatnashish» qayta bosilganda). chats=[] — hammasiga obuna."""
    row = await session.get(SubscriptionMiss, participant.id)
    if chats and row:
        row.chats, row.checked_at = chats, utcnow()
    elif chats:
        session.add(SubscriptionMiss(participant_id=participant.id, giveaway_id=participant.giveaway_id, chats=chats))
    elif row:
        await session.delete(row)
    await session.commit()


async def next_candidate(session: AsyncSession, g: Giveaway, picks: list[DrawPick]) -> Participant | None:
    """Random tartibida hali chiqmagan birinchi ishtirokchi (draw.rank — qotirilgan ro'yxat bo'yicha).

    Oldindan tekshiruvda obunasi yo'q chiqqanlar o'tkaziladi.
    """
    picked = {p.participant_id for p in picks} | (await subscription_misses(session, g.id)).keys()
    by_number = {p.number: p for p in await list_participants(session, g.id)}
    for number in draw.rank(g.seed, g.list_hash or "", by_number):
        if by_number[number].id not in picked:
            return by_number[number]
    return None
