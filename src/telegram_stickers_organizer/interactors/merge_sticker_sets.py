from aiogram.exceptions import TelegramBadRequest
from ..utils.sticker_helpers import (
    get_sticker_set,
    add_stickers_to_set,
)


async def merge_sticker_sets(user_id: int, first_set_name: str, second_set_name: str):
    try:
        second_set = await get_sticker_set(second_set_name)
        await add_stickers_to_set(user_id, first_set_name, second_set.stickers)
        merged_set = await get_sticker_set(first_set_name)
        return True, merged_set
    except TelegramBadRequest as e:
        print(f"Telegram API error: {e}")
        return False, None
    except Exception as e:
        print(f"Unexpected error merging sticker sets: {e}")
        return False, None
