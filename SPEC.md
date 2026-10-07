# TG Agent Q — 1-agent: Rozigrish kanali agenti

> Bu hujjat kelishilgan qarorlarni saqlaydi. Yangi qaror qabul qilinsa, shu yerga yoziladi.

## Maqsad

Qizlar uchun Telegram kanal/guruhni to'liq avtomatlashtirish: rozigrishlar, homiylar,
reklama muzokaralari, kontent. Hamma muhim qadamlar egasining nazoratida.

## Rollar

| Rol | Kim | Huquqlar |
|---|---|---|
| **Owner** | Egasi | Hammasi: agent sozlamalari, homiylar, CRM, to'lovlarni tasdiqlash, userbot kontaktlari |
| **Editor** | Egasining ayoli | Kontent: postlarni tasdiqlash/tahrirlash, uslub qo'llanma, post jadvali. Rozigrishlarni ko'radi, qatnashishni yopadi va **jonli o'yinni o'tkazadi** (yaratish, o'zgartirish, bekor qilish, to'lov, homiylar — yo'q) |

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
   «Qolganlariga ham» tugmasi bilan bir xil qilish mumkin), vaqt, homiy kanallar ro'yxati va **g'olibni aniqlash usuli**:
   - 🎥 **Jonli o'yin** (standart): vaqt — faqat eslatma (postda «Jonli o'yin: <vaqt>»). Vaqt kelganda egasi va muharrirga
     bir marta eslatma keladi; qatnashish **o'zi yopilmaydi**, bot g'olib aniqlamaydi va kanalga hech narsa tashlamaydi.
     O'yinni istalgan paytda (vaqtdan oldin ham, keyin ham) jonli sahifadagi «Qatnashishni yopib, o'yinni boshlash» bilan boshlaydi;
   - 🤖 **Avtomatik**: vaqti kelganda bot o'zi aniqlaydi va natijani kanalga tashlaydi (jonli o'yindagi qadamlarning o'zi:
     qayta tekshiruv → o'rinma-o'rin, chiqib ketganlar o'tkaziladi → e'lon). Xato bo'lsa — egasi/muharrirga jonli o'yin havolasi.
   Faol rozigrishda vaqt va usulni («✏️ O'zgartirish»), **homiylarni** (alohida «📣 Homiylar» tugmasi: qo'shish/olib tashlash) o'zgartirish mumkin —
   kanal posti ham yangilanadi. Yangi homiy qo'shilsa, oldin qatnashganlar ham unga obuna bo'lishi kerak (aks holda o'tkaziladi):
   ixtiyoriy ravishda kanalga «yangi homiy qo'shildi» xabari (post'ga javob) ketadi. Post hammaga bir xil (Telegram tugmalarni
   har kimga alohida ko'rsatmaydi), shuning uchun oldin qatnashgan odam «Qatnashish»ni bossa, popupda aynan u obuna
   bo'lmagan kanallar chiqadi.
   **Obuna holati faol rozigrishda ham ko'rinadi:** homiylar o'zgarsa bot hammani o'zi qayta tekshiradi; panelda
   (rozigrish sahifasi → ishtirokchilar) «🔄 Obunani tekshirish» tugmasi va «Faqat obuna bo'lmaganlar» filtri, har birining
   yonida qaysi kanalga obuna emasligi. Ochiq ro'yxatda (`/p/<id>`) ham shu ko'rinadi. Ishtirokchi «Qatnashish»ni qayta
   bossa, uning holati darhol yangilanadi.
   Botdagi yaratishda ham ko'rib chiqish oynasida usulni almashtirish tugmasi bor.
2. Bot har bir homiy kanalda admin bo'lishi shart (obunani tekshirish uchun) — bot buni oldindan tekshiradi.
   Yopiq kanal: Bot API `t.me/+...` linkdan kanalni topa olmaydi, shuning uchun bot admin qilingan kanallarni
   (`my_chat_member`) eslab qoladi. Panelda «Yopiq kanal» → ro'yxatdan tanlash + taklif linkini qo'yish. ID bilan qo'shish ham qoladi.
3. Kanalga post chiqadi: homiy linklari + **"Qatnashish (N)"** tugmasi (N — ishtirokchilar soni, har ~5 soniyada yangilanadi).
4. User tugmani **postning o'zida** bosadi (RandomGodBot kabi — botga kirish shart emas), bot obunani tekshirib popup chiqaradi:
   - hammasiga obuna → ishtirokchi bo'ladi, popupda raqami;
   - yo'q → popupda obuna bo'lmagan kanallar ro'yxati, obuna bo'lib qayta bosadi.
5. **Qatnashish yopiladi** (ro'yxat qotiriladi): avtomatik rejimda — vaqtida, jonli rejimda — o'yin boshlanganda
   (yoki botdagi «Hozir yakunlash»). Bot **hamma ishtirokchining obunasini qayta tekshiradi**
   (kanalga obuna bo'lmaganlar — qaysi kanal ekani bilan — randomga tushmaydi).
   Botdan yopilsa, egasi va muharrirga natija va jonli o'yin havolasi keladi. O'yin boshlanmaguncha jonli sahifada «Qayta tekshirish» mumkin
   (qayta obuna bo'lganlar qaytadi); birinchi g'olib chiqqach ro'yxat o'zgarmaydi.
   Ishtirokchi bo'lmasa — darhol «ishtirokchi bo'lmadi» e'lon qilinadi.
6. **Jonli o'yin** (panel, Owner yoki Editor): egasi/muharrir efirda ekranni ulashib, har o'rin uchun «G'olibni aniqlash»
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

### Bekor qilish

- Faol yoki g'olib aniqlanayotgan (hali e'lon qilinmagan) rozigrishni Owner bekor qila oladi; kanaldagi post bilan nima qilish so'raladi:
  - 📢 **E'lon qilish** (tavsiya): post «❌ ROZIGRISH BEKOR QILINDI» + chizilgan matn bilan tahrirlanadi, tugmalari olinadi,
    kanalga qisqa xabar ketadi. Tahrirlashda vaqt cheklovi yo'q;
  - 🗑 **O'chirish**: Telegram 48 soatdan eski postni botga o'chirtirmasligi mumkin — unda tugmalari olinadi va egasiga aytiladi;
  - 🤫 **Tegmaslik**: kanalga hech narsa qilinmaydi.

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

## Oqim 3 — Kontent (2-bosqich)

Maqsad: agent kanal uslubida post yozadi, Editor tasdiqlaydi, bot vaqtida chiqaradi.
Agent ishlagan sari o'rganadi. **Hamma post tasdiqdan o'tadi** (avto rejimda ham).

### Agent bilimi
- **Uslub qo'llanma** — agentning o'zi uchun yozgan umumiy qoidalari (ohang, uzunlik, emoji, tuzilish,
  mavzular, nima qilinmaydi). Har o'zgarish versiya sifatida saqlanadi, Editor ko'radi, qo'lda tuzatadi, eski versiyaga qaytaradi.
- **Namunalar kutubxonasi** — o'qitish uchun postlar: matn + rasmlar (albom — 10 tagacha, yoki tavsifi) + manba
  (o'z kanalimiz / boshqa kanal) + agentning qisqa tahlili.

### O'qitish chati (panel)
- Editor/Owner AI bilan chat ko'rinishida gaplashadi: postlarni (10–20 ta, matn va rasm) tashlaydi, izoh beradi.
- Agent tahlil qiladi va «qo'llanmaga shu qoidalarni qo'shaman» deb taklif qiladi → ✅ Qabul / ✏️ Tuzat / ❌ Yo'q.
  Qo'llanma faqat tasdiqlangandan keyin o'zgaradi.
- Rasmlar: AI rasmni o'zi ko'radi (vision), xohlasa Editor tavsif yozadi. Rasmni agent **yaratmaydi**.

- Holati (2026-10-07): **o'qitish chati, qo'llanma (versiyalar, farq ko'rinishi, qaytarish), namunalar — tayyor** (panel «📝 Kontent»).
- Chat — chatbot ko'rinishida: pastda bitta yozish maydoni, 📎 bilan rasm(lar) biriktiriladi (rasmli xabar = namuna post,
  rasmsizini «Rasmsiz post» bilan belgilash mumkin). Agent har xabarga fonda javob beradi; u yozayotganda yuborilganlar
  navbatga tushib, keyingi bitta javobda birga ko'riladi. Rasm agentga arzon «low» sifatda beriladi.

### O'z kanalimizni o'qish
- Bot kanalda admin — yangi chiqqan har bir post (qo'lda yozilganlar ham) avtomatik namunaga tushadi.
- Bot API eski tarixni o'qiy olmaydi. Eski postlar: botga forward qilish yoki Telegram Desktop eksporti (JSON) ni panelga yuklash.
  Keyinchalik userbot (3-bosqich) tarixni o'zi o'qiydi.

### Qoralama → tasdiq → chiqish
1. Editor mavzu/rasm beradi yoki agent o'zi mavzu tanlaydi → agent qoralama yozadi.
2. Holatlar: `qoralama → tasdiqlandi (vaqt bilan) → chiqdi`, yoki `rad`.
3. Editor: ✅ Tasdiqlash (hozir yoki vaqtga) / ✏️ Tahrirlash / 🔁 Izoh bilan qayta yozdirish / ❌ Rad.
4. Rasmni asosan Editor yuklaydi — bitta yoki bir nechta (albom, 10 tagacha). Rasmli postda matn ≤ 1024 belgi
   (Telegram cheklovi, albomda matn birinchi rasm tagida) — agent shunga moslab yozadi.
5. **O'rganish:** Editor tuzatgan/rad etgan qoralamalardan agent saboq chiqaradi va qo'llanmaga o'zgarish taklif qiladi (tasdiq bilan).

### Jadval
- **Avto rejim:** kuniga N–M ta post, vaqt oralig'i (masalan 09:00–21:00). Agent oldindan qoralamalar tayyorlaydi,
  Editorga bildirishnoma ketadi; tasdiqlanmagan qoralama chiqmaydi.
- **Qo'lda rejim:** agent o'zi yozmaydi, Editor so'raganda qoralama yozadi.

### LLM va xarajat
- `core/llm.py` — provider qatlami (hozir OpenAI, model `.env` da). Har so'rov tokenlari va narxi hisoblanadi.
- Oylik limit (standart $20). Limit tugasa AI to'xtaydi, Owner'ga xabar boradi; panelda sarflangan summa ko'rinadi.

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
