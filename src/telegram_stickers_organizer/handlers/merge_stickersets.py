from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, StickerSet
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from ..constants import MERGE_STICKERSETS_CALLBACK, MAX_STICKERS_IN_STICKERSET
from ..dispatcher import bot
from ..keyboard import kb_start
from ..interactors.merge_sticker_sets import merge_sticker_sets
from ..utils.sticker_helpers import is_sticker_set_owned_by_bot, get_sticker_set

router = Router()


class MergeStates(StatesGroup):
    waiting_for_first_sticker = State()
    waiting_for_second_sticker = State()


@router.callback_query(F.data == MERGE_STICKERSETS_CALLBACK)
async def merge_stickersets(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await callback_query.message.answer(
        "Please send a sticker from the first stickerset."
    )
    await state.set_state(MergeStates.waiting_for_first_sticker)


@router.message(StateFilter(MergeStates.waiting_for_first_sticker))
async def process_first_sticker(message: Message, state: FSMContext) -> None:
    if message.sticker:
        sticker_set = await get_sticker_set(message.sticker.set_name)
        if not await is_sticker_set_owned_by_bot(sticker_set.name):
            await message.answer(
                "Error: The first stickerset must be created/renamed by this bot. Please try again.",
                reply_markup=kb_start.kb_menu,
            )
            await state.clear()
            return

        first_sticker_count = len(sticker_set.stickers)
        await state.update_data(first_sticker_set=sticker_set.name)
        await message.answer(
            f"First stickerpack has <b>{first_sticker_count}</b> stickers. "
            f"Now, please send a sticker from the second stickerset. "
            f"It must be less than {MAX_STICKERS_IN_STICKERSET - first_sticker_count} stickers."
        )
        await state.set_state(MergeStates.waiting_for_second_sticker)
    else:
        await message.answer("That's not a sticker! Please send a sticker.")


@router.message(StateFilter(MergeStates.waiting_for_second_sticker))
async def process_second_sticker(message: Message, state: FSMContext) -> None:
    if message.sticker:
        data = await state.get_data()
        first_sticker_set = data.get("first_sticker_set")
        second_sticker_set = message.sticker.set_name

        if first_sticker_set == second_sticker_set:
            await message.answer(
                "Error: You can't merge a stickerset with itself. Please try again.",
                reply_markup=kb_start.kb_menu,
            )
            await state.clear()
            return

        first_set = await bot.get_sticker_set(first_sticker_set)
        second_set = await bot.get_sticker_set(second_sticker_set)

        first_set_sticker_count = len(first_set.stickers)
        second_set_sticker_count = len(second_set.stickers)
        combined_sticker_count = first_set_sticker_count + second_set_sticker_count

        if combined_sticker_count > MAX_STICKERS_IN_STICKERSET:
            await message.answer(
                f"Error: The first stickerset has {first_set_sticker_count} stickers, "
                f"the second stickerset has {second_set_sticker_count} stickers, "
                f"and the combined total is {combined_sticker_count}. "
                "Please try again with smaller stickersets.",
                reply_markup=kb_start.kb_menu,
            )
            await state.clear()
            return

        await message.answer(
            f"The second stickerset has <b>{second_set_sticker_count}</b> stickers. "
            f"Merging stickersets, please wait, dont send any messages for a while..."
        )
        success, merged_set = await merge_sticker_sets(
            message.from_user.id, first_sticker_set, second_sticker_set
        )

        if success and isinstance(merged_set, StickerSet):
            await message.answer(
                f"Stickersets '{first_sticker_set}' and '{second_sticker_set}' have been successfully merged into '{merged_set.name}'."
            )
            await message.answer_sticker(
                merged_set.stickers[0].file_id, reply_markup=kb_start.kb_menu
            )
        else:
            await message.answer(
                "Sorry, there was an error merging the stickersets. Please try again later.",
                reply_markup=kb_start.kb_menu,
            )
    else:
        await message.answer("That's not a sticker! Please send a sticker.")

    await state.clear()
