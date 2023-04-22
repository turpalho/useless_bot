from aiogram.fsm.state import State, StatesGroup


class WeatherState(StatesGroup):
    waiting_enter_city = State()


class CurrencyState(StatesGroup):
    waiting_enter_from_currency = State()
    waiting_enter_to_currency = State()


class PollsState(StatesGroup):
    waiting_question = State()
    waiting_options = State()
