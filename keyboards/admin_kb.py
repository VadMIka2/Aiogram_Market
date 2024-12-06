from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import admin_DB

admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить игру', callback_data='add_game')],
    [InlineKeyboardButton(text='Удалить игру', callback_data='delete_game')]
    ])


async def game():
    """Вывод каталога игр в виде кнопок"""
    db = admin_DB.AdminDB()
    all_catalog = await db.get_game()
    keyboard = InlineKeyboardBuilder()

    for game in all_catalog:
        keyboard.add(InlineKeyboardButton(text=game.name, callback_data=f'game_delete_{game.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_admin_panel'))

    return keyboard.adjust(2).as_markup()

