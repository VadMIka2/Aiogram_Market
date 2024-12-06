from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import *
from database.database import Database

import os


class BasketDB(Database):

    def __init__(self):
        super().__init__()

    async def select_game(self, tg_id, game_id):
        """Проверям есть ли игра в корзине"""

        async with self.Session() as request:
            return await request.scalar(select(Basket).where((Basket.telegram_id == tg_id), (Basket.product_id == game_id)))
    
    async def select_basket(self, tg_id):
        """Возвращает все игры связязанные с tg id"""

        async with self.Session() as request:
            return await request.scalars(select(Basket).where(Basket.telegram_id == tg_id))
    
    async def add_busket(self, tg_id, game_id):
        """Добавляем игру в корзину"""

        async with self.Session() as request:
            request.add(Basket(
                telegram_id=tg_id,
                product_id=game_id
            ))

            await request.commit()
    
    async def delete_game(self, tg_id, game_id):
        """Удаляет игру из корзины"""

        async with self.Session() as request:
            result = await request.scalar(select(Basket).where((Basket.telegram_id == tg_id), (Basket.product_id == game_id)))
            await request.delete(result)

            await request.commit()