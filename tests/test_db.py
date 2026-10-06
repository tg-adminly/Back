import sqlite3

from tgagent.core.db import init_db, make_engine


async def test_init_db_adds_new_columns_to_old_tables(tmp_path):
    """Eski bazada yangi ustun (auto_draw) yo'q — ishga tushganda qo'shiladi, eski qatorlar default oladi."""
    path = tmp_path / "old.db"
    engine = make_engine(f"sqlite+aiosqlite:///{path}")
    await init_db(engine)
    await engine.dispose()
    with sqlite3.connect(path) as c:
        c.execute("ALTER TABLE giveaways DROP COLUMN auto_draw")
        c.execute(
            "INSERT INTO giveaways (title, description, prizes_data, ends_at, status, seed, commit_hash, chat_id, created_at)"
            " VALUES ('a', 'b', '[]', '2026-01-01', 'active', 's', 'c', -100, '2026-01-01')"
        )

    engine = make_engine(f"sqlite+aiosqlite:///{path}")
    await init_db(engine)
    await init_db(engine)  # ikkinchi marta — o'zgarish yo'q
    await engine.dispose()
    with sqlite3.connect(path) as c:
        assert c.execute("SELECT auto_draw FROM giveaways").fetchall() == [(0,)]
