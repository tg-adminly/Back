from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sqlalchemy import JSON, BigInteger, Column, ForeignKey, String, Table, Text, UniqueConstraint, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tgagent.core.db import Base, UTCDateTime, utcnow


class GiveawayStatus(StrEnum):
    ACTIVE = "active"
    DRAWING = "drawing"  # qatnashish yopildi, g'oliblar aniqlanmoqda (jonli o'yin yoki avtomatik)
    FINISHED = "finished"
    CANCELLED = "cancelled"


class PrizeType(StrEnum):
    MONEY = "money"
    ITEM = "item"


@dataclass(frozen=True)
class Prize:
    """Bitta o'rin sovrini: pul (kartaga) yoki buyum (BTS pochta)."""

    type: PrizeType
    amount: int | None = None  # so'm (MONEY)
    name: str | None = None  # buyum nomi (ITEM)

    def to_dict(self) -> dict:
        return {"type": self.type.value, "amount": self.amount, "name": self.name}

    @classmethod
    def from_dict(cls, d: dict) -> "Prize":
        return cls(PrizeType(d["type"]), d.get("amount"), d.get("name"))


class WinnerStatus(StrEnum):
    AWAITING_INFO = "awaiting_info"  # g'olibdan karta/manzil kutilmoqda
    INFO_RECEIVED = "info_received"  # egasi to'lashi/yuborishi kerak
    DONE = "done"  # to'landi / yuborildi


class ClaimStep(StrEnum):
    CARD = "card"
    CARD_HOLDER = "card_holder"
    FULL_NAME = "full_name"
    PHONE = "phone"
    ADDRESS = "address"


giveaway_sponsors = Table(
    "giveaway_sponsors",
    Base.metadata,
    Column("giveaway_id", ForeignKey("giveaways.id", ondelete="CASCADE"), primary_key=True),
    Column("sponsor_id", ForeignKey("sponsor_channels.id", ondelete="CASCADE"), primary_key=True),
)


class SponsorChannel(Base):
    """Homiy kanal. Bot u yerda admin bo'lishi shart (obunani tekshirish uchun)."""

    __tablename__ = "sponsor_channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    title: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)


class Giveaway(Base):
    __tablename__ = "giveaways"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    # O'rinlar bo'yicha sovrinlar: prizes_data[0] — 1-o'rin. G'oliblar soni = len(prizes)
    prizes_data: Mapped[list[dict]] = mapped_column(JSON)
    ends_at: Mapped[datetime] = mapped_column(UTCDateTime)
    status: Mapped[GiveawayStatus] = mapped_column(String(16), default=GiveawayStatus.ACTIVE)
    # True — vaqti kelganda bot g'oliblarni o'zi aniqlab kanalga tashlaydi.
    # False — vaqt faqat eslatma: egasi/muharrir panelda jonli o'yin o'tkazadi
    auto_draw: Mapped[bool] = mapped_column(default=False, server_default=false())
    # Jonli rejim: vaqti kelganda egasi/muharrirga eslatma yuborilgan payt (vaqt o'zgarsa — qayta yuboriladi)
    reminded_at: Mapped[datetime | None] = mapped_column(UTCDateTime)

    # Random manbasi (draw.rank). Hech qayerda e'lon qilinmaydi
    seed: Mapped[str] = mapped_column(String(64))
    commit_hash: Mapped[str] = mapped_column(String(64))
    list_hash: Mapped[str | None] = mapped_column(String(64))

    chat_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    sponsors: Mapped[list[SponsorChannel]] = relationship(secondary=giveaway_sponsors, lazy="selectin")

    @property
    def prizes(self) -> list[Prize]:
        return [Prize.from_dict(d) for d in self.prizes_data]

    @property
    def winners_count(self) -> int:
        return len(self.prizes_data)


class Participant(Base):
    __tablename__ = "participants"
    __table_args__ = (
        UniqueConstraint("giveaway_id", "user_id"),
        UniqueConstraint("giveaway_id", "number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    giveaway_id: Mapped[int] = mapped_column(ForeignKey("giveaways.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    number: Mapped[int]
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str | None] = mapped_column(String(64))
    joined_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)


class Winner(Base):
    __tablename__ = "winners"

    id: Mapped[int] = mapped_column(primary_key=True)
    giveaway_id: Mapped[int] = mapped_column(ForeignKey("giveaways.id", ondelete="CASCADE"), index=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    place: Mapped[int]
    # O'rin sovrini g'olib yozilgan paytdagi holatida saqlanadi
    prize_type: Mapped[PrizeType] = mapped_column(String(16))
    prize_amount: Mapped[int | None]
    prize_name: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[WinnerStatus] = mapped_column(String(16), default=WinnerStatus.AWAITING_INFO)
    claim_step: Mapped[ClaimStep | None] = mapped_column(String(16))

    # Shifrlangan (Vault). Yutuq topshirilgach tozalanadi.
    card_enc: Mapped[str | None] = mapped_column(Text)
    card_holder_enc: Mapped[str | None] = mapped_column(Text)
    full_name_enc: Mapped[str | None] = mapped_column(Text)
    phone_enc: Mapped[str | None] = mapped_column(Text)
    address_enc: Mapped[str | None] = mapped_column(Text)
    card_masked: Mapped[str | None] = mapped_column(String(32))

    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)
    done_at: Mapped[datetime | None] = mapped_column(UTCDateTime)

    giveaway: Mapped[Giveaway] = relationship(lazy="selectin")
    participant: Mapped[Participant] = relationship(lazy="selectin")

    @property
    def prize(self) -> Prize:
        return Prize(PrizeType(self.prize_type), self.prize_amount, self.prize_name)


class DrawPick(Base):
    """Jonli o'yinda random chiqargan ishtirokchi: g'olib (place) yoki obunadan chiqqani uchun o'tkazilgan (None).

    Winner yozuvlari faqat natija guruhga e'lon qilinganda yaratiladi — undan oldin g'olib botga yoza olmaydi.
    """

    __tablename__ = "draw_picks"
    __table_args__ = (UniqueConstraint("giveaway_id", "participant_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    giveaway_id: Mapped[int] = mapped_column(ForeignKey("giveaways.id", ondelete="CASCADE"), index=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id", ondelete="CASCADE"))
    place: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)

    participant: Mapped[Participant] = relationship(lazy="selectin")


class SubscriptionMiss(Base):
    """Ishtirokchi qaysi kanal(lar)ga obuna emasligi (qatnashgandan keyin chiqib ketgan).

    Jonli o'yindan oldingi tekshiruv yoki o'yinda o'tkazib yuborilganda yoziladi.
    Shu yerda turgan ishtirokchi randomga tushmaydi.
    """

    __tablename__ = "subscription_misses"

    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id", ondelete="CASCADE"), primary_key=True)
    giveaway_id: Mapped[int] = mapped_column(ForeignKey("giveaways.id", ondelete="CASCADE"), index=True)
    chats: Mapped[list[str]] = mapped_column(JSON)  # kanal nomlari
    checked_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)
