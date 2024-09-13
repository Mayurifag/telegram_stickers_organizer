import os
import mimetypes
from telegram_stickers_organizer.dispatcher import bot
import gzip
import aiofiles

CACHE_DIR = "cached_stickers"


# TODO: cache folder limit
async def download_sticker(file_id: str):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_extension = os.path.splitext(file_path)[1]
    cache_file_path = os.path.join(CACHE_DIR, f"{file_id}{file_extension}")

    os.makedirs(CACHE_DIR, exist_ok=True)

    if not os.path.exists(cache_file_path):
        await bot.download_file(file_path, cache_file_path)

    if file_extension.lower() == ".tgs":
        file_extension = ".json"
        cache_file_path = await cached_convert_tgs_to_json(cache_file_path)

    with open(cache_file_path, "rb") as f:
        content = f.read()
    content_type = (
        mimetypes.guess_type(cache_file_path)[0] or "application/octet-stream"
    )

    return content, content_type


async def cached_convert_tgs_to_json(file_path: str) -> str:
    # Asynchronously open the .tgs file (gzipped Lottie)
    json_file_path = f"{os.path.splitext(file_path)[0]}.json"
    if not os.path.exists(json_file_path):
        async with aiofiles.open(file_path, mode="rb") as f:
            # Read the binary gzipped data
            tgs_data = await f.read()
        # Decompress the .tgs file (which is gzipped)
        decompressed_data = gzip.decompress(tgs_data)

        async with aiofiles.open(json_file_path, mode="w") as json_file:
            await json_file.write(decompressed_data.decode("utf-8"))

    return json_file_path
