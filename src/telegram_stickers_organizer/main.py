import logging
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from telegram_stickers_organizer.config import WEBHOOK_PATH, HOST, PORT
from telegram_stickers_organizer.handlers import start, message, rename_stickerset
from telegram_stickers_organizer.dispatcher import dp, bot


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
        message.router,
    )

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    # TODO: decide if needed or not
    # asyncio.run(main())
    main()
