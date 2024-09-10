from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from telegram_stickers_organizer.config import ALLOWED_USER_IDS


class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = (
            event.from_user.id if isinstance(event, (Message, CallbackQuery)) else None
        )

        if user_id not in ALLOWED_USER_IDS:
            if isinstance(event, Message):
                await event.answer("You are not authorized to use this bot.")
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "You are not authorized to use this bot.", show_alert=True
                )
            return

        return await handler(event, data)
