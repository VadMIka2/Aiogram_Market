from aiogram.fsm.state import StatesGroup, State

class GameState(StatesGroup):
    gameName = State()
    descriptGame = State()
    priceGame = State()
    statusGame = State()