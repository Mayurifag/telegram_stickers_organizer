from decouple import config

BOT_TOKEN = config("BOT_TOKEN")
HOST = config("HOST")
PORT = config("PORT", cast=int)
BASE_URL = config("BASE_URL")
WEBHOOK_PATH = f"/{BOT_TOKEN}"
ALLOWED_USER_IDS = [int(id) for id in config("ALLOWED_USER_IDS", cast=str).split(",")]
