from ..dispatcher import bot


async def remove_last_stickers(sticker_set_name: str, number_to_remove: int):
    try:
        sticker_set = await bot.get_sticker_set(sticker_set_name)
        stickers_to_remove = sticker_set.stickers[-number_to_remove:]

        for sticker in stickers_to_remove:
            await bot.delete_sticker_from_set(sticker.file_id)

        updated_set = await bot.get_sticker_set(sticker_set_name)
        return True, updated_set
    except Exception as e:
        print(f"Error removing stickers from set: {e}")
        return False, None
