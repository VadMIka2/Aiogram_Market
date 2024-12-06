from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.database import Database


# Кнопка для регестрации
un_reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать регестрацию', callback_data='reg')]
])

# Кнокпа для зарегестрированных пользователей
reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог игр', callback_data='catalog')],
    [InlineKeyboardButton(text='Профиль', callback_data='profile')]
])

# Кнопка для профиля
profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить логин Steam', callback_data='reset_steam'), 
     InlineKeyboardButton(text='Корзина', callback_data='basket')],
    [InlineKeyboardButton(text='На главную', callback_data='to_main')]
])

# Кнопка для покупки игры
game_buy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить все', callback_data='buy_all'), 
    InlineKeyboardButton(text='Профиль', callback_data='profile')],
    [InlineKeyboardButton(text='На главную', callback_data='to_main')]
])


async def catalog():
    """Кнопка для вывода каталога"""
    
    db = Database()
    all_catalog = await db.get_categories()
    keyboard = InlineKeyboardBuilder()
    
    for catalog in all_catalog:
        keyboard.add(InlineKeyboardButton(text=catalog.name, callback_data=f'catalog_{catalog.id}'))
    keyboard.add(InlineKeyboardButton(text='Профиль', callback_data='profile'))

    return keyboard.adjust(2).as_markup()


async def basket(game_id):
    """Кнопка для добвления игры в корзину"""

    basket = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'basket_{game_id}')],
        [InlineKeyboardButton(text='На главную', callback_data='to_main')]
    ])

    return basket

async def basket_game(game_id):
    """Кнопки для игры с корзины"""

    basket_game = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Убрать с корзины', callback_data=f'delete_{game_id}'), 
    InlineKeyboardButton(text='Купить', callback_data='buy')]
    ])

    return basket_game
