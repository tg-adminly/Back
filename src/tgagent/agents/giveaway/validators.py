import re
from datetime import datetime
from zoneinfo import ZoneInfo

from tgagent.agents.giveaway.models import Prize, PrizeType


def _digits(text: str) -> str:
    return re.sub(r"\D", "", text)


def normalize_card(text: str) -> str | None:
    """16 xonali karta raqami (Uzcard, Humo, Visa...). Bo'shliq/chiziqchalar olib tashlanadi."""
    if re.search(r"[^\d\s-]", text.strip()):
        return None
    digits = _digits(text)
    return digits if len(digits) == 16 else None


def normalize_phone(text: str) -> str | None:
    """O'zbekiston raqami → +998XXXXXXXXX."""
    digits = _digits(text)
    if len(digits) == 9:
        digits = "998" + digits
    if len(digits) == 12 and digits.startswith("998"):
        return "+" + digits
    return None


def parse_amount(text: str) -> int | None:
    digits = _digits(text)
    if not digits or len(digits) > 12 or re.search(r"[^\d\s.,']", text.strip()):
        return None
    value = int(digits)
    return value if value > 0 else None


_MULTIPLIERS = {"ming": 1_000, "k": 1_000, "mln": 1_000_000, "million": 1_000_000}
_CURRENCY = re.compile(r"\s*(so['‘’`]?m|sum|сум)\s*$", re.IGNORECASE)


def parse_prize(text: str) -> Prize | None:
    """Raqam bo'lsa — pul ("500000", "500 000 so'm", "500 ming", "1.5 mln"), aks holda buyum nomi."""
    text = text.strip()
    if not text:
        return None
    bare = _CURRENCY.sub("", text)
    m = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*(ming|k|mln|million)", bare, re.IGNORECASE)
    if m:
        amount = int(float(m.group(1).replace(",", ".")) * _MULTIPLIERS[m.group(2).lower()])
        return Prize(PrizeType.MONEY, amount=amount) if amount > 0 else None
    amount = parse_amount(bare)
    if amount is not None:
        return Prize(PrizeType.MONEY, amount=amount)
    if re.fullmatch(r"[\d\s.,']+", bare):
        return None  # "0" kabi — na summa, na nom
    return Prize(PrizeType.ITEM, name=text[:255])


def parse_local_datetime(text: str, tz: ZoneInfo) -> datetime | None:
    """"dd.mm.yyyy HH:MM" (mahalliy vaqt) → aware datetime."""
    try:
        naive = datetime.strptime(text.strip(), "%d.%m.%Y %H:%M")
    except ValueError:
        return None
    return naive.replace(tzinfo=tz)
