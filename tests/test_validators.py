from zoneinfo import ZoneInfo

from tgagent.agents.giveaway.validators import normalize_card, normalize_phone, parse_amount, parse_local_datetime
from tgagent.core.crypto import Vault, mask_card


def test_card():
    assert normalize_card("8600 1234 5678 9012") == "8600123456789012"
    assert normalize_card("8600-1234-5678-9012") == "8600123456789012"
    assert normalize_card("8600 1234") is None
    assert normalize_card("karta 8600123456789012") is None


def test_phone():
    assert normalize_phone("+998 90 123 45 67") == "+998901234567"
    assert normalize_phone("901234567") == "+998901234567"
    assert normalize_phone("12345") is None


def test_amount():
    assert parse_amount("200 000") == 200000
    assert parse_amount("0") is None
    assert parse_amount("ikki yuz") is None


def test_datetime_is_local():
    dt = parse_local_datetime("15.10.2026 20:00", ZoneInfo("Asia/Tashkent"))
    assert dt.utcoffset().total_seconds() == 5 * 3600
    assert parse_local_datetime("2026-10-15", ZoneInfo("Asia/Tashkent")) is None


def test_vault_roundtrip():
    from cryptography.fernet import Fernet

    v = Vault(Fernet.generate_key().decode())
    token = v.encrypt("8600123456789012")
    assert token != "8600123456789012"
    assert v.decrypt(token) == "8600123456789012"
    assert mask_card("8600123456789012") == "8600 **** **** 9012"


def test_prize():
    from tgagent.agents.giveaway.models import Prize, PrizeType
    from tgagent.agents.giveaway.validators import parse_prize

    assert parse_prize("500 000 so'm") == Prize(PrizeType.MONEY, amount=500000)
    assert parse_prize("500 ming") == Prize(PrizeType.MONEY, amount=500000)
    assert parse_prize("1.5 mln") == Prize(PrizeType.MONEY, amount=1500000)
    assert parse_prize("iPhone 15") == Prize(PrizeType.ITEM, name="iPhone 15")
    assert parse_prize("0") is None


def test_prizes_block_groups_equal_places():
    from tgagent.agents.giveaway.models import Prize, PrizeType
    from tgagent.agents.giveaway.texts import prizes_block

    phone, cash = Prize(PrizeType.ITEM, name="iPhone"), Prize(PrizeType.MONEY, amount=100000)
    lines = prizes_block([phone, cash, cash, cash])
    assert lines == ["🥇 1-o'rin: <b>iPhone</b>", "🏅 2–4-o'rinlar: <b>100 000 so'm</b> (har biriga)"]
