"""Panel bilan bog'liq, botda ko'rinadigan matnlar."""

LOGIN_ASK = (
    "🔐 <b>Panelga kirish so'rovi</b>\n\n"
    "Agar hozir <b>o'zingiz</b> saytda «Telegram orqali kirish» ni bosgan bo'lsangiz — tasdiqlang.\n"
    "⚠️ Kimdir sizga bu havolani yuborgan bo'lsa, <b>bosmang</b>: u sizning nomingizdan panelga kiradi."
)
BTN_LOGIN_CONFIRM = "✅ Ha, men kiryapman"
LOGIN_DONE = "✅ Tasdiqlandi. Brauzerga qayting — panel ochiladi."
LOGIN_EXPIRED = "⌛ Bu kirish havolasi eskirgan. Saytda «Telegram orqali kirish» ni qayta bosing."

# --- API xatolari (panelda ko'rinadi, oddiy matn) ---

API_NOT_LOGGED_IN = "Avval panelga kiring."
API_FORBIDDEN = "Ruxsat yo'q."
API_OWNER_ONLY = "Bu bo'lim faqat egasi uchun."
API_NOT_FOUND = "Topilmadi."
API_REQUIRED = "To'ldiring."
API_BAD_PRIZE = "Summa (500000, 500 ming, 1.5 mln) yoki sovg'a nomini yozing."
API_BAD_ENDS_AT = "Kelajakdagi sana va vaqtni tanlang."
API_BAD_LINK = "Havola https://t.me/ bilan boshlanishi kerak."
API_SPONSOR_IN_USE = "Bu kanal faol rozigrish #{id} da homiy. Avval u yakunlansin."
API_FILE_TOO_BIG = "Fayl 10 MB dan katta bo'lmasin."
API_NEED_PROOF = "Chek rasmini yuklang yoki izoh yozing (masalan BTS trek raqami)."
