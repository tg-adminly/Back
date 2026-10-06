# TG Agent Q — 1-agent: Rozigrish kanali agenti

> Bu hujjat kelishilgan qarorlarni saqlaydi. Yangi qaror qabul qilinsa, shu yerga yoziladi.

## Maqsad

Qizlar uchun Telegram kanal/guruhni to'liq avtomatlashtirish: rozigrishlar, homiylar,
reklama muzokaralari, kontent. Hamma muhim qadamlar egasining nazoratida.

## Rollar

| Rol | Kim | Huquqlar |
|---|---|---|
| **Owner** | Egasi | Hammasi: agent sozlamalari, homiylar, CRM, to'lovlarni tasdiqlash, userbot kontaktlari |
| **Editor** | Egasining ayoli | Kontent: postlarni tasdiqlash/tahrirlash, uslub qo'llanma, post jadvali |

## Ikki "qo'l"

1. **Bot** (Bot API, aiogram) — kanal/guruhga post, rozigrish, "Qatnashish" tugmasi,
   obuna tekshiruvi, admin-panel (Owner/Editor uchun).
2. **Userbot** (alohida qoralama akkaunt, Telethon) — faqat **ruxsat berilgan kontaktlar**
   bilan yozishadi: reklama/homiylik bo'yicha kanal adminlari va rozigrish g'oliblari.
   - O'zi xohlagan odamga yozmaydi — kontaktni faqat Owner qo'shadi.
   - Limitlar: kuniga / haftasiga yangi suhbatlar soni sozlanadi.
   - Egasining shaxsiy akkaunti hech qachon ishlatilmaydi.

## Oqim 1 — Rozigrish

1. Owner rozigrish yaratadi: o'rinlar soni, **har bir o'rin uchun alohida sovrin** (pul summasi yoki buyum nomi;
   «Qolganlariga ham» tugmasi bilan bir xil qilish mumkin), tugash vaqti, homiy kanallar ro'yxati.
2. Bot har bir homiy kanalda admin bo'lishi shart (obunani tekshirish uchun) — bot buni oldindan tekshiradi.
   Yopiq kanal: Bot API `t.me/+...` linkdan kanalni topa olmaydi, shuning uchun bot admin qilingan kanallarni
   (`my_chat_member`) eslab qoladi. Panelda «Yopiq kanal» → ro'yxatdan tanlash + taklif linkini qo'yish. ID bilan qo'shish ham qoladi.
3. Kanalga post chiqadi: homiy linklari + **"Qatnashish (N)"** tugmasi (N — ishtirokchilar soni, har ~5 soniyada yangilanadi).
4. User tugmani **postning o'zida** bosadi (RandomGodBot kabi — botga kirish shart emas), bot obunani tekshirib popup chiqaradi:
   - hammasiga obuna → ishtirokchi bo'ladi, popupda raqami;
   - yo'q → popupda obuna bo'lmagan kanallar ro'yxati, obuna bo'lib qayta bosadi.
5. Tugash vaqtida **qatnashish yopiladi** (ro'yxat qotiriladi) va bot **hamma ishtirokchining obunasini qayta tekshiradi**
   (qatnashgandan keyin kanaldan chiqib ketganlar — qaysi kanaldan ekani bilan — randomga tushmaydi).
   Egasiga natija va jonli o'yin havolasi keladi. O'yin boshlanmaguncha jonli sahifada «Qayta tekshirish» mumkin
   (qayta obuna bo'lganlar qaytadi); birinchi g'olib chiqqach ro'yxat o'zgarmaydi.
   Ishtirokchi bo'lmasa — darhol «ishtirokchi bo'lmadi» e'lon qilinadi.
6. **Jonli o'yin** (panel, faqat Owner): egasi efirda ekranni ulashib, har o'rin uchun «G'olibni aniqlash»
   (yoki Probel) bosadi → baraban aylanadi → g'olib chiqadi. Chiqqan nomzodning obunasi shu zahoti tekshiriladi:
   chiqib ketgan bo'lsa ekranda «❌ «kanal» kanalidan chiqib ketgan — o'tkazib yuborildi» ko'rinadi va baraban qayta aylanadi.
   Hamma o'rinlar to'lgach «Natijani kanalga e'lon qilish» → efirda ko'ringan g'oliblar kanalga chiqadi,
   natija postida **"Yutuqni olish"** tugmasi (botga deep-link). G'olib yozuvlari (Winner) faqat e'londa yaratiladi.
   Bot g'olibga faqat u botni ochgan bo'lsa yoza oladi — shuning uchun g'olib shu tugma orqali kiradi:
   - pul sovrin → karta raqami + karta egasi ismi;
   - buyum sovrin → ism, telefon, manzil (BTS pochta uchun).
7. Owner'ga to'lov ro'yxati keladi → Owner o'zi to'laydi → "To'landi ✅" + chek screenshot →
   agent g'olibga yuboradi.

**Muhim:** rozigrish mantig'i (tekshiruv, random, ro'yxatlar) — oddiy kod, LLM emas.
Ishonchli, arzon, xato qilmaydi. **G'olibni AI aniqlamaydi — botning random funksiyasi aniqlaydi.**

### G'olib tanlash

- Random — serverda (`draw.py`): maxfiy `seed` + qotirilgan ro'yxat hash'i + raqam → `sha256`, eng kichigi birinchi.
  Jonli sahifa faqat animatsiya; natijani brauzer emas, server aniqlaydi.
- Seed/hash/formula **e'lon qilinmaydi** (obunachilarga tushunarsiz edi). Ishonch — jonli efir orqali.

### Ochiq ishtirokchilar sahifasi

- `/p/<id>` — login shart emas: ishtirokchilar (faqat ism va raqam, qidiruv), sovrinlar, holat.
  Chiqib ketganlar ustidan chizilgan, qaysi kanaldan chiqqani yoniga yoziladi.
  G'oliblar faqat kanalga e'lon qilingandan keyin ko'rinadi. Jonli baraban bu sahifada **ko'rinmaydi**
  (internet sekinligi sabab turli odamlar turli narsa ko'rib, norozilik bo'lmasligi uchun).
- Domen (https) ulangach, kanal postida va natija postida «👥 Ishtirokchilar ro'yxati» tugmasi chiqadi.

## Oqim 2 — Reklama / homiylik muzokarasi (CRM)

1. Owner kontakt qo'shadi: kanal linki, admin username, kanal sahifasidagi reklama ma'lumotlari
   (narxlar, shartlar — Owner nusxalab beradi), maqsad (bizni reklama qilish / homiy bo'lish).
2. Agent userbot orqali yozadi, shu ma'lumotga tayanib aniqlaydi:
   bitta post narxi, haftalik paket narxi, necha obunachi qo'shib bera oladi, to'lov usuli
   (karta / Click / Payme), karta raqami va egasi.
3. Agent Owner'ga xulosa yuboradi → Owner **tasdiqlaydi yoki rad etadi**. Agent o'zi kelishmaydi.
4. Owner to'laydi → "To'landi" + chek screenshot → agent adminga yuboradi, reklama sanasini kelishadi.
5. Hamma holat CRM'da: `yangi → yozildi → muzokara → taklif tayyor → tasdiqlandi → to'landi → bajarildi / rad`.

**Agent hech qachon pul o'tkazmaydi va to'lov tizimlariga ulanmaydi.**

## Oqim 3 — Kontent

1. Agent jadval bo'yicha post qoralamasi yozadi (o'zbek, lotin).
2. Editor admin-botda: ✅ Tasdiqlash / ✏️ Tahrirlash / ❌ Rad.
3. Editor agentga uslub bo'yicha ko'rsatmalar beradi → **uslub qo'llanma** sifatida saqlanadi
   va har bir post yozilganda ishlatiladi.
4. Boshida hamma post tasdiqdan o'tadi.

## Boshqaruv paneli (CRM sayt, keyin Mini App)

Rozigrish yaratish, g'oliblar/to'lovlar, homiylar — **veb-panelda** (bot menyusi zaxira sifatida qoladi).
Keyin CRM, userbot suhbatlari, kontent tasdig'i ham shu yerga qo'shiladi.
- Hozir: alohida sayt (bot bilan bir jarayonda, `PANEL_URL`). Keyin shu panel Telegram Mini App sifatida ham ochiladi.
- Kirish: saytda «Telegram orqali kirish» → botda «✅ Ha, men kiryapman» → 30 kunlik sessiya. Parol yo'q.
  Faqat Owner/Editor ID'lari; karta/telefon/manzil faqat Owner «Ko'rsatish» bosganda ochiladi.
- To'lov: panelda «To'landi» → chek rasmi/izoh yuklanadi → bot g'olibga yuboradi, shaxsiy ma'lumot o'chadi.
  To'lovlar sahifasi rozigrishlar bo'yicha guruhlangan (har birida holat va jami pul).
- Bot o'zi asosan ishtirokchilar uchun (Qatnashish popup, g'olibdan ma'lumot) + egasiga bildirishnomalar.
- Domen: keyinroq (VPS + domen + Caddy HTTPS). Mini App uchun HTTPS majburiy.

## Kanal yoki guruh

Kod ikkalasini ham qo'llab-quvvatlaydi. Tavsiya: **kanal + unga bog'langan muhokama guruhi**.
Guruh tanlansa, qo'shimcha moderatsiya (spam/reklama o'chirish) kerak bo'ladi.

## Texnik qarorlar

- Python 3.12+, `uv`, aiogram 3, Telethon, SQLAlchemy + SQLite (keyin Postgres), APScheduler.
- LLM: provider almashtiriladigan qatlam. Hozir **OpenAI** (kalit bor), keyin Claude qo'shilishi mumkin.
  Arzon model — oddiy ishlar uchun, kuchliroq model — muzokara uchun (config'da).
- Byudjet: oyiga ~$20–50. LLM faqat matn yozish va suhbat uchun ishlatiladi → yetadi.
  Oylik xarajat limiti va hisoblagich bo'ladi.
- Shaxsiy ma'lumotlar (karta, telefon, manzil) shifrlanib saqlanadi, ish tugagach o'chiriladi.
- Deploy: egasining VPS'i, Docker Compose.
- Arxitektura: `core/` (umumiy: LLM, tasdiqlar, xotira, scheduler) + `agents/giveaway/`.
  Keyingi agentlar (frilans va h.k.) shu yadrodan foydalanadi.

## Bosqichlar

1. **Rozigrish yadrosi** — admin-bot, rozigrish, Qatnashish/tekshiruv, g'olib tanlash, ma'lumot yig'ish, to'lov ro'yxati.
2. **Kontent** — post qoralamalari, Editor tasdig'i, uslub qo'llanma, jadval.
3. **CRM + userbot muzokaralari** — kontaktlar, limitlar, xulosa va tasdiq, chek yuborish.
4. **Avtomatlashtirishni kengaytirish** va keyingi agentlar.

## Ishga tushirish uchun kerak bo'ladi

- Bot token (@BotFather)
- Userbot uchun `api_id` / `api_hash` (my.telegram.org, qoralama akkaunt bilan)
- OpenAI API kaliti
- Owner va Editor Telegram ID'lari
