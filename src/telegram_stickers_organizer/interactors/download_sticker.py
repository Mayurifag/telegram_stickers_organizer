import os
from telegram_stickers_organizer.dispatcher import bot

CACHE_DIR = "cached_stickers"


# TODO: cache folder limit
async def download_sticker(file_id: str):
    cache_file_path = os.path.join(CACHE_DIR, f"{file_id}.webp")

    if os.path.exists(cache_file_path):
        with open(cache_file_path, "rb") as f:
            return f.read()

    file = await bot.get_file(file_id)
    file_path = file.file_path

    os.makedirs(CACHE_DIR, exist_ok=True)  # Ensure the directory exists before writing

    await bot.download_file(file_path, cache_file_path)

    with open(cache_file_path, "rb") as f:
        return f.read()
