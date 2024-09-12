from aiohttp import web
from telegram_stickers_organizer.repositories.stickers_repository import (
    db_get_all_sticker_sets,
    db_delete_sticker_set,
)
from telegram_stickers_organizer.utils.sticker_helpers import get_sticker_set
from telegram_stickers_organizer.dispatcher import bot
from telegram_stickers_organizer.interactors.download_sticker import download_sticker


async def get_stickerpacks(request):
    sticker_packs = db_get_all_sticker_sets()
    return web.json_response(sticker_packs)


async def get_stickerpack(request):
    set_name = request.match_info["set_name"]
    sticker_set = await get_sticker_set(set_name)
    return web.json_response(
        {
            "name": sticker_set.name,
            "title": sticker_set.title,
            "stickers": [
                {"file_id": sticker.file_id, "emoji": sticker.emoji}
                for sticker in sticker_set.stickers
            ],
        }
    )


# TODO: remove from cache
async def delete_stickers(request):
    data = await request.json()
    file_ids = data.get("file_ids", [])
    results = []
    for file_id in file_ids:
        try:
            await bot.delete_sticker_from_set(file_id)
            results.append({"file_id": file_id, "success": True})
        except Exception as e:
            results.append({"file_id": file_id, "success": False, "error": str(e)})
    return web.json_response({"results": results})


# TODO: content type webp -> anything actually. Download sticker has to return content_type
async def get_sticker(request):
    file_id = request.match_info["file_id"]
    file_content = await download_sticker(file_id)
    return web.Response(body=file_content, content_type="image/webp")


async def get_stickerpack_preview(request):
    set_name = request.match_info["set_name"]
    sticker_set = await get_sticker_set(set_name)
    first_sticker = sticker_set.stickers[0]
    file_content = await download_sticker(first_sticker.file_id)
    return web.Response(body=file_content, content_type="image/webp")


async def get_all_sticker_sets(request):
    sticker_sets = db_get_all_sticker_sets()
    return web.json_response(sticker_sets)


async def delete_sticker_set(request):
    data = await request.json()
    set_name = data.get("set_name")
    if not set_name:
        return web.json_response(
            {"success": False, "error": "set_name is required"}, status=400
        )

    success = db_delete_sticker_set(set_name)
    return web.json_response({"success": success})
