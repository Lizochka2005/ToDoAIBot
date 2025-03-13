from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiosqlite
from speech_functions import *

from states import Registration, Question
import keyboards as kb

start = Router()



@start.message(Command("start"), State(None))
async def start_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT name FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            user = await cursor.fetchone()
            if user is None:
                await message.answer("Hi! What is your name?")
                await state.set_state(Registration.waiting_for_name)
            else:
                text = f"Hi, {user[0]}! You are already registered."
                text = await language_text(user_id, text)
                await message.answer(text)
                if await check_language_ru(message.from_user.id):
                    await message.answer(kb.show_commands_ru())
                    await state.clear()
                else:
                    await message.answer(kb.show_commands_en())
                    await state.clear()



@start.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("What language do you prefer? (ru/en)")
    await state.set_state(Registration.waiting_for_language)


@start.message(Registration.waiting_for_language)
async def process_language(message: Message, state: FSMContext):
    if message.text.lower() not in ["ru", "en"]:
        await message.answer("Please, choose 'ru' or 'en'.")
        return

    user_data = await state.get_data()
    user_id = message.from_user.id
    name = user_data["name"]
    language = message.text.lower()

    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT INTO users (user_id, name, language) VALUES (?, ?, ?)",
            (user_id, name, language),
        )
        await db.commit()

    text = f"Registration completed! Name: {name}, Language: {language}"
    text = await language_text(user_id, text)
    await message.answer(text)
    if await check_language_ru(message.from_user.id):
        await message.answer(kb.show_commands_ru())
        await state.clear()
    else:
        await message.answer(kb.show_commands_en())
        await state.clear()