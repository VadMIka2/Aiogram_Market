from aiogram.fsm.state import StatesGroup, State

class RegisterSate(StatesGroup):
    regName_steam = State()
    reset_steam = State()