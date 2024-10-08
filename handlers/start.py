from aiogram import Router, types, F
from aiogram.filters.command import Command


start_router = Router()

@start_router.message(Command(commands=['start']))
async def start_handler(message):
    name = message.from_user.first_name

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Наш сайт", url="https://geeks.kg"),
                types.InlineKeyboardButton(text="Наш инстаграм", url="https://instagram.com/geekskg")
            ],
            [
                types.InlineKeyboardButton(text="О нас", callback_data="about_us")
            ]
        ]
    )

    await message.answer(f"Добро {name} пожаловать на бот Backend_bot этот бот был создан для книгалюбов", reply_markup=keyboard)
@start_router.callback_query(F.data == "about_us")
async def about_us_handler(callback: types.CallbackQuery):
    text = "Текст о нашем магазине"
    await callback.message.answer(text)