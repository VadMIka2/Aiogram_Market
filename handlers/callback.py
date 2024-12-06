from aiogram import F, Bot, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import keyboard as kb
from database import database, basket_db
from state.register import RegisterSate

router = Router()


@router.callback_query(F.data == 'to_main')
@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    """Выводит каталог игр"""
    await callback.message.edit_text(f'Каталог игр:', reply_markup=await kb.catalog())


@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    """Выводит профиль пользователя"""
    db = database.Database()
    user = await db.select_user(callback.from_user.id)

    await callback.message.edit_text(f'Имя: {callback.from_user.first_name} \nЛогин Steam: {user.steam_login}', reply_markup=kb.profile)


@router.callback_query(F.data == 'reset_steam')
async def steam(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Сброс логина Steam"""

    await callback.message.edit_text(f"Напишите новый логин Steam")
    await state.set_state(RegisterSate.reset_steam)


@router.callback_query(F.data.startswith('catalog_'))
async def game(callback: CallbackQuery):
    """Информация о игре"""
    db = database.Database()

    game_id = int((callback.data.split('_'))[1])
    game = await db.game(game_id)

    await callback.message.edit_text(f'Игра: {game.name} \nСтоимость: {game.price} \nОписание: {game.description} \nКолличество: {game.status}', reply_markup=await kb.basket(game_id))


@router.callback_query(F.data.startswith('basket_'))
async def basket(callback: CallbackQuery):
    """Добавление игры в корзину"""
    db = basket_db.BasketDB()

    tg_id = callback.from_user.id
    game_id = int((callback.data.split('_'))[1])

    if not await db.select_game(tg_id, game_id):
        await callback.answer('Вы добавили игру в корзину')
        await db.add_busket(tg_id, game_id)
    else:
        await callback.answer('Игра уже находится в корзине')


@router.callback_query(F.data == 'basket')
async def print_basket(callback: CallbackQuery):
    """Вывод корзины"""
    db = basket_db.BasketDB()
    
    basket_games = await db.select_basket(callback.from_user.id)
    count = 0
    
    await callback.message.edit_text('Ваша корзина:')

    for games in basket_games:
        count += 1
        game_id = games.product_id
        games = await db.game(game_id)

        await callback.message.answer(f'Игра: {games.name} \nЦена: {games.price}руб. \nОсталось: {games.status}', reply_markup=await kb.basket_game(games.id))
    
    if count == 0:
        await callback.message.answer('В корзине ничего нет', reply_markup=kb.reg)
    else:
        await callback.message.answer('Вы можете купить по отдельности или можете купить все:', reply_markup=kb.game_buy)


@router.callback_query(F.data.startswith('delete_'))
async def delete_game(callback: CallbackQuery):
    """Удаление игры из корзины"""
    db = basket_db.BasketDB()

    game_id = int((callback.data.split('_'))[1])
    tg_id = callback.from_user.id

    if not await db.select_game(tg_id, game_id):
        await callback.answer('Игры нет в корзине')
    else:
        await callback.answer('Игра была удалена из корзины')
        await db.delete_game(tg_id, game_id)
        await callback.message.delete()


@router.callback_query(F.data == 'reg')
async def reg(message: Message, bot: Bot, state: FSMContext):
    """Регистрация пользователя"""
    db = database.Database()

    if not await db.select_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f"Начнем регестрацию. Пожалуйста напишите свой логин Steam:")
        await state.set_state(RegisterSate.regName_steam)
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')


@router.message(RegisterSate.regName_steam)
async def reg_user(message: Message, bot: Bot, state: FSMContext):
    """Добавляем пользователя в БД"""
    await state.update_data(regname=message.text)

    reg_data = await state.get_data()

    username = message.from_user.first_name
    tg_id = message.from_user.id
    tg_url = str("https://t.me/" + message.from_user.username)
    steam_login = reg_data.get('regname')

    await bot.send_message(message.from_user.id, f"Приятно познакмится {username}")

    db = database.Database()
    await db.add_user(tg_id, username, tg_url, steam_login)
    await state.clear()
    await bot.send_message(message.from_user.id, 'Вы успешно прошли регестрацию')


@router.message(RegisterSate.reset_steam)
async def login_steam(message: Message, bot: Bot, state: FSMContext):
    """Смена логина Steam"""
    db = database.Database()

    await state.update_data(login=message.text)
    login_data = await state.get_data()
    steam_login = login_data.get('login')
    
    await db.reset_steam(message.from_user.id, steam_login)
    await bot.send_message(message.from_user.id, 'Вы успешно сменили логин Steam', reply_markup=kb.reg)
