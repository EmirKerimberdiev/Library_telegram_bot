import asyncio
import logging
from aiogram import Bot

from bot_config import bot, dp, database
from handlers.start import start_router
from handlers.picture import pic_router
from handlers.opros_diolog import opros_router
from handlers.other_messages import echo_router
from handlers.admin_book_ism import admin_book_router
from handlers.book_catalog import catalog_router


async def on_startup(bot: Bot):
    print("База данных создана")
    database.create_tables()


async def main():
    dp.startup.register(on_startup)
    dp.include_router(start_router)
    dp.include_router(pic_router)
    dp.include_router(opros_router)
    dp.include_router(admin_book_router)
    dp.include_router(catalog_router)

    dp.include_router(echo_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
