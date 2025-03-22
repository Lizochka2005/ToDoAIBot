
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
import aiosqlite

from states import Question, Registration
from speech_functions import language_text



my_nearest_tasks = Router()


@my_nearest_tasks.message(Command("my_nearest_tasks"))
async def show_tasks_for_today(message: Message):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT task, date, time FROM tasks WHERE user_id=? and status not like('Выполнено') ORDER BY date, time", (user_id,)) as cursor:
        tasks = await cursor.fetchall()
        if not tasks:
            text = "You don't have any nearest tasks."
            text = await language_text(user_id, text)
            await message.answer(text)
            return

        response = "Your nearest tasks:\n"
        for task, date, time in tasks:
            response += f"- {task} (Date: {date}, Time: {time})\n"
        
        response = await language_text(user_id, response)
        await message.answer(response)

