from datetime import timedelta

import pytest

from tgagent.agents.giveaway import service
from tgagent.agents.giveaway.models import Prize, PrizeType
from tgagent.core.db import init_db, make_engine, make_sessionmaker, utcnow


@pytest.fixture
async def sm():
    engine = make_engine("sqlite+aiosqlite:///:memory:")
    await init_db(engine)
    yield make_sessionmaker(engine)
    await engine.dispose()


async def _giveaway(s, ends_in=timedelta(hours=1)):
    sponsor = await service.upsert_sponsor(s, -1001, "Homiy", "https://t.me/homiy")
    return await service.create_giveaway(
        s, title="Test", description="Sovg'a",
        prizes=[Prize(PrizeType.MONEY, amount=500000), Prize(PrizeType.ITEM, name="iPhone 15")],
        ends_at=utcnow() + ends_in, chat_id=-100, sponsor_ids=[sponsor.id],
    )


async def test_participant_numbers_are_sequential_and_unique(sm):
    async with sm() as s:
        g = await _giveaway(s)
        assert [sp.title for sp in g.sponsors] == ["Homiy"]
        assert g.winners_count == 2
        assert g.prizes[1] == Prize(PrizeType.ITEM, name="iPhone 15")
        p1, new1 = await service.add_participant(s, g.id, 10, "Ali", None)
        p2, new2 = await service.add_participant(s, g.id, 20, "Vali", "vali")
        again, new3 = await service.add_participant(s, g.id, 10, "Ali", None)
        assert (p1.number, p2.number, again.number) == (1, 2, 1)
        assert (new1, new2, new3) == (True, True, False)
        assert await service.participants_count(s, g.id) == 2


async def test_due_giveaways(sm):
    async with sm() as s:
        future = await _giveaway(s)
        past = await _giveaway(s, ends_in=timedelta(seconds=-1))
        assert await service.due_giveaway_ids(s) == [past.id]
        assert future.ends_at.tzinfo is not None
