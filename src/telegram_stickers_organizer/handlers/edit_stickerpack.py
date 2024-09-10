from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, StickerSet
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from ..constants import EDIT_STICKERPACK_CALLBACK
from ..keyboard import kb_start
from ..keyboard.kb_edit_stickerpack import (
    kb_edit_stickerpack_inline_number,
    kb_edit_stickerpack_actions_for_sticker,
    kb_edit_stickerpack_actions_for_sticker_emoji,
)
from ..utils.sticker_helpers import is_sticker_set_owned_by_bot, get_sticker_set
from ..dispatcher import bot
import emoji

router = Router()


class EditStickerpackStates(StatesGroup):
    waiting_for_sticker = State()
    waiting_for_start_index = State()
    editing_sticker = State()
    waiting_for_emoji = State()


@router.callback_query(F.data == EDIT_STICKERPACK_CALLBACK)
async def edit_stickerpack_start(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer()
    await callback_query.message.edit_text(
        "Please send a sticker from the stickerset you want to edit."
    )
    await state.set_state(EditStickerpackStates.waiting_for_sticker)


@router.message(StateFilter(EditStickerpackStates.waiting_for_sticker))
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

        await state.update_data(sticker_set=sticker_set.name)
        await message.answer(
            f"From which sticker do you want to start editing? (0-{len(sticker_set.stickers) - 1})",
            reply_markup=kb_edit_stickerpack_inline_number,
        )
        await state.set_state(EditStickerpackStates.waiting_for_start_index)
    else:
        await message.answer("That's not a sticker! Please send a sticker.")


@router.message(StateFilter(EditStickerpackStates.waiting_for_start_index))
@router.callback_query(F.data == "0")
async def process_start_index(
    update: Message | CallbackQuery, state: FSMContext
) -> None:
    if isinstance(update, CallbackQuery):
        start_index = 0
        message = update.message
        await update.answer()
    elif isinstance(update, Message) and update.text and update.text.isdigit():
        start_index = int(update.text)
        message = update
    else:
        await update.answer("Please enter a valid number.")
        return

    data = await state.get_data()
    sticker_set_name = data["sticker_set"]
    sticker_set = await get_sticker_set(sticker_set_name)

    if 0 <= start_index < len(sticker_set.stickers):
        await state.update_data(current_index=start_index)
        await show_sticker(message, state, sticker_set, start_index)
    else:
        await message.answer("Invalid index. Please try again.")


async def show_sticker(
    update: Message | CallbackQuery,
    state: FSMContext,
    sticker_set: StickerSet,
    index: int,
):
    sticker = sticker_set.stickers[index]
    emoji = sticker.emoji if sticker.emoji else "No emoji"

    if isinstance(update, CallbackQuery):
        await update.message.answer_sticker(sticker.file_id)
        await update.message.answer(
            f"Sticker {index + 1}/{len(sticker_set.stickers)}. Its emoji: {emoji}",
            reply_markup=kb_edit_stickerpack_actions_for_sticker,
        )
        await update.answer()
    else:
        await update.answer_sticker(sticker.file_id)
        await update.answer(
            f"Sticker {index + 1}/{len(sticker_set.stickers)}. Its emoji: {emoji}",
            reply_markup=kb_edit_stickerpack_actions_for_sticker,
        )

    await state.set_state(EditStickerpackStates.editing_sticker)


@router.callback_query(StateFilter(EditStickerpackStates.editing_sticker))
async def process_edit_action(callback_query: CallbackQuery, state: FSMContext) -> None:
    action = callback_query.data
    data = await state.get_data()
    sticker_set_name = data["sticker_set"]
    current_index = data["current_index"]
    sticker_set = await get_sticker_set(sticker_set_name)

    if action == "delete":
        await bot.delete_sticker_from_set(sticker_set.stickers[current_index].file_id)
        sticker_set = await get_sticker_set(sticker_set_name)
        if current_index >= len(sticker_set.stickers):
            current_index = len(sticker_set.stickers) - 1
        await state.update_data(current_index=current_index)
        await show_sticker(callback_query.message, state, sticker_set, current_index)
    elif action == "edit_emoji":
        await callback_query.message.answer(
            "Please send the new single emoji for this sticker",
            reply_markup=kb_edit_stickerpack_actions_for_sticker_emoji,
        )
        await state.set_state(EditStickerpackStates.waiting_for_emoji)
    elif action == "next":
        if current_index < len(sticker_set.stickers) - 1:
            current_index += 1
            await state.update_data(current_index=current_index)
            await show_sticker(
                callback_query.message, state, sticker_set, current_index
            )
        else:
            await callback_query.message.answer(
                "You have reached the end of the sticker set.",
                reply_markup=kb_start.kb_menu,
            )
    elif action == "done":
        await callback_query.message.answer(
            "Editing done.", reply_markup=kb_start.kb_menu
        )
        await state.clear()
    else:
        await callback_query.answer("Unknown action")


@router.message(StateFilter(EditStickerpackStates.waiting_for_emoji))
@router.callback_query(F.data == "cancel_emoji_edit")
async def process_new_emoji(update: Message | CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    sticker_set_name = data["sticker_set"]
    current_index = data["current_index"]
    sticker_set = await get_sticker_set(sticker_set_name)
    sticker = sticker_set.stickers[current_index]

    if isinstance(update, Message):  # new emoji sent by user
        new_emoji = update.text.strip()
        if len(new_emoji) == 1 and new_emoji in emoji.UNICODE_EMOJI_ENGLISH:
            try:
                await bot.set_sticker_emoji_list(sticker.file_id, [new_emoji])
                await update.answer("Emoji updated successfully.")
                await show_sticker(update, state, sticker_set, current_index)
            except Exception as e:
                await update.answer(f"Error updating emoji: {str(e)}")
        else:
            await update.answer("Please send a single valid emoji.")
    elif update.data == "cancel_emoji_edit":
        await show_sticker(update, state, sticker_set, current_index)
