import io
import json
from types import SimpleNamespace

import httpx
import pytest
from cryptography.fernet import Fernet
from PIL import Image as PILImage
from test_panel import EDITOR, OWNER, FakeBot, H, login

from tgagent.channels.telegram_bot.chats import ChatRef
from tgagent.config import Settings
from tgagent.core.crypto import Vault
from tgagent.core.db import init_db, make_engine, make_sessionmaker
from tgagent.core.llm import LLM, Completion
from tgagent.panel.api import Deps
from tgagent.panel.auth import LoginRequests
from tgagent.panel.server import create_app


class FakeAI:
    """OpenAI o'rniga: so'rovlarni eslab qoladi, berilgan javobni qaytaradi."""

    def __init__(self):
        self.calls = []
        self.answer = {"reply": "Tushunarli!", "samples": [], "guide": None, "guide_note": None}

    async def __call__(self, messages, schema):
        self.calls.append(messages)
        return Completion(json.dumps(self.answer), tokens_in=1000, tokens_out=500)


@pytest.fixture
async def env(tmp_path):
    engine = make_engine("sqlite+aiosqlite:///:memory:")
    await init_db(engine)
    sm = make_sessionmaker(engine)
    settings = Settings(
        _env_file=None, bot_token="x", owner_ids=[OWNER], editor_ids=[EDITOR], main_chat_id=-100,
        fernet_key=Fernet.generate_key().decode(), media_dir=str(tmp_path / "media"), llm_monthly_limit=1.0,
    )
    ai = FakeAI()
    limit_hits = []

    async def on_limit():
        limit_hits.append(1)

    llm = LLM(settings, sm, provider=ai, on_limit=on_limit)
    app = create_app(Deps(settings, FakeBot(), sm, Vault(settings.fernet_key), ChatRef(-100, "Kanal", "https://t.me/kanal"),
                          LoginRequests(), llm), dist=tmp_path)
    client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")
    yield SimpleNamespace(client=client, logins=app.state.deps.logins, ai=ai, llm=llm, limit_hits=limit_hits)
    await client.aclose()
    await engine.dispose()


def jpeg(size=(2000, 1000)) -> bytes:
    buf = io.BytesIO()
    PILImage.new("RGB", size, "pink").save(buf, "PNG")
    return buf.getvalue()


async def test_training_chat_flow(env):
    await login(env, EDITOR)  # muharrir ham o'qitadi
    c = env.client

    # Namunalar yig'iladi, agent hali javob bermaydi
    r = await c.post("/api/content/chat/sample", data={"text": "Bahor keldi 🌸", "source_name": "@boshqa"},
                     files={"image": ("a.png", jpeg(), "image/png")}, headers=H)
    assert r.status_code == 200, r.text
    first = r.json()["sample"]
    await c.post("/api/content/chat/sample", data={"text": "Ikkinchi post"}, headers=H)
    assert (await c.post("/api/content/chat/sample", data={"text": " "}, headers=H)).status_code == 400
    assert (await c.get("/api/content/chat")).json()["pending_samples"] == 2
    assert env.ai.calls == []

    # Rasm kichraytirib saqlangan va faqat xodimga ochiq
    img = await c.get(first["image"])
    assert img.status_code == 200 and max(PILImage.open(io.BytesIO(img.content)).size) == 1280
    assert (await c.get("/api/content/media/..%2F..%2Fsecret")).status_code == 404

    # «Tahlil qilish»: agent namunalarni rasmi bilan ko'radi va qo'llanma taklif qiladi
    env.ai.answer = {
        "reply": "Ikkala post ham qisqa va iliq.",
        "samples": [{"id": first["id"], "image_desc": "Pushti fon", "analysis": "Qisqa, emoji bilan."}],
        "guide": "Ohang:\n- iliq, qisqa", "guide_note": "Ohang qo'shildi",
    }
    r = await c.post("/api/content/chat/message", json={"text": ""}, headers=H)
    assert r.status_code == 200, r.text
    reply = r.json()
    assert reply["proposal_status"] == "pending" and reply["proposal_note"] == "Ohang qo'shildi"
    sent = env.ai.calls[-1]
    assert sum(len(m.images) for m in sent) == 1
    assert "@boshqa" in "\n".join(m.text for m in sent)

    chat = (await c.get("/api/content/chat")).json()
    assert chat["pending_samples"] == 0
    analysed = next(m["sample"] for m in chat["messages"] if m["sample"] and m["sample"]["id"] == first["id"])
    assert analysed["image_desc"] == "Pushti fon"

    # Qo'llanma faqat tasdiqlangandan keyin o'zgaradi; xodim tuzatib qabul qilishi mumkin
    assert (await c.get("/api/content/guide")).json()["current"] is None
    r = await c.post(f"/api/content/chat/{reply['id']}/decide", json={"accept": True, "text": "Ohang:\n- iliq"},
                     headers=H)
    assert r.json()["guide"]["text"] == "Ohang:\n- iliq"
    assert (await c.post(f"/api/content/chat/{reply['id']}/decide", json={"accept": False}, headers=H)).status_code == 409

    # Keyingi suhbatda agent joriy qo'llanmani ko'radi
    env.ai.answer = {"reply": "Xo'p", "samples": [], "guide": None, "guide_note": None}
    await c.post("/api/content/chat/message", json={"text": "Kamroq emoji ishlat"}, headers=H)
    assert "Ohang:\n- iliq" in "\n".join(m.text for m in env.ai.calls[-1])

    # Qo'lda tahrir va eski versiyaga qaytarish
    await c.put("/api/content/guide", json={"text": "Yangi qoida"}, headers=H)
    guide = (await c.get("/api/content/guide")).json()
    assert guide["current"]["text"] == "Yangi qoida" and len(guide["versions"]) == 2
    old = guide["versions"][1]["id"]
    await c.post(f"/api/content/guide/{old}/restore", headers=H)
    assert (await c.get("/api/content/guide")).json()["current"]["text"] == "Ohang:\n- iliq"

    # Namunani o'chirish — chatda «o'chirilgan» bo'lib qoladi
    assert (await c.delete(f"/api/content/samples/{first['id']}", headers=H)).status_code == 200
    assert (await c.get(first["image"])).status_code == 404
    msgs = (await c.get("/api/content/chat")).json()["messages"]
    assert msgs[0]["sample_deleted"] is True


async def test_new_proposal_supersedes_old(env):
    await login(env)
    env.ai.answer = {"reply": "a", "samples": [], "guide": "v1", "guide_note": "1"}
    one = (await env.client.post("/api/content/chat/message", json={"text": "x"}, headers=H)).json()
    env.ai.answer = {"reply": "b", "samples": [], "guide": "v2", "guide_note": "2"}
    await env.client.post("/api/content/chat/message", json={"text": "y"}, headers=H)
    msgs = {m["id"]: m for m in (await env.client.get("/api/content/chat")).json()["messages"]}
    assert msgs[one["id"]]["proposal_status"] == "superseded"


async def test_monthly_limit_stops_ai(env):
    await login(env)
    # Har so'rov: 1000*0.25 + 500*2.0 = $0.00125; limit $1 → narxni sun'iy oshiramiz
    env.llm.settings.llm_price_out = 1_000_000.0
    assert (await env.client.post("/api/content/chat/message", json={"text": "salom"}, headers=H)).status_code == 200
    usage = (await env.client.get("/api/content/usage")).json()
    assert usage["month_cost"] >= usage["limit"] and usage["enabled"]
    r = await env.client.post("/api/content/chat/message", json={"text": "yana"}, headers=H)
    assert r.status_code == 503 and "limiti" in r.json()["detail"]
    await env.client.post("/api/content/chat/message", json={"text": "yana"}, headers=H)
    assert env.limit_hits == [1]  # egasiga bir marta xabar
