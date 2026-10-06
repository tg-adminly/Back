# TG Agent Q

Telegram agentlar platformasi. 1-agent — qizlar uchun rozigrish kanalini avtomatlashtirish.
Talablar va kelishilgan qarorlar: **`SPEC.md`** (yagona manba — yangi qaror qabul qilinsa, shu faylni yangila).

Egasi bilan o'zbek tilida (lotin) gaplash.

## Buyruqlar

```bash
uv sync                          # bog'liqliklarni o'rnatish
uv run pytest                    # testlar
uv run python -m tgagent         # bot + panel (http://localhost:8080) ishga tushadi (.env kerak)
cd panel && npm install && npm run build   # panel frontendini yig'ish (o'zgargandan keyin)
cd panel && npm run dev          # frontendni jonli tahrirlash (http://localhost:5173, bot ham ishlab turishi kerak)
docker compose up -d --build     # VPS'da ishga tushirish
```

## Tuzilma

```
src/tgagent/
  config.py              # .env sozlamalari (pydantic-settings)
  __main__.py            # kirish nuqtasi: bot + fon vazifalar
  core/                  # hamma agentlar uchun umumiy: db, shifrlash, llm (AI + xarajat limiti)
  channels/telegram_bot/ # Bot API yordamchilari (obuna tekshiruvi, chat linklari)
  agents/giveaway/       # 1-agent: rozigrish
    draw.py              # tekshirsa bo'ladigan random (sof funksiyalar, LLM yo'q)
    models.py, service.py, jobs.py, texts.py, handlers/
    actions.py           # Telegram'ga tegadigan egasi amallari (bot menyusi va panel umumiy)
  agents/content/        # 2-agent qismi: kontent (o'qitish chati, uslub qo'llanma, namunalar)
  panel/                 # veb-panel backend: FastAPI API (content_api.py — kontent), botda kirishni tasdiqlash
panel/                   # veb-panel frontend: React + Vite + Tailwind (yig'ilgani panel/dist)
tests/
```

Keyingi agentlar (frilans va h.k.) `agents/<nom>/` ichida, `core/` dan foydalanadi.

## Qat'iy qoidalar

- **AI faqat `core/llm.py` orqali** (har so'rov narxi yoziladi, oylik limit). Post kanalga faqat xodim tasdiqlagandan keyin chiqadi.
- **G'olibni faqat `draw.py` aniqlaydi.** Rozigrish mantig'ida LLM ishlatilmaydi.
- **Agent pul o'tkazmaydi**, to'lov tizimlariga ulanmaydi. To'lovni egasi qiladi, "To'landi" bosadi, chekni yuklaydi.
- **Userbot** (3-bosqich) faqat egasi qo'shgan kontaktlarga, limit bilan yozadi. Egasining shaxsiy akkaunti ishlatilmaydi.
- Karta, telefon, manzil — faqat `Vault` orqali shifrlangan holda saqlanadi; ish tugagach tozalanadi.
- `.env`, `data/`, `*.session` fayllarini o'qima va chiqarma — ularda sirlar bor.
- Panel API faqat Owner/Editor sessiyasi bilan; karta/manzil faqat Owner so'raganda ochiladi. O'zgartiruvchi so'rovlar `x-panel: 1` sarlavhasini talab qiladi (CSRF).
- Foydalanuvchiga ko'rinadigan barcha matnlar o'zbek (lotin) tilida, `texts.py` da (panel frontendida — komponentlarning o'zida). Telegram HTML rejimi — foydalanuvchi matnini `html.escape` qil.
- Vaqt bazada UTC da saqlanadi, ko'rsatishda `settings.tz` (Asia/Tashkent).
- DB sxemasi hozircha `create_all` bilan; mavjud jadvalga yangi ustun `init_db` da o'zi qo'shiladi (`server_default` yoki NULL bo'lishi shart). Murakkab o'zgarishlar uchun Alembic qo'shiladi.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
