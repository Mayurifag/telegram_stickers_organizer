from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_add_stickers_to_stickerpack_actions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Done", callback_data="add_stickers_done"),
            InlineKeyboardButton(
                text="Remove previous sticker",
                callback_data="remove_previous_sticker",
            ),
        ]
    ]
)
