from cryptography.fernet import Fernet


class Vault:
    """Shaxsiy ma'lumotlarni (karta, telefon, manzil) shifrlash."""

    def __init__(self, key: str):
        self._fernet = Fernet(key.encode())

    def encrypt(self, value: str | None) -> str | None:
        if value is None:
            return None
        return self._fernet.encrypt(value.encode()).decode()

    def decrypt(self, token: str | None) -> str | None:
        if token is None:
            return None
        return self._fernet.decrypt(token.encode()).decode()


def mask_card(card: str) -> str:
    return f"{card[:4]} **** **** {card[-4:]}"
