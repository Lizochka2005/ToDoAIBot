from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import aiosqlite

from states import Question, GetTaskListForDate
from speech_functions import *

from aiogram import Router

my_tasks_for_date = Router()


@my_tasks_for_date.message(Command("my_tasks_for_date"))
async def ask_for_date(message: Message, state: FSMContext):
    text = 'Enter the date in format YYYY-MM-DD'
    text = await language_text(message.from_user.id, text)
    await message.answer(text)
    await state.set_state(GetTaskListForDate.waiting_for_date)


@my_tasks_for_date.message(GetTaskListForDate.waiting_for_date)
async def show_tasks_for_date(message: Message, state: FSMContext):
    date = message.text
    user_id = message.from_user.id
    try:
        a = date.split("-")
        if (
            len(a) != 3
            or len(a[0]) != 4
            or len(a[1]) != 2
            or len(a[2]) != 2
            or a[0][:1] == 0
        ):
            text = 'Incorrect date, please try again!'
            text = await language_text(user_id, text)
            await message.answer(text)
            return
        elif (a[1][:1] != 0 and int(a[1]) > 12) or (a[2][:1] != 0 and a[2] > 31):
            text = 'Incorrect date, please try again!'
            text = await language_text(user_id, text)
            await message.answer(text)
            return
    except Exception as e:
        text = 'Incorrect date, please try again!'
        text = await language_text(user_id, text)
        await message.answer(text)
        return

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
                await message.answer(f"У вас нет задач на {date}.")
                return

            response = f"Your tasks on {date}:\n"
            for task, status, date, time in tasks:
                response += f"- {task} (Status: {status}, Time: {time})\n"
            
            response = await language_text(user_id, response)
            await message.answer(response)
            # await state.set_state(Start.question)
