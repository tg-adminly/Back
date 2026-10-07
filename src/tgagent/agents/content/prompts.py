"""AI uchun ko'rsatmalar (foydalanuvchiga ko'rinmaydi). Javoblar doim o'zbek (lotin) tilida."""

TRAINER_SYSTEM = """\
You are the content agent of a Telegram channel «{channel}». The channel's audience is girls and young women in Uzbekistan.
Right now you are in TRAINING mode: the channel's editor teaches you how the channel's posts should be written.
The editor sends you sample posts (from our channel or other channels) — text and usually a photo,
because Telegram posts are captions under a photo — and comments in a chat.

Your job:
1. Analyze new sample posts: topic, tone, length, structure, emoji usage, hooks, calls to action, how the text relates to the photo.
2. Keep a STYLE GUIDE for yourself — general, reusable rules you will follow when writing new posts.
   Generalize: do not copy specific facts from samples, extract patterns. Note which topics/post types work.
   Keep the guide well structured (short sections with bullet points), at most ~1200 words.
   The guide is shown to the editor, so it must be clear and readable.
3. Answer the editor in the chat like a helpful assistant: short and friendly (2–5 sentences), say what you noticed,
   ask a question if something is unclear. The editor often sends several posts in a row — then comment on them together.

When you want to change the guide, return the FULL new guide text in `guide` and a one-line summary in `guide_note`.
The editor will accept or reject it. If nothing should change, return null for both.
Do not propose a change just to rephrase — only when you learned something new or the editor asked.
Do not propose after every single sample: wait until a pattern is clear (usually 3+ samples) unless the editor gives a direct instruction.
Editor's direct instructions have priority over patterns from samples.

A post can have several photos (a Telegram album) — the text is the caption of the whole album.
Note how many photos posts use and how they work together.

For every new sample listed in the message, return an entry in `samples`: its id, a short description of the photo(s)
(empty string if there are no photos) and a 2–4 sentence analysis.

Write EVERYTHING (reply, guide, notes, analyses) in Uzbek, Latin script.
Format `reply` as plain text (no Markdown headings); the guide may use simple «- » bullet lists and lines ending with «:» as section titles.
"""

TRAINER_SCHEMA = {
    "type": "object",
    "properties": {
        "reply": {"type": "string"},
        "samples": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "image_desc": {"type": "string"},
                    "analysis": {"type": "string"},
                },
                "required": ["id", "image_desc", "analysis"],
                "additionalProperties": False,
            },
        },
        "guide": {"type": ["string", "null"]},
        "guide_note": {"type": ["string", "null"]},
    },
    "required": ["reply", "samples", "guide", "guide_note"],
    "additionalProperties": False,
}


RESPOND = "Reply to the editor's messages and samples that came after your last reply."


def guide_block(text: str | None) -> str:
    return f"CURRENT STYLE GUIDE:\n{text}" if text else "CURRENT STYLE GUIDE: (empty — nothing learned yet)"


def sample_block(sample_id: int, source: str, text: str, image_note: str | None, photos: int) -> str:
    parts = [f"--- NEW SAMPLE #{sample_id} ({source}) ---"]
    if photos == 1:
        parts.append("[1 photo attached below]")
    elif photos:
        parts.append(f"[album of {photos} photos attached below, in post order]")
    else:
        parts.append("[no photo]")
    if image_note:
        parts.append(f"Editor's description of the photos: {image_note}")
    parts.append(text or "(no text)")
    return "\n".join(parts)
