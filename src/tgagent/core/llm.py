"""LLM qatlami: provider almashtiriladigan, har so'rov narxi hisoblanadi, oylik limit bilan.

Hozir OpenAI. Agentlar faqat `LLM.complete` ni chaqiradi — provider tafsilotlari shu yerda qoladi.
"""

import base64
import json
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import String, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column

from tgagent.config import Settings
from tgagent.core.db import Base, UTCDateTime, utcnow

log = logging.getLogger(__name__)

NO_KEY = "AI ulanmagan: .env faylida OPENAI_API_KEY kiritilmagan."
LIMIT_REACHED = "Bu oylik AI limiti (${limit:.2f}) tugadi. Limitni .env dagi LLM_MONTHLY_LIMIT da oshirish mumkin."
FAILED = "AI javob bermadi, birozdan keyin qayta urinib ko'ring."


class LlmError(Exception):
    """Foydalanuvchiga ko'rsatsa bo'ladigan xato (o'zbekcha)."""


class LlmUsage(Base):
    """Har bir AI so'rovi: nima uchun, qancha token, qancha dollar."""

    __tablename__ = "llm_usage"

    id: Mapped[int] = mapped_column(primary_key=True)
    at: Mapped[datetime] = mapped_column(UTCDateTime, default=utcnow, index=True)
    purpose: Mapped[str] = mapped_column(String(64))
    model: Mapped[str] = mapped_column(String(64))
    tokens_in: Mapped[int]
    tokens_out: Mapped[int]
    cost_usd: Mapped[float]


@dataclass
class Image:
    data: bytes
    mime: str = "image/jpeg"


@dataclass
class Msg:
    role: str  # system / user / assistant
    text: str
    images: list[Image] = field(default_factory=list)


@dataclass
class Completion:
    text: str
    tokens_in: int
    tokens_out: int


# Provider: xabarlar → javob matni va tokenlar. Testlarda soxtasi beriladi.
Provider = Callable[[list[Msg], dict | None], Awaitable[Completion]]


def month_start(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class LLM:
    def __init__(self, settings: Settings, sm: async_sessionmaker, provider: Provider | None = None,
                 on_limit: Callable[[], Awaitable[None]] | None = None):
        self.settings = settings
        self.sm = sm
        self.provider = provider or (_openai_provider(settings) if settings.openai_api_key else None)
        self.on_limit = on_limit  # limit tugaganda bir marta (egasiga xabar)
        self._limit_notified: datetime | None = None

    @property
    def enabled(self) -> bool:
        return self.provider is not None

    async def month_cost(self) -> float:
        async with self.sm() as s:
            total = await s.scalar(select(func.sum(LlmUsage.cost_usd)).where(LlmUsage.at >= month_start(utcnow())))
        return float(total or 0)

    async def complete(self, messages: list[Msg], *, purpose: str, schema: dict | None = None) -> str:
        """Javob matni. `schema` berilsa — shu JSON sxemasiga mos JSON qaytadi."""
        if self.provider is None:
            raise LlmError(NO_KEY)
        limit = self.settings.llm_monthly_limit
        if await self.month_cost() >= limit:
            await self._notify_limit()
            raise LlmError(LIMIT_REACHED.format(limit=limit))
        try:
            res = await self.provider(messages, schema)
        except LlmError:
            raise
        except Exception:
            log.exception("LLM so'rovi xato (%s)", purpose)
            raise LlmError(FAILED) from None
        cost = (res.tokens_in * self.settings.llm_price_in + res.tokens_out * self.settings.llm_price_out) / 1_000_000
        async with self.sm() as s:
            s.add(LlmUsage(purpose=purpose, model=self.settings.llm_model, tokens_in=res.tokens_in,
                           tokens_out=res.tokens_out, cost_usd=cost))
            await s.commit()
        log.info("LLM %s: %d+%d token, $%.4f", purpose, res.tokens_in, res.tokens_out, cost)
        return res.text

    async def complete_json(self, messages: list[Msg], *, purpose: str, schema: dict) -> dict:
        text = await self.complete(messages, purpose=purpose, schema=schema)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            log.error("LLM JSON emas (%s): %.300s", purpose, text)
            raise LlmError(FAILED) from None

    async def _notify_limit(self) -> None:
        month = month_start(utcnow())
        if self.on_limit and self._limit_notified != month:
            self._limit_notified = month
            try:
                await self.on_limit()
            except Exception:
                log.exception("Limit haqida xabar yuborilmadi")


def _openai_provider(settings: Settings) -> Provider:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=120)

    def part(m: Msg) -> str | list[dict]:
        if not m.images:
            return m.text
        parts: list[dict] = [{"type": "text", "text": m.text}]
        for img in m.images:
            url = f"data:{img.mime};base64,{base64.b64encode(img.data).decode()}"
            # low — rasm arzon (≈85 token): uslubni tushunish uchun yetadi
            parts.append({"type": "image_url", "image_url": {"url": url, "detail": "low"}})
        return parts

    async def call(messages: list[Msg], schema: dict | None) -> Completion:
        kwargs: dict = {}
        if schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "answer", "schema": schema, "strict": True},
            }
        if settings.llm_reasoning:
            kwargs["reasoning_effort"] = settings.llm_reasoning
        r = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": m.role, "content": part(m)} for m in messages],
            **kwargs,
        )
        usage = r.usage
        return Completion(r.choices[0].message.content or "", usage.prompt_tokens if usage else 0,
                          usage.completion_tokens if usage else 0)

    return call
