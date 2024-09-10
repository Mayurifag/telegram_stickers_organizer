from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, StickerSet
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from ..constants import REMOVE_LAST_STICKERS_CALLBACK
from ..keyboard import kb_start
from ..interactors.remove_last_stickers import remove_last_stickers
from ..utils.sticker_helpers import is_sticker_set_owned_by_bot, get_sticker_set

router = Router()


class RemoveLastStickersStates(StatesGroup):
    waiting_for_sticker = State()
    waiting_for_number = State()


@router.callback_query(F.data == REMOVE_LAST_STICKERS_CALLBACK)
async def remove_last_stickers_start(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer()
    await callback_query.message.edit_text(
        "Please send a sticker from the stickerset you want to modify."
    )
    await state.set_state(RemoveLastStickersStates.waiting_for_sticker)


@router.message(StateFilter(RemoveLastStickersStates.waiting_for_sticker))
async def process_sticker(message: Message, state: FSMContext) -> None:
    if message.sticker:
        sticker_set = await get_sticker_set(message.sticker.set_name)
        if not await is_sticker_set_owned_by_bot(sticker_set.name):
            await message.answer(
                "Error: The stickerset must be created/renamed by this bot. Please try again.",
                reply_markup=kb_start.kb_menu,
            )
            await state.clear()
            return

        sticker_count = len(sticker_set.stickers)
        await state.update_data(
            sticker_set=sticker_set.name, sticker_count=sticker_count
        )
        await message.answer(
            f"This stickerset has {sticker_count} stickers. How many last stickers do you want to remove?"
        )
        await state.set_state(RemoveLastStickersStates.waiting_for_number)
    else:
        await message.answer("That's not a sticker! Please send a sticker.")


@router.message(StateFilter(RemoveLastStickersStates.waiting_for_number))
async def process_number(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        number = int(message.text)
        data = await state.get_data()
        sticker_set_name = data["sticker_set"]
        sticker_count = data["sticker_count"]

        if number >= sticker_count:
            await message.answer(
                f"Error: You can't remove {number} stickers from a set with {sticker_count} stickers. Please try again with a smaller number.",
                reply_markup=kb_start.kb_menu,
            )
            await state.clear()
            return

        await message.answer(
            f"Removing last {number} stickers from the set. Please wait..."
        )
        success, updated_set = await remove_last_stickers(sticker_set_name, number)

        if success and isinstance(updated_set, StickerSet):
            remaining_stickers = len(updated_set.stickers)
            await message.answer(
                f"Successfully removed {number} stickers. The set now has {remaining_stickers} stickers."
            )
            await message.answer_sticker(
                updated_set.stickers[0].file_id, reply_markup=kb_start.kb_menu
            )
        else:
            await message.answer(
                "Sorry, there was an error removing stickers from the set. Please try again later.",
                reply_markup=kb_start.kb_menu,
            )
    else:
        await message.answer("Please enter a valid number.")

    await state.clear()
