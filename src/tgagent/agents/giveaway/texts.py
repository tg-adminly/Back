"""Foydalanuvchiga ko'rinadigan barcha matnlar (o'zbek, lotin). HTML rejimi."""

from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

from tgagent.agents.giveaway.models import Giveaway, Prize, PrizeType, Winner, WinnerStatus
from tgagent.core.crypto import Vault


def money(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " so'm"


def local_time(dt: datetime, tz: ZoneInfo) -> str:
    return dt.astimezone(tz).strftime("%d.%m.%Y %H:%M")


def user_link(user_id: int, name: str) -> str:
    return f'<a href="tg://user?id={user_id}">{escape(name)}</a>'


def prize_text(prize: Prize) -> str:
    return money(prize.amount) if prize.type == PrizeType.MONEY else escape(prize.name or "")


_MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


def prizes_block(prizes: list[Prize]) -> list[str]:
    """Ketma-ket bir xil sovrinlar birlashtiriladi: «🏅 4–10-o'rinlar: 100 000 so'm»."""
    lines, start = [], 0
    while start < len(prizes):
        end = start
        while end + 1 < len(prizes) and prizes[end + 1] == prizes[start]:
            end += 1
        first, last = start + 1, end + 1
        if first == last:
            lines.append(f"{_MEDALS.get(first, '🏅')} {first}-o'rin: <b>{prize_text(prizes[start])}</b>")
        else:
            lines.append(f"🏅 {first}–{last}-o'rinlar: <b>{prize_text(prizes[start])}</b> (har biriga)")
        start = end + 1
    return lines


# --- Menyu ---

BTN_NEW = "🎁 Yangi rozigrish"
BTN_LIST = "📋 Faol rozigrishlar"
BTN_PAYOUTS = "💳 To'lovlar"

OWNER_WELCOME = "Salom! Boshqaruv paneli. Quyidagi tugmalardan foydalaning.\nIstalgan jarayonni to'xtatish: /bekor"
EDITOR_WELCOME = "Salom! Kontent bo'limi (postlar, uslub qo'llanma) 2-bosqichda qo'shiladi."
DEFAULT_REPLY = (
    "Salom! 👋 Bu bot kanalimizdagi rozigrishlar uchun.\n"
    "Qatnashish uchun kanaldagi rozigrish postidagi «🎁 Qatnashish» tugmasini bosing."
)
CANCELLED = "Bekor qilindi."
STAFF_UNKNOWN = "Tushunmadim. Menyu: /menu, jarayonni bekor qilish: /bekor"

# --- Rozigrish yaratish ---

ASK_TITLE = "Rozigrish nomini yozing (masalan: «Kuzgi rozigrish»):"
ASK_DESCRIPTION = "Rozigrish haqida qisqa matn yozing (post matni, qo'shimcha shartlar):"
ASK_WINNERS = "Nechta o'rin (g'olib) bo'ladi? (1–100)"
BAD_WINNERS = "1 dan 100 gacha son yozing."
PRIZE_HINT = (
    "Pul bo'lsa — summani yozing: <code>500000</code>, <code>500 ming</code>, <code>1.5 mln</code>\n"
    "Buyum bo'lsa — nomini yozing: <code>iPhone 15</code>, <code>Chanel atiri</code>"
)
BAD_PRIZE = "Tushunmadim. " + PRIZE_HINT


def ask_place_prize(place: int, total: int) -> str:
    head = f"🏆 <b>{place}-o'rin</b> sovrini? ({place}/{total})"
    return head + "\n\n" + PRIZE_HINT if place == 1 else head


def btn_same_for_rest(prize: Prize) -> str:
    label = money(prize.amount) if prize.type == PrizeType.MONEY else (prize.name or "")
    return f"↪️ Qolganlariga ham: {label[:40]}"

ASK_ENDS_AT = "Qachon yakunlanadi? Format: <code>kk.oo.yyyy ss:dd</code> (Toshkent vaqti)\nMasalan: <code>15.10.2026 20:00</code>"
BAD_ENDS_AT = "Format noto'g'ri yoki vaqt o'tib ketgan. Masalan: <code>15.10.2026 20:00</code>"
ASK_SPONSORS = (
    "Homiy kanallarni birma-bir yuboring:\n"
    "• <code>@username</code>, yoki\n"
    "• kanaldan istalgan postni shu yerga <b>forward</b> qiling, yoki\n"
    "• yopiq kanal uchun: <code>-100ID https://t.me/+link</code>\n\n"
    "⚠️ Bot har bir homiy kanalda <b>admin</b> bo'lishi shart (obunani tekshirish uchun).\n"
    "Tugatgach «Tayyor» ni bosing. Homiysiz bo'lsa ham «Tayyor» ni bosing."
)
BTN_DONE = "✅ Tayyor"
SPONSOR_NOT_FOUND = "Kanal topilmadi. @username to'g'rimi yoki bot kanalga qo'shilganmi?"
SPONSOR_NOT_ADMIN = "❌ Bot «{title}» kanalida admin emas. Avval botni admin qiling, keyin qayta yuboring."
SPONSOR_NO_LINK = "Bu kanal yopiq va linkini ololmadim. Shunday yuboring: <code>{chat_id} https://t.me/+link</code>"
SPONSOR_IS_MAIN = "Bu bizning asosiy kanalimiz — u avtomatik shart qilib qo'shiladi."


def sponsor_added(titles: list[str]) -> str:
    listing = "\n".join(f"{i}. {escape(t)}" for i, t in enumerate(titles, 1))
    return f"✅ Qo'shildi. Homiylar:\n{listing}\n\nYana yuboring yoki «Tayyor» ni bosing."


BTN_PUBLISH = "📢 E'lon qilish"
# Bosilsa boshqasiga almashadi
BTN_AUTO_OFF = "🔁 G'olib: 🎥 jonli o'yinda"
BTN_AUTO_ON = "🔁 G'olib: 🤖 bot avtomatik"
BTN_CANCEL = "❌ Bekor qilish"
PREVIEW_HEADER = "👇 Post shunday ko'rinadi. E'lon qilaymi?"
PUBLISHED = "✅ Rozigrish #{id} e'lon qilindi!"
PUBLISH_FAILED = "❌ Kanalga post chiqmadi: {error}\nBot asosiy kanalda post yozish huquqiga ega adminmi?"


def giveaway_post(g: Giveaway, tz: ZoneInfo, sponsor_titles: list[str]) -> str:
    lines = [
        "🎁 <b>ROZIGRISH!</b>",
        "",
        f"<b>{escape(g.title)}</b>",
        escape(g.description),
        "",
        "🏆 <b>Sovrinlar:</b>",
        *prizes_block(g.prizes),
        "",
        f"⏰ Yakunlanadi: <b>{local_time(g.ends_at, tz)}</b> (Toshkent vaqti)",
        "",
        "<b>Qatnashish shartlari:</b>",
    ]
    step = 1
    if sponsor_titles:
        lines.append(f"{step}. Homiy kanallarga obuna bo'ling (pastdagi tugmalar)")
        step += 1
    lines += [
        f"{step}. Pastdagi «🎁 Qatnashish» tugmasini bosing",
        "",
        "🤖 G'oliblar shu vaqtda bot tomonidan avtomatik aniqlanadi!" if g.auto_draw else "🎥 G'oliblar jonli efirda aniqlanadi!",
    ]
    return "\n".join(lines)


BTN_JOIN = "🎁 Qatnashish"
BTN_PARTICIPANTS = "👥 Ishtirokchilar ro'yxati"


def join_button(count: int) -> str:
    return f"{BTN_JOIN} ({count})" if count else BTN_JOIN


# --- Faol rozigrishlar ---

NO_ACTIVE = "Faol rozigrish yo'q."
BTN_FINISH_NOW = "⏹ Hozir yakunlash"
BTN_CANCEL_GIVEAWAY = "🗑 Bekor qilish"
BTN_YES = "Ha, tasdiqlayman"
CONFIRM_FINISH = "Rozigrish #{id} da qatnashishni hozir yopaymi? {next}"
FINISH_NEXT_AUTO = "Bot g'oliblarni darhol o'zi aniqlab, kanalga e'lon qiladi."
FINISH_NEXT_LIVE = "G'oliblarni keyin panelda jonli o'yinda aniqlaysiz."
CONFIRM_CANCEL = "Rozigrish #{id} ni bekor qilaymi? G'olib aniqlanmaydi."
FINISH_SCHEDULED = "⏳ Rozigrish #{id} da qatnashish 1 daqiqa ichida yopiladi. {next}"
FINISH_SCHEDULED_AUTO = "Keyin bot g'oliblarni o'zi aniqlab, kanalga e'lon qiladi."
FINISH_SCHEDULED_LIVE = "Keyin jonli o'yin uchun havola yuboraman."
GIVEAWAY_CANCELLED = "🗑 Rozigrish #{id} bekor qilindi."
NOT_ACTIVE = "Bu rozigrish allaqachon faol emas."


def active_item(g: Giveaway, count: int, tz: ZoneInfo) -> str:
    return (
        f"<b>#{g.id} {escape(g.title)}</b>\n"
        f"👥 Ishtirokchilar: {count}\n"
        f"🏆 G'oliblar: {g.winners_count}\n"
        f"⏰ Yakun: {local_time(g.ends_at, tz)}\n"
        f"{draw_mode(g)}"
    )


def draw_mode(g: Giveaway) -> str:
    return "🤖 G'olibni bot avtomatik aniqlaydi" if g.auto_draw else "🎥 G'olib jonli o'yinda aniqlanadi"


# --- Qatnashish ---

# Popup (alert) matnlari: HTML ishlamaydi, 200 belgigacha.
GIVEAWAY_NOT_FOUND = "Bu rozigrish topilmadi."
GIVEAWAY_CLOSED = "Bu rozigrish yakunlangan. Keyingi rozigrishlarni kuzatib boring! 💕"
ALERT_LIMIT = 200


def joined(number: int) -> str:
    return (
        f"🎉 Siz qatnashyapsiz! Raqamingiz: #{number}\n\n"
        "⚠️ Natija chiqquncha kanallardan chiqmang, aks holda g'oliblikdan chetlatilasiz."
    )


def already_joined(number: int) -> str:
    return f"✅ Siz allaqachon qatnashyapsiz. Raqamingiz: #{number}"


def not_subscribed(titles: list[str]) -> str:
    text = "❌ Avval bu kanallarga obuna bo'ling, keyin qayta bosing:\n" + "\n".join(f"• {t}" for t in titles)
    return text if len(text) <= ALERT_LIMIT else text[: ALERT_LIMIT - 1] + "…"


# --- Natija ---


def results_post(
    g: Giveaway, total: int, winners: list[tuple[int, int, str, int]], skipped: list[int]
) -> str:
    """winners: (o'rin, user_id, ism, raqam)."""
    lines = ["🏁 <b>Rozigrish yakunlandi!</b>", f"<b>{escape(g.title)}</b>", f"👥 Ishtirokchilar: {total}", ""]
    if winners:
        lines.append("🏆 <b>G'oliblar:</b>" if g.auto_draw else "🏆 <b>Jonli efirda aniqlangan g'oliblar:</b>")
        prizes = g.prizes
        lines += [
            f"{_MEDALS.get(place, '🏅')} {user_link(uid, name)} — #{num} — {prize_text(prizes[place - 1])}"
            for place, uid, name, num in winners
        ]
        lines.append("\nTabriklaymiz! 🎉 G'oliblar, yutuqni olish uchun pastdagi «🎁 Yutuqni olish» tugmasini bosing.")
    else:
        lines.append("Afsuski, shartlarni bajargan ishtirokchi bo'lmadi.")
    if skipped:
        nums = ", ".join(f"#{n}" for n in skipped)
        lines.append(f"\n<i>Obunadan chiqib ketgani uchun o'tkazib yuborildi: {nums}</i>")
    return "\n".join(lines)


BTN_CLAIM = "🎁 Yutuqni olish"
NOT_A_WINNER = "Siz bu rozigrishda g'olib bo'lmadingiz. Keyingi rozigrishlarda omad! 💕"
CLAIM_ALREADY_DONE = "✅ Ma'lumotlaringiz allaqachon qabul qilingan. Yutug'ingizni tez orada yuboramiz."
NO_PARTICIPANTS = "🏁 «{title}» rozigrishi yakunlandi, lekin ishtirokchi bo'lmadi."


# --- G'olib bilan yozishma ---


def winner_congrats(w: Winner) -> str:
    head = (
        f"🎉 <b>Tabriklaymiz!</b> Siz «{escape(w.giveaway.title)}» rozigrishida <b>{w.place}-o'rinni</b> egalladingiz!\n"
        f"Yutuq: <b>{prize_text(w.prize)}</b>\n\n"
    )
    if w.prize.type == PrizeType.MONEY:
        return head + "Pulni o'tkazishimiz uchun <b>karta raqamingizni</b> yuboring (16 ta raqam)."
    return head + "Sovg'ani BTS pochta orqali yuboramiz. Iltimos, <b>to'liq ism-familiyangizni</b> yozing."


ASK_CARD_HOLDER = "Rahmat! Endi <b>karta egasining ism-familiyasini</b> yozing."
BAD_CARD = "Karta raqami 16 ta raqamdan iborat bo'lishi kerak. Qayta yuboring."
ASK_PHONE = "Rahmat! Endi <b>telefon raqamingizni</b> yuboring (pastdagi tugma yoki +998XXXXXXXXX)."
BTN_SHARE_PHONE = "📱 Raqamni yuborish"
BAD_PHONE = "Raqam noto'g'ri. Masalan: +998901234567"
ASK_ADDRESS = "Rahmat! Endi <b>to'liq manzilingizni</b> yozing (viloyat, tuman, ko'cha, uy) yoki eng yaqin BTS filiali."
NEED_TEXT = "Iltimos, matn ko'rinishida yozing."
CLAIM_DONE = "✅ Ma'lumotlaringiz qabul qilindi! Tez orada yutug'ingizni yuboramiz. Ma'lumotlar faqat yutuqni yetkazish uchun ishlatiladi."
PRIZE_SENT_MONEY = "💸 Yutug'ingiz kartangizga o'tkazildi! Yana bir bor tabriklaymiz 🎉"
PRIZE_SENT_ITEM = "📦 Sovg'angiz BTS pochta orqali yuborildi! Yana bir bor tabriklaymiz 🎉"

# --- Egasi uchun: to'lovlar ---

NO_PAYOUTS = "Ochiq to'lov yo'q ✅"
BTN_PAID = "✅ To'landi"
BTN_SENT = "✅ Yuborildi"
ASK_PROOF = "Chek skrinshotini (yoki BTS trek raqamini) yuboring — g'olibga jo'nataman. Bekor qilish: /bekor"
PROOF_SENT = "✅ G'olibga yuborildi, holat yopildi."
PROOF_FAILED = "⚠️ Holat yopildi, lekin g'olibga yuborib bo'lmadi (botni bloklagan bo'lishi mumkin)."
WINNER_DM_FAILED = (
    "ℹ️ G'olib {link} botni hali ochmagan, shuning uchun unga o'zim yoza olmadim. "
    "U natija postidagi «🎁 Yutuqni olish» tugmasini bosishi kerak — kerak bo'lsa, eslatib qo'ying."
)


def live_ready(g: Giveaway, total: int, excluded: int | None, live_url: str) -> str:
    """excluded=None — obunani tekshirib bo'lmadi (panelda qayta tekshirish mumkin)."""
    if excluded is None:
        check = "⚠️ Obunani tekshirib bo'lmadi — jonli o'yin sahifasida «Qayta tekshirish»ni bosing.\n\n"
    elif excluded:
        check = f"🔄 Obuna qayta tekshirildi: {excluded} kishi homiy kanaldan chiqib ketgan — o'yinda qatnashmaydi.\n\n"
    else:
        check = "🔄 Obuna qayta tekshirildi: hamma shartni bajargan ✅\n\n"
    return (
        f"⏰ Rozigrish #{g.id} «{escape(g.title)}» vaqti keldi — qatnashish yopildi. Ishtirokchilar: {total}.\n"
        f"{check}"
        f"🎥 Jonli o'yinni boshlash (efirda ekranni ulashing):\n{live_url}"
    )


def auto_draw_failed(g: Giveaway, error: str, live_url: str) -> str:
    return (
        f"⚠️ Rozigrish #{g.id} «{escape(g.title)}»: g'oliblarni avtomatik aniqlab bo'lmadi.\n{error}\n\n"
        f"Jonli o'yin sahifasida qo'lda davom ettiring:\n{live_url}"
    )


POST_EDIT_FAILED = "Sozlama saqlandi, lekin kanaldagi postni yangilab bo'lmadi: {error}"
NOT_EDITABLE = "Faqat faol rozigrishni o'zgartirish mumkin."

# Jonli o'yin (panel) xatolari
NOT_DRAWING = "Bu rozigrish jonli o'yin bosqichida emas."
ALL_PLACES_FILLED = "Hamma o'rinlar to'ldi — natijani guruhga e'lon qiling."
NO_MORE_CANDIDATES = "Boshqa nomzod qolmadi — natijani guruhga e'lon qiling."
DRAW_NOT_DONE = "Hali hamma o'rinlar aniqlanmadi."
BOT_NOT_ADMIN_IN = "Bot «{title}» kanalida admin emas — obunani tekshira olmayman. Botni admin qiling va qayta urining."
ANNOUNCE_FAILED = "Natijani kanalga yuborib bo'lmadi: {error}"
CHECK_RUNNING = "Obuna tekshirilmoqda — tugashini kuting."
CHECK_FAILED = "Obunani tekshirishda xato bo'ldi — qayta urinib ko'ring."
CHECK_TOO_LATE = "O'yin boshlangan — ro'yxatni endi yangilab bo'lmaydi."


def draw_summary(g: Giveaway, total: int, winners_count: int) -> str:
    return (
        f"🏁 Rozigrish #{g.id} «{escape(g.title)}» yakunlandi.\n"
        f"Ishtirokchilar: {total}, g'oliblar: {winners_count}.\n"
        "G'oliblarga yozdim, ma'lumot kelganda xabar beraman."
    )


def payout_card(w: Winner, vault: Vault) -> str:
    g, p = w.giveaway, w.participant
    lines = [
        f"💳 <b>«{escape(g.title)}»</b> — {w.place}-o'rin",
        f"G'olib: {user_link(w.user_id, p.full_name)} (#{p.number})",
        f"Yutuq: <b>{prize_text(w.prize)}</b>",
    ]
    if w.status == WinnerStatus.AWAITING_INFO:
        lines.append("⏳ G'olibdan ma'lumot kutilmoqda")
        return "\n".join(lines)
    if w.prize.type == PrizeType.MONEY:
        lines.append(f"Karta: <code>{escape(vault.decrypt(w.card_enc) or '')}</code>")
        lines.append(f"Egasi: {escape(vault.decrypt(w.card_holder_enc) or '')}")
    else:
        lines.append(f"Ism: {escape(vault.decrypt(w.full_name_enc) or '')}")
        lines.append(f"Tel: <code>{escape(vault.decrypt(w.phone_enc) or '')}</code>")
        lines.append(f"Manzil: {escape(vault.decrypt(w.address_enc) or '')}")
    return "\n".join(lines)
