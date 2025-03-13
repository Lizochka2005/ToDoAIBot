
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
import aiosqlite

from states import Question
from speech_functions import *



my_nearest_deadlines = Router()


@my_nearest_deadlines.message(Command("my_nearest_deadlines"))
async def show_tasks_for_today(message: Message):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT deadline, date, time FROM deadlines WHERE user_id=? and status not like('Завершён')", (user_id,)) as cursor:
        deadlines = await cursor.fetchall()

        if not deadlines:
            text = "You don't have any nearest deadlines."
            text = await language_text(user_id, text)
            await message.answer(text)
            return

        response = "Your nearest deadlines:\n"
        for deadline, date, time in deadlines:
            response += f"- {deadline} (Date: {date}, Time: {time})\n"
        
        response = await language_text(user_id, response)
        await message.answer(response)
