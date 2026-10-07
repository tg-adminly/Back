import asyncio
import io
import json
from types import SimpleNamespace

import httpx
import pytest
from cryptography.fernet import Fernet
from PIL import Image as PILImage
from test_panel import EDITOR, OWNER, FakeBot, H, login

from tgagent.agents.content import trainer
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
async def env(tmp_path, monkeypatch):
    monkeypatch.setattr(trainer, "responder", trainer._Responder())
    # Fayl baza: agent fonda ishlaydi, :memory: esa bitta ulanishni hamma sessiyaga bo'lib beradi
    engine = make_engine(f"sqlite+aiosqlite:///{tmp_path / 'test.db'}")
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


async def answered(env) -> dict:
    """Agent fonda javob beradi — tugashini kutib, chatni qaytaradi."""
    if trainer.responder.task:
        await trainer.responder.task
    return (await env.client.get("/api/content/chat")).json()


async def send(env, text="", *, sample=False, images=(), **form):
    files = [("images", (f"{i}.png", data, "image/png")) for i, data in enumerate(images)]
    data = {"text": text, "sample": "true" if sample else "false", **form}
    return await env.client.post("/api/content/chat/message", data=data, files=files or None, headers=H)


async def test_training_chat_flow(env):
    await login(env, EDITOR)  # muharrir ham o'qitadi
    c = env.client
    env.ai.answer = {
        "reply": "Ikkala post ham qisqa va iliq.",
        "samples": [], "guide": "Ohang:\n- iliq, qisqa", "guide_note": "Ohang qo'shildi",
    }

    # Rasmli xabar — doim namuna post (albom); agent fonda javob beradi
    r = await send(env, "Bahor keldi 🌸", images=[jpeg(), jpeg((300, 300))], source_name="@boshqa")
    assert r.status_code == 200, r.text
    first = r.json()["sample"]
    env.ai.answer["samples"] = [{"id": first["id"], "image_desc": "Pushti fon", "analysis": "Qisqa, emoji bilan."}]
    chat = await answered(env)
    assert chat["thinking"] is False and chat["error"] is None
    reply = chat["messages"][-1]
    assert reply["role"] == "assistant" and reply["proposal_status"] == "pending"
    sent = env.ai.calls[-1]
    assert sum(len(m.images) for m in sent) == 2
    assert "album of 2 photos" in "\n".join(m.text for m in sent)
    assert "@boshqa" in "\n".join(m.text for m in sent)
    assert chat["messages"][0]["sample"]["image_desc"] == "Pushti fon"

    # Rasmsiz namuna (belgilangan) va bo'sh/ortiqcha so'rovlar
    env.ai.answer = {"reply": "Ko'rdim", "samples": [], "guide": None, "guide_note": None}
    assert (await send(env, "Matnli post", sample=True)).json()["sample"]["text"] == "Matnli post"
    await answered(env)
    assert (await send(env, " ")).status_code == 400
    eleven = [jpeg((10, 10))] * 11
    assert (await send(env, images=eleven)).status_code == 400

    # Rasm kichraytirib saqlangan va faqat xodimga ochiq
    img = await c.get(first["images"][0])
    assert img.status_code == 200 and max(PILImage.open(io.BytesIO(img.content)).size) == 1280
    assert (await c.get("/api/content/media/..%2F..%2Fsecret")).status_code == 404

    # Qo'llanma faqat tasdiqlangandan keyin o'zgaradi; xodim tuzatib qabul qilishi mumkin
    assert (await c.get("/api/content/guide")).json()["current"] is None
    r = await c.post(f"/api/content/chat/{reply['id']}/decide", json={"accept": True, "text": "Ohang:\n- iliq"},
                     headers=H)
    assert r.json()["guide"]["text"] == "Ohang:\n- iliq"
    assert (await c.post(f"/api/content/chat/{reply['id']}/decide", json={"accept": False}, headers=H)).status_code == 409

    # Keyingi suhbatda agent joriy qo'llanmani ko'radi
    env.ai.answer = {"reply": "Xo'p", "samples": [], "guide": None, "guide_note": None}
    await send(env, "Kamroq emoji ishlat")
    await answered(env)
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
    assert (await c.get(first["images"][1])).status_code == 404
    msgs = (await c.get("/api/content/chat")).json()["messages"]
    assert msgs[0]["sample_deleted"] is True


async def test_messages_while_thinking_get_one_reply(env):
    """Agent o'ylayotganda yuborilgan postlar navbatga tushadi va keyingi bitta javobda birga ko'riladi."""
    await login(env)
    gate = asyncio.Event()
    real = env.ai.__call__

    async def slow(messages, schema):
        await gate.wait()
        return await real(messages, schema)

    env.llm.provider = slow
    await send(env, "1-post", sample=True)
    assert (await env.client.get("/api/content/chat")).json()["thinking"] is True
    await send(env, "2-post", sample=True)
    await send(env, "3-post", sample=True)
    gate.set()
    chat = await answered(env)
    assert len(env.ai.calls) == 2  # 1-post uchun, keyin 2- va 3-post birga
    second = "\n".join(m.text for m in env.ai.calls[1])
    assert "2-post" in second and "3-post" in second
    assert [m["role"] for m in chat["messages"]] == ["user", "user", "user", "assistant", "assistant"]


async def test_new_proposal_supersedes_old(env):
    await login(env)
    env.ai.answer = {"reply": "a", "samples": [], "guide": "v1", "guide_note": "1"}
    await send(env, "x")
    one = (await answered(env))["messages"][-1]
    env.ai.answer = {"reply": "b", "samples": [], "guide": "v2", "guide_note": "2"}
    await send(env, "y")
    msgs = {m["id"]: m for m in (await answered(env))["messages"]}
    assert msgs[one["id"]]["proposal_status"] == "superseded"


async def test_monthly_limit_stops_ai(env):
    await login(env)
    # Har so'rov: 1000*0.25 + 500*2.0 = $0.00125; limit $1 → narxni sun'iy oshiramiz
    env.llm.settings.llm_price_out = 1_000_000.0
    await send(env, "salom")
    assert (await answered(env))["error"] is None
    usage = (await env.client.get("/api/content/usage")).json()
    assert usage["month_cost"] >= usage["limit"] and usage["enabled"]
    assert (await send(env, "yana")).status_code == 200  # xabar saqlanadi, javob — xato
    chat = await answered(env)
    assert "limiti" in chat["error"] and chat["messages"][-1]["text"] == "yana"
    await env.client.post("/api/content/chat/retry", headers=H)
    assert "limiti" in (await answered(env))["error"]
    assert env.limit_hits == [1]  # egasiga bir marta xabar
