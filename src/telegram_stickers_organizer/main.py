import logging
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import aiohttp_cors
from telegram_stickers_organizer.config import WEBHOOK_PATH, HOST, PORT
from telegram_stickers_organizer.handlers import (
    start,
    message,
    rename_stickerset,
    merge_stickersets,
    remove_last_n_stickers,
    edit_stickerpack,
    add_stickers_to_stickerpack,
)
from telegram_stickers_organizer.dispatcher import dp, bot
from telegram_stickers_organizer.api.sticker_controller import (
    get_stickerpacks,
    get_stickerpack,
    delete_stickers,
    get_sticker,
    get_stickerpack_preview,
    get_all_sticker_sets,
    delete_sticker_set,
    move_sticker,
)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # message.router has to be last, because it is handler for messages which
    # were not handled by other routers
    dp.include_routers(
        start.router,
        rename_stickerset.router,
        merge_stickersets.router,
        remove_last_n_stickers.router,
        edit_stickerpack.router,
        add_stickers_to_stickerpack.router,
        message.router,
    )

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    app.add_routes(
        [
            web.get("/api/stickerpacks", get_stickerpacks),
            web.get("/api/stickerpack/{name}", get_stickerpack),
            web.post("/api/delete_stickers", delete_stickers),  # Add this line
            web.get("/api/sticker/{file_id}", get_sticker),
            web.get("/api/stickerpack/{name}/preview", get_stickerpack_preview),
            web.get("/api/all_sticker_sets", get_all_sticker_sets),
            web.post("/api/delete_sticker_set", delete_sticker_set),
            web.post("/api/move_sticker", move_sticker),
        ]
    )

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods=["GET", "POST", "OPTIONS"],
            )
        },
    )

    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    # TODO: decide if needed or not
    # asyncio.run(main())
    main()
