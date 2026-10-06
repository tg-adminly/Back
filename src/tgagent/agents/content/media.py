"""Yuklangan rasmlar: diskda (media_dir), JPEG ga keltirilib, kichraytirib saqlanadi."""

import io
import re
import uuid
from pathlib import Path

from PIL import Image, UnidentifiedImageError

MAX_BYTES = 10 * 1024 * 1024
MAX_SIDE = 1280
_NAME = re.compile(r"^[0-9a-f]{32}\.jpg$")


class BadImage(ValueError):
    pass


def save_image(media_dir: str, data: bytes) -> str:
    if len(data) > MAX_BYTES:
        raise BadImage("Rasm 10 MB dan katta.")
    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except (UnidentifiedImageError, OSError):
        raise BadImage("Bu rasm emas yoki fayl buzilgan.") from None
    img = img.convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    name = f"{uuid.uuid4().hex}.jpg"
    path = Path(media_dir)
    path.mkdir(parents=True, exist_ok=True)
    img.save(path / name, "JPEG", quality=85)
    return name


def image_path(media_dir: str, name: str) -> Path | None:
    if not _NAME.match(name):
        return None
    p = Path(media_dir) / name
    return p if p.is_file() else None


def read_image(media_dir: str, name: str) -> bytes | None:
    p = image_path(media_dir, name)
    return p.read_bytes() if p else None


def delete_image(media_dir: str, name: str | None) -> None:
    if name and (p := image_path(media_dir, name)):
        p.unlink(missing_ok=True)
