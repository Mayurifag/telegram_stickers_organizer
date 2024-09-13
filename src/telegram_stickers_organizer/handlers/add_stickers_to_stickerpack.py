from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from ..constants import ADD_STICKERS_TO_STICKERPACK_CALLBACK
from ..keyboard import kb_start
from ..keyboard.kb_add_stickers_to_stickerpack import (
    kb_add_stickers_to_stickerpack_actions,
)
from ..utils.sticker_helpers import add_stickers_to_set, get_sticker_set
from ..dispatcher import bot
from ..keyboard.kb_stolen_stickerpacks import kb_stolen_stickerpacks

router = Router()


class AddStickersStates(StatesGroup):
    choosing_stickerpack = State()
    adding_stickers = State()


@router.callback_query(F.data == ADD_STICKERS_TO_STICKERPACK_CALLBACK)
async def add_stickers_start(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    user_id = callback_query.from_user.id
    keyboard = kb_stolen_stickerpacks(user_id)

    await callback_query.message.edit_text(
        "Choose a sticker set to add stickers to:", reply_markup=keyboard
    )
    await state.set_state(AddStickersStates.choosing_stickerpack)


@router.callback_query(
    StateFilter(AddStickersStates.choosing_stickerpack),
    F.data.startswith("select_set:"),
)
async def process_stickerpack_selection(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    set_name = callback_query.data.split(":", 1)[1]
    sticker_set = await get_sticker_set(set_name)
    await state.update_data(current_set=set_name)
    # TODO: add button to cancel adding stickers
    await callback_query.message.edit_text(
        f"Please send a sticker to add to the set {sticker_set.title}."
    )
    await state.set_state(AddStickersStates.adding_stickers)


@router.message(StateFilter(AddStickersStates.adding_stickers))
async def process_sticker(message: Message, state: FSMContext) -> None:
    if not message.sticker:
        await message.answer("That's not a sticker! Please send a sticker.")
        return

    data = await state.get_data()
    set_name = data["current_set"]
    user_id = message.from_user.id

    try:
        await add_stickers_to_set(user_id, set_name, [message.sticker])
        sticker_set = await get_sticker_set(set_name)
        await message.answer_sticker(sticker_set.stickers[-1].file_id)
        sticker_count = len(sticker_set.stickers)

        await message.answer(
            f"Sticker added successfully. The set '{sticker_set.title}' now "
            f"has <b>{sticker_count}/120</b> stickers.\n"
            "Send another sticker to add, or use the buttons below.",
            reply_markup=kb_add_stickers_to_stickerpack_actions,
        )
    except Exception as e:
        await message.answer(f"Error adding sticker: {str(e)}")


@router.callback_query(
    StateFilter(AddStickersStates.adding_stickers), F.data == "add_stickers_done"
)
async def finish_adding_stickers(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer()
    data = await state.get_data()
    set_name = data["current_set"]
    sticker_set = await get_sticker_set(set_name)
    await callback_query.message.edit_text(
        f"Finished adding stickers to the set: {sticker_set.title}.",
        reply_markup=kb_start.kb_menu,
    )
    await state.clear()


@router.callback_query(
    StateFilter(AddStickersStates.adding_stickers), F.data == "remove_previous_sticker"
)
async def remove_previous_sticker(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer()
    data = await state.get_data()
    set_name = data["current_set"]

    try:
        sticker_set = await get_sticker_set(set_name)
        if len(sticker_set.stickers) > 0:
            last_sticker = sticker_set.stickers[-1]
            await bot.delete_sticker_from_set(last_sticker.file_id)
            sticker_set = await get_sticker_set(set_name)
            sticker_count = len(sticker_set.stickers)
            await callback_query.message.answer_sticker(
                sticker_set.stickers[-1].file_id
            )
            await callback_query.message.answer(
                f"Previous sticker removed from the set '{sticker_set.title}'. "
                f"The set now has {sticker_count}/120 stickers.\n"
                "Send another sticker to add it.",
                reply_markup=callback_query.message.reply_markup,
            )
        else:
            await callback_query.message.answer("No stickers to remove.")
    except Exception as e:
        await callback_query.message.answer(f"Error removing sticker: {str(e)}")
