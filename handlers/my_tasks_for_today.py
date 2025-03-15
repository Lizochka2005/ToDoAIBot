from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject
import aiosqlite
from speech_functions import *
from datetime import datetime, time

from states import Registration

my_tasks_for_today = Router()

date = datetime.today().date()

@my_tasks_for_today.message(Command("my_tasks_for_today"),Registration.confirmed)
async def show_tasks_for_date(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT task, status, date, time FROM tasks WHERE user_id=? and date=?",
            (
                user_id,
                date,
            ),
        ) as cursor:
            tasks = await cursor.fetchall()

            if not tasks:
                text = f'You have no tasks on {date}'
                text = await language_text(user_id, text)
                await message.answer(text)
                return

            response = f"Your tasks on {date}:\n"
            for task, status, date, time in tasks:
                status = await translate_text_to_en(user_id, status)
                response += f"- {task} (Status: {status}, Time: {time})\n"

            response = await language_text(user_id, response)
            await message.answer(response)
            await state.set_state(Registration.confirmed)
