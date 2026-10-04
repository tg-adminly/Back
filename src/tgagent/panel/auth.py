"""Panelga kirish: sayt kod yaratadi → egasi botda tasdiqlaydi → brauzerga sessiya cookie beriladi.

Parol yo'q, Telegram Login vidjeti ham shart emas (u domen talab qiladi).
Mini App ulanganda Telegram initData orqali kirish shu yerga qo'shiladi.
"""

import hashlib
import secrets
import time
from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgagent.config import Settings
from tgagent.core.db import utcnow
from tgagent.panel.models import PanelSession

COOKIE = "tga_session"
LOGIN_TTL = 300  # soniya
SESSION_TTL = timedelta(days=30)


@dataclass(frozen=True)
class Staff:
    user_id: int
    name: str
    role: str  # "owner" | "editor"

    @property
    def is_owner(self) -> bool:
        return self.role == "owner"


def staff_role(settings: Settings, user_id: int) -> str | None:
    if user_id in settings.owner_ids:
        return "owner"
    if user_id in settings.editor_ids:
        return "editor"
    return None


@dataclass
class LoginRequest:
    created: float
    user_id: int | None = None
    user_name: str = ""


class LoginRequests:
    """Kutilayotgan kirish so'rovlari (xotirada, 5 daqiqa yashaydi)."""

    def __init__(self):
        self._items: dict[str, LoginRequest] = {}

    def create(self) -> str:
        self._cleanup()
        token = secrets.token_urlsafe(24)
        self._items[token] = LoginRequest(created=time.monotonic())
        return token

    def get(self, token: str) -> LoginRequest | None:
        self._cleanup()
        return self._items.get(token)

    def confirm(self, token: str, user_id: int, user_name: str) -> bool:
        req = self.get(token)
        if req is None or req.user_id is not None:
            return False
        req.user_id, req.user_name = user_id, user_name
        return True

    def pop(self, token: str) -> None:
        self._items.pop(token, None)

    def _cleanup(self) -> None:
        now = time.monotonic()
        for t in [t for t, r in self._items.items() if now - r.created > LOGIN_TTL]:
            del self._items[t]


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


async def create_session(sm: async_sessionmaker, user_id: int, user_name: str) -> str:
    raw = secrets.token_urlsafe(32)
    async with sm() as s:
        s.add(
            PanelSession(
                token_hash=_hash(raw), user_id=user_id, user_name=user_name[:255], expires_at=utcnow() + SESSION_TTL
            )
        )
        await s.commit()
    return raw


async def session_staff(sm: async_sessionmaker, settings: Settings, raw: str | None) -> Staff | None:
    if not raw:
        return None
    async with sm() as s:
        ps = await s.scalar(select(PanelSession).where(PanelSession.token_hash == _hash(raw)))
    if ps is None or ps.expires_at <= utcnow():
        return None
    # Rol har safar .env dan olinadi: ID ro'yxatdan olib tashlansa, sessiya darhol ishlamay qoladi
    role = staff_role(settings, ps.user_id)
    return Staff(ps.user_id, ps.user_name, role) if role else None


async def delete_session(sm: async_sessionmaker, raw: str) -> None:
    async with sm() as s:
        await s.execute(delete(PanelSession).where(PanelSession.token_hash == _hash(raw)))
        await s.commit()
