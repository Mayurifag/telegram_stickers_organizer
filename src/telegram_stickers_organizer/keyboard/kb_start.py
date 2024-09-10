from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .constants import FILM_SPIZDILI_CALLBACK, FILM_SPIZDILI_TEXT

kb_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=FILM_SPIZDILI_TEXT, callback_data=FILM_SPIZDILI_CALLBACK
            ),
        ]
    ]
)
