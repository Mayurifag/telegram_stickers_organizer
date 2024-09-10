from aiogram import Bot, Dispatcher
import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from telegram_stickers_organizer.config import (
    BASE_URL,
    WEBHOOK_PATH,
    # ADMIN_ID,
    BOT_TOKEN,
)


async def set_commands() -> None:
    commands = [BotCommand(command="start", description="Start")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup() -> None:
    await set_commands()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    # await asyncio.sleep(1)
    # startup_message = await bot.send_message(chat_id=ADMIN_ID, text="Bot startup event")
    # await bot.delete_message(chat_id=ADMIN_ID, message_id=startup_message.message_id)


async def on_shutdown() -> None:
    # shutdown_message = await bot.send_message(chat_id=ADMIN_ID, text="Bot stop event")
    await bot.delete_webhook(drop_pending_updates=True)
    # await asyncio.sleep(1)
    # await bot.delete_message(chat_id=ADMIN_ID, message_id=shutdown_message.message_id)
    await bot.session.close()


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)
