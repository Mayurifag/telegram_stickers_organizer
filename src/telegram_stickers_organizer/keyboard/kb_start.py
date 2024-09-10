from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..constants import (
    RENAME_STICKERSET_CALLBACK,
    RENAME_STICKERSET_TEXT,
    MERGE_STICKERSETS_CALLBACK,
    MERGE_STICKERSETS_TEXT,
    REMOVE_LAST_STICKERS_CALLBACK,
    REMOVE_LAST_STICKERS_TEXT,
    EDIT_STICKERPACK_CALLBACK,
    EDIT_STICKERPACK_TEXT,
    ADD_STICKERS_TO_STICKERPACK_CALLBACK,
    ADD_STICKERS_TO_STICKERPACK_TEXT,
)

kb_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=RENAME_STICKERSET_TEXT, callback_data=RENAME_STICKERSET_CALLBACK
            ),
        ],
        [
            InlineKeyboardButton(
                text=MERGE_STICKERSETS_TEXT, callback_data=MERGE_STICKERSETS_CALLBACK
            ),
        ],
        [
            InlineKeyboardButton(
                text=REMOVE_LAST_STICKERS_TEXT,
                callback_data=REMOVE_LAST_STICKERS_CALLBACK,
            ),
        ],
        [
            InlineKeyboardButton(
                text=EDIT_STICKERPACK_TEXT,
                callback_data=EDIT_STICKERPACK_CALLBACK,
            ),
        ],
        [
            InlineKeyboardButton(
                text=ADD_STICKERS_TO_STICKERPACK_TEXT,
                callback_data=ADD_STICKERS_TO_STICKERPACK_CALLBACK,
            ),
        ],
    ]
)
