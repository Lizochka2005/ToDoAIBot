from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import aiosqlite
from speech_functions import *

from states import GetTaskListForDate

my_tasks_for_today = Router()


@my_tasks_for_today.message(GetTaskListForDate.waiting_for_date)
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
                text = f'You have no tasks on {date}'
                text = await language_text(user_id, text)
                await message.answer(text)
                return

            response = f"Your tasks on {date}:\n"
            for task, status, date, time in tasks:
                response += f"- {task} (Status: {status}, Time: {time})\n"

            response = await language_text(user_id, response)
            await message.answer(response)
