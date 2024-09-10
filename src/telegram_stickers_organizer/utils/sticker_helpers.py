from aiogram.types import InputSticker
from ..dispatcher import bot


async def get_bot_username():
    bot_info = await bot.get_me()
    return bot_info.username


def create_input_sticker(sticker) -> InputSticker:
    return InputSticker(
        sticker=sticker.file_id,
        emoji_list=[sticker.emoji],
        format=get_sticker_format(sticker),
    )


def get_sticker_format(sticker) -> str:
    if sticker.is_animated:
        return "animated"
    elif sticker.is_video:
        return "video"
    else:
        return "static"


async def is_sticker_set_owned_by_bot(sticker_set_name: str) -> bool:
    bot_username = await get_bot_username()
    return sticker_set_name.endswith(f"_by_{bot_username}")


async def get_sticker_set(sticker_set_name: str):
    return await bot.get_sticker_set(sticker_set_name)


async def add_stickers_to_set(user_id: int, set_name: str, stickers):
    for sticker in stickers:
        input_sticker = create_input_sticker(sticker)
        await bot.add_sticker_to_set(
            user_id=user_id,
            name=set_name,
            sticker=input_sticker,
        )
