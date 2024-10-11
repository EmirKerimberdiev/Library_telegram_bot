from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

opros_router = Router()


class Opros(StatesGroup):
    name = State()
    age = State()
    gender = State()
    genre = State()


@opros_router.message(Command('opros'))
async def opros_handler(message: types.Message, state: FSMContext):
    # Выставляем состояние диолога на Opros.name
    await state.set_state(Opros.name)
    await message.answer("Как вас зовут?")


@opros_router.message(Command('stop'))
@opros_router.message(F.text == "стоп")
async def stop_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос остановлен !")


@opros_router.message(Opros.name)
async def opros_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Opros.age)
    await message.answer("Сколько вам лет?")


@opros_router.message(Opros.age)
async def opros_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Opros.gender)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Мужской"),
                types.KeyboardButton(text="Женский")
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer("Какого вы пола? (М / Ж)", reply_markup=kb)


@opros_router.message(Opros.gender)
async def opros_gender(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.update_data(gender=message.text)
    await state.set_state(Opros.genre)
    await message.answer("Отправьте ваш любимый жанр литературы?")


@opros_router.message(Opros.genre)
async def opros_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)

    data = await state.get_data()
    print(data)
    await state.clear()
    await message.answer("Спасибр за пройденный опрос!!!")
