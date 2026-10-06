"""G'olib tanlash random'i. LLM yo'q, faqat sha256.

1. Rozigrish yaratilganda maxfiy `seed` yaratiladi (hech qayerda chop etilmaydi).
2. Qatnashish yopilganda ishtirokchilar ro'yxati qotiriladi: `participants_hash(entries)`.
3. Har bir raqam uchun sha256("seed:list_hash:raqam") hisoblanadi; eng kichik
   qiymatlar birinchi. Jonli o'yinda shu tartibda bittadan chiqariladi,
   obunadan chiqqanlar o'tkazib yuboriladi.
"""

import hashlib
import secrets
from collections.abc import Iterable


def new_seed() -> str:
    return secrets.token_hex(32)


def commit_of(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()


def participants_file(entries: Iterable[tuple[int, int]]) -> bytes:
    """(raqam, user_id) juftliklari → "raqam:user_id" qatorlari, raqam bo'yicha tartiblangan."""
    return "".join(f"{n}:{uid}\n" for n, uid in sorted(entries)).encode()


def participants_hash(entries: Iterable[tuple[int, int]]) -> str:
    return hashlib.sha256(participants_file(entries)).hexdigest()


def ticket_hash(seed: str, list_hash: str, number: int) -> str:
    return hashlib.sha256(f"{seed}:{list_hash}:{number}".encode()).hexdigest()


def rank(seed: str, list_hash: str, numbers: Iterable[int]) -> list[int]:
    """Raqamlarni g'oliblik tartibida qaytaradi (birinchisi — 1-o'rin nomzodi)."""
    return sorted(numbers, key=lambda n: ticket_hash(seed, list_hash, n))
