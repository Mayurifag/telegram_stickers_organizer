from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from telegram_stickers_organizer.config import (
    BASE_URL,
    WEBHOOK_PATH,
    BOT_TOKEN,
)
from telegram_stickers_organizer.middlewares.auth_middleware import AuthMiddleware


async def set_commands() -> None:
    commands = [BotCommand(command="start", description="Start")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup() -> None:
    await set_commands()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")


async def on_shutdown() -> None:
    await bot.session.close()
    await bot.delete_webhook(drop_pending_updates=True)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)
dp.message.middleware(AuthMiddleware())
dp.callback_query.middleware(AuthMiddleware())
