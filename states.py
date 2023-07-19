from aiogram.dispatcher.filters.state import State, StatesGroup


class NextStep(StatesGroup):
    step_two = State()
