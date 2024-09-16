from ..utils.sticker_helpers import get_sticker_set, add_stickers_to_set
from ..dispatcher import bot
from ..constants import MAX_STICKERS_IN_STICKERSET
import logging


async def move_sticker_to_another_set(
    source_pack: str, destination_pack: str, file_id: str, user_id: int
):
    try:
        # Get the source sticker set
        source_set = await get_sticker_set(source_pack)

        # Find the sticker with the given file_id in the source set
        sticker = next((s for s in source_set.stickers if s.file_id == file_id), None)

        if not sticker:
            return False, "Sticker not found in the source pack"

        # Get the destination sticker set
        destination_set = await get_sticker_set(destination_pack)

        # Check if the destination pack is full
        if len(destination_set.stickers) >= MAX_STICKERS_IN_STICKERSET:
            return False, "Destination pack is full (maximum 120 stickers)"

        # Add the sticker to the destination pack
        await add_stickers_to_set(user_id, destination_pack, [sticker])

        # Remove the sticker from the source pack
        await bot.delete_sticker_from_set(file_id)

        return True, None
    except Exception as e:
        logging.error(f"Error moving sticker: {e}")
        return False, str(e)
