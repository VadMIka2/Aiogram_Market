import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import commands, callback
from database.database import Database

async def main():
    load_dotenv()
    db = Database()
    await db.create_db()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(commands.router,
                       callback.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot starting")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stoping')