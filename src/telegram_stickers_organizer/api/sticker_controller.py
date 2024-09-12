from aiohttp import web
from telegram_stickers_organizer.repositories.stickers_repository import (
    db_get_all_sticker_sets,
    db_delete_sticker_set,
    db_get_user_id_by_set_name,
)
from telegram_stickers_organizer.utils.sticker_helpers import (
    get_sticker_set,
    add_stickers_to_set,
)
from telegram_stickers_organizer.dispatcher import bot
from telegram_stickers_organizer.interactors.download_sticker import download_sticker
import logging


async def get_stickerpacks(request):
    sticker_packs = db_get_all_sticker_sets()

    response_data = [
        {
            "user_id": sticker_set["user_id"],
            "name": sticker_set["set_name"],
            "title": sticker_set["title"],
        }
        for sticker_set in sticker_packs
    ]
    return web.json_response(response_data)


async def get_stickerpack(request):
    set_name = request.match_info["name"]
    sticker_set = await get_sticker_set(set_name)
    user_id = db_get_user_id_by_set_name(set_name)
    return web.json_response(
        {
            "user_id": user_id,
            "name": sticker_set.name,
            "title": sticker_set.title,
            "stickers": [
                {
                    "file_id": sticker.file_id,
                    "emoji": sticker.emoji,
                    "is_animated": sticker.is_animated,
                    "is_video": sticker.is_video,
                }
                for sticker in sticker_set.stickers
            ],
        }
    )


# TODO: remove from cache
# TODO: this should be done in the background -> and endpoints should support that
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


async def get_sticker(request):
    file_id = request.match_info["file_id"]
    file_content, content_type = await download_sticker(file_id)
    return web.Response(body=file_content, content_type=content_type)


async def get_stickerpack_preview(request):
    set_name = request.match_info["name"]
    sticker_set = await get_sticker_set(set_name)
    first_sticker = sticker_set.stickers[0]
    file_content, content_type = await download_sticker(first_sticker.file_id)
    return web.Response(body=file_content, content_type=content_type)


async def get_all_sticker_sets(request):
    sticker_sets = db_get_all_sticker_sets()
    return web.json_response(sticker_sets)


async def delete_sticker_set(request):
    data = await request.json()
    set_name = data.get("name")
    if not set_name:
        return web.json_response(
            {"success": False, "error": "name is required"}, status=400
        )

    success = db_delete_sticker_set(set_name)
    return web.json_response({"success": success})


async def move_sticker(request):
    data = await request.json()
    source_pack = data.get("source_pack")
    destination_pack = data.get("destination_pack")
    file_id = data.get("file_id")
    user_id = data.get("user_id")

    if not all([source_pack, destination_pack, file_id]):
        return web.json_response(
            {
                "success": False,
                "error": "source_pack, destination_pack, and file_id are required",
            },
            status=400,
        )

    try:
        # Get the source sticker set
        source_set = await get_sticker_set(source_pack)

        # Find the sticker with the given file_id in the source set
        sticker = next((s for s in source_set.stickers if s.file_id == file_id), None)

        if not sticker:
            return web.json_response(
                {"success": False, "error": "Sticker not found in the source pack"},
                status=404,
            )

        # Add the sticker to the destination pack
        await add_stickers_to_set(user_id, destination_pack, [sticker])

        # Remove the sticker from the source pack
        await bot.delete_sticker_from_set(file_id)

        return web.json_response({"success": True})
    except Exception as e:
        logging.error(f"Error moving sticker: {e}")
        return web.json_response({"success": False, "error": str(e)}, status=500)
