import asyncio
import logging

from bot_config import bot, dp
from handlers.start import start_router
from handlers.picture import pic_router
from handlers.other_messages import echo_router


async def main():
    dp.include_router(start_router)
    dp.include_router(pic_router)
    dp.include_router(echo_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
