from aiogram import F, Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from handlers import admin
from keyboards import keyboard as kb
from database import database

router = Router()
router.include_router(admin.router)

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    """Обработка команды старт"""
    
    db = database.Database()
    if not await db.select_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.first_name}.\n'
                               'Добро пожаловать в магазин с играми для платформы Steam.', reply_markup=kb.un_reg)
    else:
        await bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.first_name}.\n'
                               'Добро пожаловать в магазин с играми для платформы Steam.', reply_markup=kb.reg)


@router.message(Command('profile'))
async def profile(message: Message, bot: Bot):
    """Вывод профиля при команде - /profile"""
    
    db = database.Database()
    user = await db.select_user(message.from_user.id)

    if not await db.select_user(message.from_user.id):
        await bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.first_name}.\n'
                               'У вас нет профиля, для начала надо зарегестрироваться', reply_markup=kb.un_reg)
    else:
        await bot.send_message(message.from_user.id, f'Имя: {message.from_user.first_name} \nЛогин Steam: {user.steam_login}', reply_markup=kb.profile)