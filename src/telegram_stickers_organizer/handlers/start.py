from aiogram.filters import CommandStart
from aiogram.types import Message
from ..keyboard import kb_start
from aiogram import Router

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.delete()  # Remove user's /start message
    await message.answer(
        "Бот работает, выберите команду", reply_markup=kb_start.kb_menu
    )
