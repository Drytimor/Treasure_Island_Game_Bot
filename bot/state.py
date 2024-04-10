from aiogram.fsm.state import StatesGroup, State


class ExchangeTris(StatesGroup):
    exchange_gold = State()


class BetOnTeam(StatesGroup):
    bid = State()

