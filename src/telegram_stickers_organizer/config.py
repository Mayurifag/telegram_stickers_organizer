from decouple import config

BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST")
PORT = config("PORT", cast=int)
BASE_URL = config("BASE_URL")
ADMIN_ID = config("ADMIN_ID", cast=int)
WEBHOOK_PATH = f"/{BOT_TOKEN}"
