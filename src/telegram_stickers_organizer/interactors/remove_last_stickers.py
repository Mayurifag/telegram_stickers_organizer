from ..dispatcher import bot
from aiogram.exceptions import TelegramBadRequest
from ..utils.sticker_helpers import get_sticker_set


async def remove_last_stickers(sticker_set_name: str, number_to_remove: int):
    try:
        sticker_set = await get_sticker_set(sticker_set_name)
        stickers_to_remove = sticker_set.stickers[-number_to_remove:]

        for sticker in stickers_to_remove:
            await bot.delete_sticker_from_set(sticker.file_id)

        updated_set = await get_sticker_set(sticker_set_name)
        return True, updated_set
    except TelegramBadRequest as e:
        print(f"Telegram API error: {e}")
        return False, None
    except Exception as e:
        print(f"Unexpected error removing stickers from set: {e}")
        return False, None
