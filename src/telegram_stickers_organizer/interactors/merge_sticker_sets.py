from aiogram.types import InputSticker
from ..dispatcher import bot


async def merge_sticker_sets(user_id: int, first_set_name: str, second_set_name: str):
    try:
        second_set = await bot.get_sticker_set(second_set_name)

        for sticker in second_set.stickers:
            input_sticker = InputSticker(
                sticker=sticker.file_id,
                emoji_list=[sticker.emoji],
                format=get_sticker_format(sticker),
            )
            await bot.add_sticker_to_set(
                user_id=user_id,
                name=first_set_name,
                sticker=input_sticker,
            )

        merged_set = await bot.get_sticker_set(first_set_name)
        return True, merged_set
    except Exception as e:
        print(f"Error merging sticker sets: {e}", exc_info=True)
        return False, None


def get_sticker_format(sticker) -> str:
    if sticker.is_animated:
        return "animated"
    elif sticker.is_video:
        return "video"
    else:
        return "static"
