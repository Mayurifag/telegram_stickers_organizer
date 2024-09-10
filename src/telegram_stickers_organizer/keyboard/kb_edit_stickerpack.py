from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_edit_stickerpack_inline_number = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="0", callback_data="0")]]
)

kb_edit_stickerpack_actions_for_sticker = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Remove sticker", callback_data="delete"),
            InlineKeyboardButton(text="Edit emoji", callback_data="edit_emoji"),
        ],
        [
            InlineKeyboardButton(text="Done", callback_data="done"),
            InlineKeyboardButton(text="Next", callback_data="next"),
        ],
    ]
)

kb_edit_stickerpack_actions_for_sticker_emoji = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Cancel edit", callback_data="cancel_emoji_edit")]
    ]
)
