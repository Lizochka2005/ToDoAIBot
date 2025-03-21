from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram.types import ReplyKeyboardRemove

from speech_functions import *

from states import Registration, Question
import keyboards as kb

start = Router()


@start.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT name FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            user = await cursor.fetchone()
            if user is None:
                await message.answer(
                    "What language do you prefer? (ru/en)",
                    reply_markup=kb.choose_language,
                )
                await state.set_state(Registration.waiting_for_language)
            else:
                text1 = "Hi, "
                text1 = await language_text(user_id, text1)
                text2 = " You are already registered."
                text2 = await language_text(user_id, text2)
                text = text1 + " " + user[0] + "! " + text2
                await message.answer(text)
                await state.set_state(Registration.confirmed)


@start.message(Registration.waiting_for_language)
async def process_language(message: Message, state: FSMContext):
    if message.text.lower() not in ["ru", "en"]:
        await message.answer(
            "Please, choose 'ru' or 'en'.", reply_markup=kb.choose_language
        )
        return

    await state.update_data(language=message.text.lower())
    if message.text.lower() == "ru":
        await message.answer(
            "Привет! Как я могу к вам обращаться?", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Hi! What is your name?", reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(Registration.waiting_for_name)


@start.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = message.from_user.id
    name = message.text
    language = user_data["language"]

    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT INTO users(user_id, name, language, subscribed) VALUES (?, ?, ?, TRUE)",
            (user_id, name, language),
        )
        await db.commit()

    text1 = "Registration completed! Name:"
    text1 = await language_text(user_id, text1)
    text2 = "Language:"
    text2 = await language_text(user_id, text2)
    text = text1 + f" {name}, " + text2 + " " + language
    await message.answer(text)
    await state.set_state(Registration.confirmed)
