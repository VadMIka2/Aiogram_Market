from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import keyboard as kb
from keyboards import admin_kb
from database import admin_DB
from state.admin import GameState

router = Router()

@router.message(Command('admin'))
async def cmd_admin(message: Message, bot: Bot):
    """Обработка комманды admin"""
    db = admin_DB.AdminDB()

    if not await db.select_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Вы не администратор', reply_markup=kb.reg)
    else:
        await bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.first_name}, вот панель администратора.', reply_markup=admin_kb.admin)


@router.callback_query(F.data == 'to_admin_panel')
async def admin_panel(message: Message, bot: Bot):
    """Вывод админ панели"""
    await bot.send_message(message.from_user.id, f'Панель администратора.', reply_markup=admin_kb.admin)


@router.callback_query(F.data == 'delete_game')
async def catalog_game(message: Message, bot: Bot):
    """Вывод игры из каталога для удаления"""
    await bot.send_message(message.from_user.id, 'Выберете игру для удаления', reply_markup=await admin_kb.game())


@router.callback_query(F.data.startswith('game_delete_'))
async def delete_game(callback: CallbackQuery):
    """Удаление игры из БД"""
    db = admin_DB.AdminDB()

    game_id = (callback.data.split('_'))[2]
    await db.delete_game(game_id)

    await callback.answer('Игра была удалена')


@router.callback_query(F.data == 'add_game')
async def add_game(message: Message, bot: Bot, state: FSMContext):
    """Запрашиваем имя для игры"""
    db = admin_DB.AdminDB()

    if not await db.select_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Вы не администратор', reply_markup=kb.reg)
    else:
        await bot.send_message(message.from_user.id, f'Напишите название игры:')
        await state.set_state(GameState.gameName)


@router.message(GameState.gameName)
async def add_name_game(message: Message, bot: Bot, state: FSMContext):
    """Добавляем имя в машинное состаяние"""
    await state.update_data(namegame=message.text)

    await bot.send_message(message.from_user.id, f'Напишите описание игры:')
    await state.set_state(GameState.descriptGame)


@router.message(GameState.descriptGame)
async def add_name_game(message: Message, bot: Bot, state: FSMContext):
    """Добавляем описание в машинное состаяние"""
    await state.update_data(descriptgame=message.text)

    await bot.send_message(message.from_user.id,'Введите цену игры:')
    await state.set_state(GameState.priceGame)


@router.message(GameState.priceGame)
async def add_name_game(message: Message, bot: Bot, state: FSMContext):
    """Добавляем цену в машинное состаяние"""
    try:
        await state.update_data(pricegame=float(message.text))

        await bot.send_message(message.from_user.id, f'Теперь введите колличество ключей:')
        await state.set_state(GameState.statusGame)
    except ValueError:
        await bot.send_message(message.from_user.id, f'Введите ЦЕНУ игры!!!')
        await state.set_state(GameState.priceGame)


@router.message(GameState.statusGame)
async def add_name_game(message: Message, bot: Bot, state: FSMContext):
    """Добавляем колличесвто в машинное состаяние и даем запрос в БД"""
    try:
        db = admin_DB.AdminDB()

        await state.update_data(statusgame=int(message.text))
        game_data = await state.get_data()

        name = game_data.get('namegame')
        descript = game_data.get('descriptgame')
        price = game_data.get('pricegame')
        status_key = game_data.get('statusgame')
        
        await db.add_game(name, descript, price, status_key)
        await bot.send_message(message.from_user.id, f'Игра {name} успешна добавлена в каталог', reply_markup=kb.reg)

        await state.clear()
    except ValueError:
        await bot.send_message(message.from_user.id, f'Введите КОЛЛИЧЕСТВО!!!')
        await state.set_state(GameState.statusGame)