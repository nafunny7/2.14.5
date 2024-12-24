from aiogram import types, Dispatcher, executor, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import asyncio
import sqlite3
from crud_functions2 import *

api = "8086178039:AAGi5LK7wqg_2DJ43AOvt_WJtMaNJJHh_H4"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_def = ReplyKeyboardMarkup(resize_keyboard=True)
but_def1 = KeyboardButton(text="Рассчитать")
but_def2 = KeyboardButton(text="Информация")
but_def3 = KeyboardButton(text="Купить")
but_def4 = KeyboardButton(text="Регистрация")
kb_def.add(but_def1, but_def2,
           but_def3, but_def4)

kbm_inline = InlineKeyboardMarkup(resize_keyboard=True)
but_inline1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
but_inline2 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kbm_inline.add(but_inline1, but_inline2)

kbm_inline_buy = InlineKeyboardMarkup(resize_keyboard=True)
but_inline_buy1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
but_inline_buy2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
but_inline_buy3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
but_inline_buy4 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
kbm_inline_buy.add(but_inline_buy1, but_inline_buy2, but_inline_buy3, but_inline_buy4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    age = State()
    email = State()
    balance = 1000


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Данный пользователь уже существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("ВВедите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data["username"], data["email"], data["age"])
    await message.answer("Регистрация выполнилась!!!")
    await state.finish


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        await message.answer(f"Название: {product[1]}| Описание: {product[2]}  | Цена: {product[3]}")
        with open(f"{product[0]}.png", "rb") as images:
            await message.answer_photo(images)

    await message.answer("Выберите продукт для покупки:", reply_markup=kbm_inline_buy)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Продукт заказан")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = int(int(data["weight"]) * 10 + 6.25 * int(data["growth"]) - 4.92 * int(data["age"]))
    await message.answer(f"Ваша норма калорий в день составляет: {res}")
    await state.finish()


@dp.message_handler(commands=["start"])
async def com_start(message):
    await message.answer("Выберите виджет:", reply_markup=kb_def)


@dp.message_handler(text="Информация")
async def information(message):
    await message.answer("Информация про бота отсутствует🤫")


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kbm_inline)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer()


@dp.message_handler()
async def all_message(message):
    await message.answer("😊")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
