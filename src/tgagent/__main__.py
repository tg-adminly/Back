import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.storage.memory import MemoryStorage

from tgagent.agents.giveaway.handlers import admin, editor, participant
from tgagent.agents.giveaway.jobs import draw_loop
from tgagent.channels.telegram_bot import tracking
from tgagent.channels.telegram_bot.chats import ChatRef, bot_is_admin, chat_link
from tgagent.config import Settings
from tgagent.core.crypto import Vault
from tgagent.core.db import init_db, make_engine, make_sessionmaker
from tgagent.panel import bot_login
from tgagent.panel.api import Deps
from tgagent.panel.auth import LoginRequests
from tgagent.panel.server import create_app, make_server, serve_panel

log = logging.getLogger("tgagent")


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = Settings()

    engine = make_engine(settings.database_url)
    await init_db(engine)
    sm = make_sessionmaker(engine)
    vault = Vault(settings.fernet_key)

    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        chat = await bot.get_chat(settings.main_chat_id)
    except TelegramBadRequest as e:
        await bot.session.close()
        await engine.dispose()
        raise SystemExit(
            f"MAIN_CHAT_ID={settings.main_chat_id} topilmadi ({e.message}).\n"
            "Tekshiring: 1) bot shu kanal/guruhga admin qilib qo'shilganmi; "
            "2) ID -100 bilan boshlanadimi va to'liq ko'chirilganmi."
        ) from None
    if not await bot_is_admin(bot, chat.id):
        log.warning("Bot asosiy kanal/guruhda admin emas — post chiqara olmaydi!")
    main_chat = ChatRef(chat.id, chat.title or "Kanal", await chat_link(bot, chat) or "")

    logins = LoginRequests()
    dp = Dispatcher(storage=MemoryStorage())
    # Tartib muhim: panelga kirish → egasi → muharrir → qolganlar (ishtirokchilar)
    dp.include_router(tracking.build_router())  # bot admin bo'lgan kanallarni eslab qoladi
    dp.include_router(bot_login.build_router(settings, logins))
    dp.include_router(admin.build_router(settings))
    dp.include_router(editor.build_router(settings))
    dp.include_router(participant.build_router(settings))

    app = create_app(Deps(settings, bot, sm, vault, main_chat, logins))
    panel = make_server(app, settings.panel_host, settings.panel_port)
    panel_task = asyncio.create_task(serve_panel(panel))
    log.info("Panel: %s", settings.panel_url)

    loop_task = asyncio.create_task(draw_loop(bot, sm, settings, main_chat))
    try:
        await dp.start_polling(
            bot,
            sm=sm,
            vault=vault,
            main_chat=main_chat,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        loop_task.cancel()
        panel.should_exit = True
        await panel_task
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
