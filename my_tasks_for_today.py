from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject
import aiosqlite
from speech_functions import *
from datetime import datetime, time

from states import Registration

my_tasks_for_today = Router()

@my_tasks_for_today.message(Command("my_tasks_for_today"))
async def show_tasks_for_date(message: Message, state: FSMContext):
    user_id = message.from_user.id
    date = datetime.today().date()
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT task, status, date, time FROM tasks WHERE user_id=? and date=? ORDER BY time",
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

            date = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date.strftime('%d %B %Y')
            if await check_language_ru(message.from_user.id):
                date = formatted_date.split(' ')
                month = await language_text(message.from_user.id, date[1])
                formatted_date = f'{date[0]} {month} {date[-1]}'
            response = f"Your tasks on {formatted_date}:\n"
            response = await language_text(user_id, response)
            for task, status, date, time in tasks:
                if await check_language_ru(user_id):
                    response += f"- {task} (Cтатус: {status}, Время: {time})\n"
                else:
                    status = await translate_text_to_en(status)
                    response += f"- {task} (Status: {status}, Time: {time})\n"

            await message.answer(response)
    await state.clear()

