from aiogram.types import InputSticker
from ..dispatcher import bot
import random
import string


async def copy_sticker_set(user_id: int, old_name: str, new_title: str):
    try:
        bot_username = await get_bot_username()
        original_set = await bot.get_sticker_set(old_name)
        new_set_name = generate_new_set_name(bot_username)

        await create_sticker_set(user_id, new_set_name, new_title, original_set)
        new_sticker_set = await bot.get_sticker_set(new_set_name)
        return True, new_sticker_set
    except Exception as e:
        print(f"Error copying sticker set: {e}")
        return False, None


async def get_bot_username():
    bot_info = await bot.get_me()
    return bot_info.username


def generate_new_set_name(bot_username: str) -> str:
    random_hash = generate_random_hash()
    return f"{random_hash}_by_{bot_username}"


async def create_sticker_set(
    user_id: int, new_set_name: str, new_title: str, original_set
) -> None:
    first_sticker = original_set.stickers[0]
    input_sticker = create_input_sticker(first_sticker)

    await bot.create_new_sticker_set(
        user_id=user_id,
        name=new_set_name,
        title=new_title,
        stickers=[input_sticker],
    )

    await add_remaining_stickers(user_id, new_set_name, original_set.stickers[1:])


async def add_remaining_stickers(user_id: int, new_set_name: str, stickers) -> None:
    for sticker in stickers:
        input_sticker = create_input_sticker(sticker)
        await bot.add_sticker_to_set(
            user_id=user_id,
            name=new_set_name,
            sticker=input_sticker,
        )


def create_input_sticker(sticker) -> InputSticker:
    return InputSticker(
        sticker=sticker.file_id,
        emoji_list=[sticker.emoji],
        format=get_sticker_format(sticker),
    )


def generate_random_hash(length=10) -> str:
    """Generate a random hash of English letters."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def get_sticker_format(sticker) -> str:
    if sticker.is_animated:
        return "animated"
    elif sticker.is_video:
        return "video"
    else:
        return "static"
