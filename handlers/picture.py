from aiogram import Router, types
from aiogram.filters.command import Command


pic_router = Router()


@pic_router.message(Command(commands=['pic']))
async def pic_handler(message):
    image = types.FSInputFile('C:/Users/User/Desktop/python_geeks/3_month/Lesson/me.webp')
    await message.answer_photo(image)
