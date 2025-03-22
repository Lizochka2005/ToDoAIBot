
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite
from datetime import datetime
from speech_functions import language_text, check_language_ru



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

        response = "Your nearest tasks:"
        response = await language_text(user_id, response)
        response += '\n'
        for task, date, time in tasks:
            date = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date.strftime('%d %B %Y')
            if await check_language_ru(message.from_user.id):
                date = formatted_date.split(' ')
                month = await language_text(message.from_user.id, date[1])
                formatted_date = f'{date[0]} {month} {date[-1]}'
            if await check_language_ru(user_id):
                response += f"- {task} (Дата: {formatted_date}, Время: {time})\n"
            else:
                response += f"- {task} (Date: {formatted_date}, Time: {time})\n"
        
        await message.answer(response)

