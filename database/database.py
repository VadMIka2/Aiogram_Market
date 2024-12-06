from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from database.models import *

import os


class Database():
    """Запросы в БД"""

    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.connect = self.db_name
        self.async_engine = create_async_engine(self.connect)
        self.Session = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)
    
    async def create_db(self):
        """Создание таблицы"""
        
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def select_user(self, tg_id):
        """Проверка на нахождения пользователя в БД"""

        async with self.Session() as request:
            return await request.scalar(select(User).where(User.telegram_id == tg_id))

    async def add_user(self, tg_id, name, tg_url, steam_login):
        """Добовляем пользователя"""

        async with self.Session() as request:
            request.add(User(
                username=name,
                telegram_id=tg_id,
                telegram_url=tg_url,
                steam_login=steam_login
            ))

            await request.commit()

    async def reset_steam(self, tg_id, login_steam):
        """Сброс логина Steam"""

        async with self.Session() as request:
            await request.execute(update(User).values(steam_login=login_steam).where(User.telegram_id == tg_id)) 
     
            await request.commit()

    async def get_categories(self):
        """Вывод каталога игр"""

        async with self.Session() as request:
            return await request.scalars(select(Catalog).where(Catalog.status > 0))
    
    async def game(self, game_id):
        """Вывод информации о игре"""

        async with self.Session() as request:
            return await request.scalar(select(Catalog).where(Catalog.id == game_id))
        


