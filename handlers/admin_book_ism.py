from aiogram import Router, F, types
from aiogram.filters import Command, state
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_config import database


class BookForm(StatesGroup):
    name = State()
    prise = State()
    author = State()
    genre = State()
    confirm = State()


class GanreForm(StatesGroup):
    name = State()


admin = 1625576858
admin_book_router = Router()
admin_book_router.message.filter(F.from_user.id == admin)


@admin_book_router.message(Command("newganre"))
async def add_new_ganre(message: types.Message, state: FSMContext):
    await state.set_state(GanreForm.name)
    await message.answer("Введите название нового жанра:")


@admin_book_router.message(GanreForm.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    database.execute(
        query="""INSERT INTO ganres (name) VALUES (?,)""",
        params=(name,)
    )
    await state.clear()
    await message.answer("Жанр успешно добавлен!")


@admin_book_router.message(Command("newbook"))
async def start_book_form(message: types.Message, state: FSMContext):
    await state.set_state(BookForm.name)
    await message.answer("Задайте название книги:")


@admin_book_router.message(BookForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookForm.prise)
    await message.answer("Задайте цену книги:")


@admin_book_router.message(BookForm.prise)
async def process_prise(message: types.Message, state: FSMContext):
    await state.update_data(prise=message.text)
    await state.set_state(BookForm.author)
    await message.answer("Кто автор этой книги:")


@admin_book_router.message(BookForm.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(BookForm.genre)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Приключения"),
                types.KeyboardButton(text="Фантастика")
            ],
            [
                types.KeyboardButton(text="Детектив"),
                types.KeyboardButton(text="Мистика")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите жанр ...."
    )
    await message.answer("Выберите жанр книги:", reply_markup=kb)


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
    await message.answer(f"Вы ввели:\n Название: {data['name']},\nЦена: {data['prise']},\n"
                         f"Автор: {data['author']},\nЖанр: {data['genre']}", reply_markup=kb)


@admin_book_router.message(BookForm.confirm, F.text == "Да")
async def process_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    database.execute(
        query="""
            INSERT INTO books (name, author, prise, genre)
            VALUES (?, ?, ?, ?)
        """,
        params=(
            data['name'],
            data['author'],
            data['prise'],
            data['genre']
        )

    )

    await state.clear()
    await message.answer("Данные были сохранены!")


@admin_book_router.message(BookForm.confirm, F.text == "Нет")
async def process_confirm(message: types.Message, state: FSMContext):
    await state.set_state(BookForm.name)
    await message.answer("Задайте название книги:")
