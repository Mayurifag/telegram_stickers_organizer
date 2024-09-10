from aiogram import Router
from aiogram.types import Message
from ..keyboard import kb_start

router = Router()


@router.message()
async def echo_handler(message: Message) -> None:
    # if message.sticker:
    #     sticker_pack = (
    #         message.sticker.set_name if message.sticker.set_name else "Unknown"
    #     )
    #     await message.answer(f"Sticker from pack: <b>{sticker_pack}</b>")
    #     await message.answer_sticker(
    #         message.sticker.file_id, reply_markup=kb_start.kb_menu
    #     )  # Send the sticker back
    # elif (
    #     message.photo
    #     or message.animation
    #     or message.video
    #     or message.video_note
    #     or message.document
    # ):
    #     file = (
    #         message.document or message.photo[-1]
    #         if message.photo
    #         else message.animation or message.video or message.video_note
    #     )
    #     await message.answer_document(file.file_id, reply_markup=kb_start.kb_menu)
    # else:
    #     await message.answer("No handler for this type.", reply_markup=kb_start.kb_menu)

    await message.answer(
        "Bot doesnt support usage without commands", reply_markup=kb_start.kb_menu
    )
