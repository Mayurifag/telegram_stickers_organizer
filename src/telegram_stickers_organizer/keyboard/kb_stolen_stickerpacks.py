from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..repositories.stickers_repository import db_get_user_sticker_sets


def kb_stolen_stickerpacks(user_id: int) -> InlineKeyboardMarkup:
    sticker_sets = db_get_user_sticker_sets(user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=set_info["title"],
                    callback_data=f"select_set:{set_info['set_name']}",
                )
            ]
            for set_info in sticker_sets
        ]
    )
    return keyboard
