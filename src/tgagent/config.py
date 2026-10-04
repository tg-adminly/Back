from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: str
    owner_ids: Annotated[list[int], NoDecode]
    editor_ids: Annotated[list[int], NoDecode] = []
    main_chat_id: int
    fernet_key: str
    database_url: str = "sqlite+aiosqlite:///data/bot.db"
    timezone: str = "Asia/Tashkent"

    # Veb-panel. Tashqaridan faqat HTTPS reverse-proxy (Caddy) orqali ochiladi
    panel_host: str = "127.0.0.1"
    panel_port: int = 8080
    panel_url: str = "http://localhost:8080"  # botdagi havolalar uchun; domen ulangach https://...

    # Keyingi bosqichlar uchun
    openai_api_key: str | None = None
    tg_api_id: int | None = None
    tg_api_hash: str | None = None

    @field_validator("owner_ids", "editor_ids", mode="before")
    @classmethod
    def _split_ids(cls, v: object) -> object:
        if isinstance(v, str):
            return [int(x) for x in v.replace(" ", "").split(",") if x]
        return v

    @field_validator("openai_api_key", "tg_api_hash", "tg_api_id", mode="before")
    @classmethod
    def _empty_to_none(cls, v: object) -> object:
        return None if v == "" else v

    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.timezone)
