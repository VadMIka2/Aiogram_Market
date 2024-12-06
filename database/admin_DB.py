from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import *
from database.database import Database

class AdminDB(Database):

    def __init__(self):
        super().__init__()
    
    async def select_admin(self, tg_id):
        """Проверяем есть ли админ в БД"""

        async with self.Session() as request:
            return await request.scalar(select(Admin.username).where(Admin.telegram_id == tg_id))
    
    async def add_game(self, name: str, descript: str, price: float, status: int):
        """Добавляем игру в БД"""

        async with self.Session() as request:
            request.add(Catalog(
                name=name,
                description=descript,
                price=price,
                status=status
            ))

            await request.commit()
    
    async def get_game(self):
        """Вывод игр для удаления"""

        async with self.Session() as request:
            return await request.scalars(select(Catalog))
    
    async def delete_game(self, game_id):
        """Удаление игры из БД"""

        async with self.Session() as request:
            result = await request.scalar(select(Catalog).where(Catalog.id == game_id))

            await request.delete(result)
            await request.commit()
