from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import aiosqlite

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
            await message.answer("Некорректно введена дата, попробуйте ещё раз!")
            return
        elif (a[1][:1] != 0 and int(a[1]) > 12) or (a[2][:1] != 0 and a[2] > 31):
            await message.answer("Некорректно введена дата, попробуйте ещё раз!")
            return
    except Exception as e:
        await message.answer("Некорректно введена дата, попробуйте ещё раз!")
        return

    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT task, status, date, time FROM tasks WHERE user_id=? and date=?",
            (
                user_id,
                date,
            ),
        ) as cursor:
            tasks = cursor.fetchall()

            if not tasks:
                await message.answer(f"У вас нет задач на {date}.")
                return

            response = f"Ваши задачи на {date}:\n"
            for task, status, date, time in tasks:
                response += f"- {task} (Статус: {status}, Время: {time})\n"
            await message.answer(response)
