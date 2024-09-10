from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_edit_stickerpack_inline_number = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="0", callback_data="0")]]
)

kb_edit_stickerpack_actions_for_sticker = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Delete", callback_data="delete")],
        [InlineKeyboardButton(text="Edit emoji", callback_data="edit_emoji")],
        [InlineKeyboardButton(text="Next", callback_data="next")],
        [InlineKeyboardButton(text="Done", callback_data="done")],
    ]
)
