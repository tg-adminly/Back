from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import DateTime, TypeDecorator, inspect
from sqlalchemy.engine import Connection
from sqlalchemy.schema import CreateColumn
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UTCDateTime(TypeDecorator):
    """Bazada naive UTC saqlaydi, har doim aware UTC qaytaradi (SQLite tz saqlamaydi)."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("naive datetime saqlanmaydi")
        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(self, value: datetime | None, dialect):
        return None if value is None else value.replace(tzinfo=UTC)


def utcnow() -> datetime:
    return datetime.now(UTC)


def make_engine(url: str) -> AsyncEngine:
    if url.startswith("sqlite") and ":///" in url:
        path = url.split(":///", 1)[1]
        if path and path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
    return create_async_engine(url)


def make_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)


async def init_db(engine: AsyncEngine) -> None:
    # Modellar Base.metadata ga ro'yxatdan o'tishi uchun import qilinadi
    import tgagent.agents.content.models  # noqa: F401
    import tgagent.agents.giveaway.models  # noqa: F401
    import tgagent.channels.telegram_bot.models  # noqa: F401
    import tgagent.core.llm  # noqa: F401
    import tgagent.panel.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_add_missing_columns)


def _add_missing_columns(conn: Connection) -> None:
    """create_all mavjud jadvalga yangi ustun qo'shmaydi — shuni to'ldiradi (Alembic kelguncha).

    Faqat server_default'li yoki NULL bo'la oladigan ustunlar (eski qatorlar uchun qiymat bo'lishi kerak).
    """
    insp = inspect(conn)
    for table in Base.metadata.sorted_tables:
        if not insp.has_table(table.name):
            continue
        existing = {c["name"] for c in insp.get_columns(table.name)}
        for col in table.columns:
            if col.name in existing:
                continue
            if col.server_default is None and not col.nullable:
                raise RuntimeError(f"{table.name}.{col.name}: server_default kerak (eski qatorlar uchun)")
            ddl = CreateColumn(col).compile(dialect=conn.dialect)
            conn.exec_driver_sql(f"ALTER TABLE {table.name} ADD COLUMN {ddl}")
