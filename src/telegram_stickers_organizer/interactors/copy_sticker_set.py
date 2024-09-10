import random
import string
from aiogram.exceptions import TelegramBadRequest
from ..utils.sticker_helpers import (
    get_bot_username,
    create_input_sticker,
    get_sticker_set,
    add_stickers_to_set,
)
from ..dispatcher import bot


async def copy_sticker_set(user_id: int, old_name: str, new_title: str):
    try:
        original_set = await get_sticker_set(old_name)
        new_set_name = await generate_new_set_name()

        await create_sticker_set(user_id, new_set_name, new_title, original_set)
        new_sticker_set = await get_sticker_set(new_set_name)
        return True, new_sticker_set
    except TelegramBadRequest as e:
        print(f"Telegram API error: {e}")
        return False, None
    except Exception as e:
        print(f"Unexpected error copying sticker set: {e}")
        return False, None


async def generate_new_set_name() -> str:
    bot_username = await get_bot_username()
    random_hash = "".join(random.choices(string.ascii_lowercase, k=10))
    return f"{random_hash}_by_{bot_username}"


async def create_sticker_set(
    user_id: int, new_set_name: str, new_title: str, original_set
):
    first_sticker = original_set.stickers[0]
    input_sticker = create_input_sticker(first_sticker)

    await bot.create_new_sticker_set(
        user_id=user_id,
        name=new_set_name,
        title=new_title,
        stickers=[input_sticker],
    )

    await add_stickers_to_set(user_id, new_set_name, original_set.stickers[1:])
