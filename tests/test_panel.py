import asyncio
from datetime import datetime, timedelta
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import httpx
import pytest
from cryptography.fernet import Fernet

from tgagent.agents.giveaway.models import Winner, WinnerStatus
from tgagent.channels.telegram_bot.chats import ChatRef
from tgagent.config import Settings
from tgagent.core.crypto import Vault
from tgagent.core.db import init_db, make_engine, make_sessionmaker
from tgagent.panel import api as panel_api
from tgagent.panel.api import Deps, sponsor_ref
from tgagent.panel.auth import LoginRequests
from tgagent.panel.server import create_app

OWNER, EDITOR = 1, 2
H = {"x-panel": "1"}


class FakeBot:
    def __init__(self):
        self.sent = []
        self.left: set[int] = set()  # kanaldan chiqib ketgan user_id lar

    async def me(self):
        return SimpleNamespace(id=999, username="test_bot")

    async def get_chat(self, ref):
        return SimpleNamespace(id=-1005, title="Homiy kanal", username="homiy", invite_link=None)

    async def get_chat_member(self, chat_id, user_id):
        return SimpleNamespace(status="left" if user_id in self.left else "administrator")

    async def send_message(self, chat_id, text, **kw):
        self.sent.append(("message", chat_id, text))
        return SimpleNamespace(message_id=len(self.sent))

    async def send_photo(self, chat_id, photo, caption=None, **kw):
        self.sent.append(("photo", chat_id, caption))


@pytest.fixture
async def env(tmp_path):
    engine = make_engine("sqlite+aiosqlite:///:memory:")
    await init_db(engine)
    sm = make_sessionmaker(engine)
    settings = Settings(
        _env_file=None, bot_token="x", owner_ids=[OWNER], editor_ids=[EDITOR], main_chat_id=-100,
        fernet_key=Fernet.generate_key().decode(),
    )
    bot, logins = FakeBot(), LoginRequests()
    vault = Vault(settings.fernet_key)
    main_chat = ChatRef(-100, "Kanal", "https://t.me/kanal")
    app = create_app(Deps(settings, bot, sm, vault, main_chat, logins), dist=tmp_path)
    client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")
    yield SimpleNamespace(client=client, bot=bot, logins=logins, sm=sm, vault=vault, settings=settings, main_chat=main_chat)
    await client.aclose()
    await engine.dispose()


async def login(env, user_id=OWNER):
    r = await env.client.post("/api/auth/start")
    token = r.json()["token"]
    assert r.json()["bot_url"] == f"https://t.me/test_bot?start=login_{token}"
    assert (await env.client.get("/api/auth/poll", params={"token": token})).json() == {"status": "pending"}
    env.logins.confirm(token, user_id, "Ega")  # botdagi «Ha, men kiryapman»
    assert (await env.client.get("/api/auth/poll", params={"token": token})).json() == {"status": "ok"}


def future(hours=2) -> str:
    return (datetime.now(ZoneInfo("Asia/Tashkent")) + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M")


async def test_requires_login_and_csrf_header(env):
    assert (await env.client.get("/api/me")).status_code == 401
    await login(env)
    assert (await env.client.get("/api/me")).json()["role"] == "owner"
    assert (await env.client.post("/api/giveaways/1/cancel")).status_code == 403  # x-panel sarlavhasisiz


async def test_editor_cannot_see_payouts(env):
    await login(env, EDITOR)
    assert (await env.client.get("/api/payouts")).status_code == 403


async def test_login_token_is_single_use(env):
    r = await env.client.post("/api/auth/start")
    token = r.json()["token"]
    assert env.logins.confirm(token, OWNER, "Ega")
    assert not env.logins.confirm(token, 777, "Boshqa")  # ikkinchi marta tasdiqlab bo'lmaydi


async def test_create_giveaway_flow(env):
    await login(env)
    sp = (await env.client.post("/api/sponsors", json={"ref": "t.me/homiy"}, headers=H)).json()
    body = {
        "title": "Kuzgi", "description": "Omad!", "prizes": ["iPhone 15", "1 mln", "0"],
        "ends_at": future(), "sponsor_ids": [sp["id"]],
    }
    preview = (await env.client.post("/api/giveaways/preview", json=body, headers=H)).json()
    assert preview["errors"] == {"prizes.2": preview["errors"]["prizes.2"]}
    assert preview["prizes"][1]["label"] == "1 000 000 so'm"

    body["prizes"][2] = "200 ming"
    r = await env.client.post("/api/giveaways", json=body, headers=H)
    assert r.status_code == 200, r.text
    gid = r.json()["id"]
    assert env.bot.sent[-1][1] == -100  # kanalga post chiqdi

    g = (await env.client.get(f"/api/giveaways/{gid}")).json()
    assert g["winners_count"] == 3 and "seed" not in g and g["post_url"] == "https://t.me/kanal/1"
    assert [x["title"] for x in g["sponsors"]] == ["Homiy kanal"]
    # Faol rozigrishdagi homiyni o'chirib bo'lmaydi
    assert (await env.client.delete(f"/api/sponsors/{sp['id']}", headers=H)).status_code == 400
    assert (await env.client.post(f"/api/giveaways/{gid}/cancel", headers=H)).json() == {"ok": True}
    assert (await env.client.delete(f"/api/sponsors/{sp['id']}", headers=H)).json() == {"ok": True}


async def test_past_end_time_rejected(env):
    await login(env)
    body = {"title": "X", "description": "Y", "prizes": ["100k"], "ends_at": future(-1)}
    r = await env.client.post("/api/giveaways", json=body, headers=H)
    assert r.status_code == 422 and "ends_at" in r.json()["detail"]["errors"]


async def test_payout_deliver(env):
    await login(env)
    body = {"title": "X", "description": "Y", "prizes": ["100k"], "ends_at": future()}
    gid = (await env.client.post("/api/giveaways", json=body, headers=H)).json()["id"]
    from tgagent.agents.giveaway import service

    async with env.sm() as s:
        p, _ = await service.add_participant(s, gid, 42, "Malika", "malika")
        w = Winner(
            giveaway_id=gid, participant_id=p.id, user_id=42, place=1, prize_type="money", prize_amount=100000,
            status=WinnerStatus.INFO_RECEIVED, card_enc=env.vault.encrypt("8600123412341234"),
            card_holder_enc=env.vault.encrypt("Malika A"), card_masked="8600 **** **** 1234",
        )
        s.add(w)
        await s.commit()

    items = (await env.client.get("/api/payouts")).json()
    assert items[0]["card_masked"] == "8600 **** **** 1234" and "card" not in items[0]
    details = (await env.client.get(f"/api/payouts/{w.id}/details")).json()
    assert details == {"card": "8600123412341234", "card_holder": "Malika A"}

    assert (await env.client.post(f"/api/payouts/{w.id}/deliver", headers=H)).status_code == 400
    r = await env.client.post(
        f"/api/payouts/{w.id}/deliver", headers=H, files={"proof": ("chek.png", b"\x89PNG", "image/png")},
        data={"note": "<b>rahmat</b>"},
    )
    assert r.json() == {"ok": True, "delivered": True}
    assert env.bot.sent[-2] == ("photo", 42, "&lt;b&gt;rahmat&lt;/b&gt;")
    assert (await env.client.get("/api/payouts")).json() == []
    async with env.sm() as s:
        assert (await s.get(Winner, w.id)).card_enc is None  # shaxsiy ma'lumot tozalandi


def test_sponsor_ref():
    assert sponsor_ref("https://t.me/homiy_kanal") == "@homiy_kanal"
    assert sponsor_ref("-1001234") == -1001234
    assert sponsor_ref("@abc") == "@abc"


async def test_bot_chats_lists_admin_channels_not_yet_sponsors(env):
    from tgagent.channels.telegram_bot import tracking

    await login(env)
    async with env.sm() as s:
        await tracking.remember_chat(s, -1005, "Homiy kanal", "homiy")
        await tracking.remember_chat(s, -1007, "Yopiq kanal", None)
        await tracking.remember_chat(s, -100, "Bizning kanal", None)  # asosiy kanal ko'rinmaydi
    r = await env.client.get("/api/bot-chats")
    assert [c["chat_id"] for c in r.json()] == [-1005, -1007]

    await env.client.post("/api/sponsors", json={"ref": "-1005"}, headers=H)
    assert [c["chat_id"] for c in (await env.client.get("/api/bot-chats")).json()] == [-1007]

    async with env.sm() as s:
        await tracking.forget_chat(s, -1007)  # bot adminlikdan olindi
    assert (await env.client.get("/api/bot-chats")).json() == []


async def test_invite_link_in_ref_gives_clear_error(env):
    await login(env)
    r = await env.client.post("/api/sponsors", json={"ref": "https://t.me/+l6U_QEwKs91jZDhi"}, headers=H)
    assert r.status_code == 400
    assert "Yopiq kanal" in r.json()["detail"]


async def test_live_draw_flow(env):
    from tgagent.agents.giveaway import jobs, service

    await login(env)
    body = {"title": "Jonli", "description": "Y", "prizes": ["300k", "200k"], "ends_at": future()}
    gid = (await env.client.post("/api/giveaways", json=body, headers=H)).json()["id"]
    async with env.sm() as s:
        for uid, name in [(11, "Ali"), (12, "Vali"), (13, "Gani"), (14, "Sobir")]:
            await service.add_participant(s, gid, uid, name, None)

    # Ochiq ro'yxat: login shart emas, faqat ism va raqam
    env.client.cookies.clear()
    pub = (await env.client.get(f"/api/public/giveaways/{gid}")).json()
    assert pub["participants"][0] == {"number": 1, "name": "Ali", "missing": []} and pub["winners"] == []
    await login(env)

    # Faol rozigrishda jonli o'yin boshlanmaydi
    assert (await env.client.post(f"/api/giveaways/{gid}/live/next", headers=H)).status_code == 400
    async with env.sm() as s:
        await service.finish_now(s, gid)
    # Sobir qatnashgandan keyin kanaldan chiqib ketgan — yopilishda qayta tekshiruv uni chiqarib tashlaydi
    env.bot.left.add(14)
    await jobs.close_participation(env.bot, env.sm, env.settings, env.main_chat, gid)
    note = env.bot.sent[-1][2]
    assert "/giveaways/%d/live" % gid in note and "1 kishi" in note  # egasiga havola va tekshiruv natijasi

    state = (await env.client.get(f"/api/giveaways/{gid}/live")).json()
    assert state["status"] == "drawing" and len(state["names"]) == 3 and state["picks"] == []
    assert state["excluded"] == [{"number": 4, "name": "Sobir", "missing": ["Kanal"]}]
    panel_api._public_cache.clear()  # ochiq sahifa 5 soniya keshlanadi
    pub = (await env.client.get(f"/api/public/giveaways/{gid}")).json()
    assert pub["participants"][3]["missing"] == ["Kanal"]

    # Qayta obuna bo'ldi — o'yindan oldin ro'yxatni yangilasa, qaytib kiradi
    env.bot.left.discard(14)
    assert (await env.client.post(f"/api/giveaways/{gid}/live/check", headers=H)).json() == {"ok": True}
    while (state := (await env.client.get(f"/api/giveaways/{gid}/live")).json())["check"]:
        await asyncio.sleep(0.01)
    assert state["excluded"] == [] and len(state["names"]) == 4 and state["check_error"] is None

    # Random tartibidagi birinchi nomzod kanaldan chiqib ketgan — o'tkazib yuboriladi
    async with env.sm() as s:
        from tgagent.agents.giveaway.models import Giveaway

        first = await service.next_candidate(s, await s.get(Giveaway, gid), [])
    env.bot.left.add(first.user_id)
    picks = (await env.client.post(f"/api/giveaways/{gid}/live/next", headers=H)).json()["picks"]
    assert picks[0] == {"number": first.number, "name": first.full_name, "place": None, "missing": ["Kanal"]}
    assert picks[-1]["place"] == 1 and len(picks) == 2
    # O'yin boshlangach ro'yxat yangilanmaydi
    assert (await env.client.post(f"/api/giveaways/{gid}/live/check", headers=H)).status_code == 400

    # Hamma o'rin to'lmaguncha e'lon qilinmaydi
    assert (await env.client.post(f"/api/giveaways/{gid}/live/announce", headers=H)).status_code == 400
    picks = (await env.client.post(f"/api/giveaways/{gid}/live/next", headers=H)).json()["picks"]
    assert picks[-1]["place"] == 2
    assert (await env.client.post(f"/api/giveaways/{gid}/live/next", headers=H)).status_code == 400

    sent_before = len(env.bot.sent)
    assert (await env.client.post(f"/api/giveaways/{gid}/live/announce", headers=H)).json() == {"ok": True}
    post = env.bot.sent[sent_before]
    assert post[1] == -100 and "Seed" not in post[2] and f"#{first.number}" in post[2]  # o'tkazilgani ko'rsatiladi
    g = (await env.client.get(f"/api/giveaways/{gid}")).json()
    assert g["status"] == "finished" and [w["place"] for w in g["winners"]] == [1, 2]
    pub = (await env.client.get(f"/api/public/giveaways/{gid}")).json()
    assert [w["place"] for w in pub["winners"]] == [1, 2] and "user_id" not in pub["winners"][0]
