from datetime import datetime
from enum import StrEnum

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tgagent.core.db import Base, UTCDateTime, utcnow


class StyleGuide(Base):
    """Uslub qo'llanma versiyasi. Joriysi — eng oxirgisi; eskilari tarix (qaytarish mumkin)."""

    __tablename__ = "style_guides"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    note: Mapped[str | None] = mapped_column(String(500))  # nima o'zgardi
    author: Mapped[str] = mapped_column(String(255))  # "AI" yoki xodim ismi
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)


class SampleSource(StrEnum):
    OWN = "own"  # o'z kanalimiz
    OTHER = "other"  # boshqa kanal


class Sample(Base):
    """O'qitish uchun post: matn + rasm (ixtiyoriy) + agentning tahlili."""

    __tablename__ = "content_samples"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[SampleSource] = mapped_column(String(16))
    source_name: Mapped[str | None] = mapped_column(String(255))  # kanal nomi/linki
    text: Mapped[str] = mapped_column(Text, default="")
    image: Mapped[str | None] = mapped_column(String(64))  # media_dir ichidagi fayl nomi
    image_note: Mapped[str | None] = mapped_column(Text)  # xodim yozgan rasm tavsifi
    analysis: Mapped[str | None] = mapped_column(Text)  # agent tahlili; None — hali tahlil qilinmagan
    image_desc: Mapped[str | None] = mapped_column(Text)  # agent rasmda nimani ko'rdi
    # Telegram'dan kelgan bo'lsa (takror qo'shilmasin)
    chat_id: Mapped[int | None] = mapped_column(BigInteger)
    message_id: Mapped[int | None]
    added_by: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)


class ProposalStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"  # keyinroq yangi taklif keldi


class TrainMessage(Base):
    """O'qitish chati xabari. Xodim xabari, namuna post yoki agent javobi (qo'llanma taklifi bilan)."""

    __tablename__ = "content_train_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(16))  # user / assistant
    author: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text, default="")
    sample_id: Mapped[int | None] = mapped_column(ForeignKey("content_samples.id", ondelete="SET NULL"))
    sample: Mapped[Sample | None] = relationship(lazy="selectin")
    # Agent taklifi: qo'llanmaning to'liq yangi matni + qisqacha nima o'zgardi
    proposal: Mapped[str | None] = mapped_column(Text)
    proposal_note: Mapped[str | None] = mapped_column(String(500))
    proposal_status: Mapped[ProposalStatus | None] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow)
