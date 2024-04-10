import logging
from datetime import datetime, timedelta
from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import suppress
from aiogram.fsm.context import FSMContext
from state import (
    ExchangeTris,
    BetOnTeam
)
from keyboards import (
    get_choices_team_kb,
    main_menu_kb,
    get_wallet_kb,
    get_back_wallet_kb,
    get_back_bet_on_team
)
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from services import (
    create_user,
    get_user,
    get_well_tris,
    exchange_tris_for_gold,
    create_a_bit,
    get_total_amount_gold_teams,
    sending_result_to_users
)


log = logging.getLogger(__name__)


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message | CallbackQuery):
    await create_user(message.from_user.id, message.from_user.username)
    await message.answer(
        text='Описание',
        reply_markup=main_menu_kb()
    )


@router.callback_query(F.data == "start_game")
async def choices_team(callback: CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    time = scheduler.get_jobs()[0].next_run_time
    # time_game = datetime(year=time.year, month=time.month, day=time.day, hour=time.hour, minute=time.minute, second=time.second)
    time_game = datetime(**time)
    log.info(f'time_game {time_game}')
    time_game_delta = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    current_time = datetime.now()
    current_time_delta = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
    next_time_game = time_game_delta - current_time_delta
    await state.clear()
    total_amount_gold = await get_total_amount_gold_teams()
    await callback.message.edit_text(
        f"Сражение начнется через {next_time_game}"
        f"Собрано золота: {round(total_amount_gold, 4)}\n"
        f"Выберете команду\n",
        reply_markup=get_choices_team_kb()
    )
    await callback.answer()


@router.callback_query(
    StateFilter(None),
    F.data.in_({'Berberes', 'Tartugi', 'Jamajki'})
)
async def start_game_for_team(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    await state.update_data(team=callback.data)
    await callback.message.edit_text(
        f'Если команда победит вы получите награду\n'
        f'доступно: {user.gold}\n'
        f'Введите количество золота:\n',
        reply_markup=get_back_bet_on_team()
    )
    await state.set_state(BetOnTeam.bid)


@router.message(BetOnTeam.bid, F.text.regexp(r'^[0-9]*[.,]?[0-9]+$'))
async def make_a_bit(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    result = await create_a_bit(
        user_id=message.from_user.id,
        team=data['team'],
        amount_gold=message.text
    )
    if result:
        await message.answer('Успех', reply_markup=get_back_bet_on_team())
    else:
        await message.answer('Что то пошло не так')


@router.callback_query(F.data == "wallet")
async def get_wallet(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user = await get_user(callback.from_user.id)
    well = await get_well_tris()
    await callback.message.edit_text(
        f"Курс: 1 Tris - {round(well, 2)} gold\n"
        f"Tris: {round(user.tris, 4)}\n"
        f"Gold: {round(user.gold, 4)}\n"
        f"Farm: {round(user.farm_gold, 4)}\n",
        reply_markup=get_wallet_kb()
    )


@router.callback_query(StateFilter(None), F.data == "tris_exchange")
async def exchange_tris_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ExchangeTris.exchange_gold)
    await callback.message.edit_text(
        'Введите количество Tris', reply_markup=get_back_wallet_kb()
    )


@router.message(ExchangeTris.exchange_gold, F.text.regexp(r'^[0-9]*[.,]?[0-9]+$'))
async def exchange_gold(message: Message, state: FSMContext):
    await state.clear()
    result = await exchange_tris_for_gold(message.text, message.from_user.id)
    if result:
        await message.answer('Успех', reply_markup=get_back_wallet_kb())
    else:
        await message.answer('Что то пошло не так')


@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text='Описание',
        reply_markup=main_menu_kb()
    )


