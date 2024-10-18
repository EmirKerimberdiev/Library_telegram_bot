from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_config import database


class BookForm(StatesGroup):
    name = State()
    price = State()
    author = State()
    genre = State()
    confirm = State()

admin = 239834
admin_book_router = Router()
admin_book_router.message.filter(F.from_user.id == admin)


@admin_book_router.message(Command("newbook"))
async def start_book_form(message: types.Message, state: FSMContext):
    await state.set_state(BookForm.name)
    await message.answer("Задайте название книги:")


@admin_book_router.message(BookForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookForm.price)
    await message.answer("Задайте цену книги:")


@admin_book_router.message(BookForm.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(BookForm.author)
    await message.answer("Кто автор этой книги:")


@admin_book_router.message(BookForm.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(BookForm.genre)
    await message.answer("Выберите жанр:")


@admin_book_router.message(BookForm.genre)
async def proces_s_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    data = await state.get_data()
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]],
        resize_keyboard=True
    )
    await state.set_state(BookForm.confirm)
    await message.answer(f"Вы ввели:\n Название: {data['name']},\nЦена: {data['price']},\n"
                         f"Автор: {data['author']},\nЖанр: {data['genre']}", reply_markup=kb)


@admin_book_router.message(BookForm.confirm, F.text == "Да")
async def process_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await state.clear()
    await message.answer("Данные были сохранены!")
