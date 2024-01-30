from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminStates(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    count = State()
    finish = State()

class AdminInfoStates(StatesGroup):
    tlf = State()
    FIO = State()
    operating_mode = State()
    delivery = State()
    finish = State()


