from datetime import datetime

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from tgagent.core.db import Base, UTCDateTime, utcnow


class BotChat(Base):
    """Bot admin bo'lgan kanal/guruh. my_chat_member yangilanishlaridan yig'iladi —
    yopiq kanalni ID'siz tanlash uchun (Bot API +taklif linkidan kanalni topa olmaydi)."""

    __tablename__ = "bot_chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    title: Mapped[str] = mapped_column(String(255))
    username: Mapped[str | None] = mapped_column(String(64))
    updated_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow, onupdate=utcnow)
