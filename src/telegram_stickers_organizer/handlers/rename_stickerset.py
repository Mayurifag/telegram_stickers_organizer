from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, StickerSet
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from ..constants import RENAME_STICKERSET_CALLBACK
from ..keyboard import kb_start
from ..interactors.copy_sticker_set import copy_sticker_set

router = Router()


class RenameStates(StatesGroup):
    waiting_for_sticker = State()
    waiting_for_new_title = State()


@router.callback_query(F.data == RENAME_STICKERSET_CALLBACK)
async def rename_stickerset(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await callback_query.message.edit_text("Please send a sticker from any stickerset.")
    await state.set_state(RenameStates.waiting_for_sticker)


@router.message(StateFilter(RenameStates.waiting_for_sticker))
async def process_sticker(message: Message, state: FSMContext) -> None:
    if message.sticker:
        sticker_pack = (
            message.sticker.set_name if message.sticker.set_name else "Unknown"
        )
        await state.update_data(sticker_pack=sticker_pack)
        await message.answer(
            "Enter the new name for the sticker pack. Do not use HTML tags."
        )
        await state.set_state(RenameStates.waiting_for_new_title)
    else:
        await message.answer("That's not a sticker! Please send a sticker.")


@router.message(StateFilter(RenameStates.waiting_for_new_title))
async def process_new_title(message: Message, state: FSMContext) -> None:
    new_title = message.text
    data = await state.get_data()
    sticker_pack = data.get("sticker_pack")

    await message.answer("Данные получены, начинаем копирование, надо подождать...")
    success, new_sticker_set = await copy_sticker_set(
        message.from_user.id, sticker_pack, new_title
    )

    if success and isinstance(new_sticker_set, StickerSet):
        await message.answer_sticker(new_sticker_set.stickers[0].file_id)
        await message.answer(
            f"Sticker pack <b>{sticker_pack}</b> has been copied to a new pack named "
            f"'<b>{new_sticker_set.name}</b>' with title '<b>{new_title}</b>'.",
            reply_markup=kb_start.kb_menu,
        )
    else:
        await message.answer(
            "Sorry, there was an error creating the new sticker pack. Please try again later."
        )
    await state.clear()
