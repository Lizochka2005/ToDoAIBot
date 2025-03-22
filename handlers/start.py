from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
import aiosqlite
from speech_functions import language_text, check_language_ru

from states import Registration
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
                await message.answer("Choose the language that you prefer. (ru/en)", reply_markup=kb.registration_lan)
            else:
                text1 = "Hi, " 
                text1 = await language_text(user_id, text1)
                text2 =" You are already registered."
                text2 = await language_text(user_id, text2)
                text = text1 + " " + user[0] + '! ' + text2
                await message.answer(text)

    
@start.message(Registration.waiting_for_language)
async def process_language(message: Message, state: FSMContext):
    user_data = await state.get_data()
    lan = user_data['lan']

    await state.update_data(language=lan)
    if lan == 'ru':
        await message.answer("Привет! Как я могу к вам обращаться?")
    else:
        await message.answer("Hi! What is your name?")

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

    if await check_language_ru(user_id):
        text = f"Регистрация завершена! Имя: {name}, Язык: {language}"
    else:
        text = f"Registration completed! Name: {name}, Language: {language}"
    await message.answer(text)
    await state.clear()


