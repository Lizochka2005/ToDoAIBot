
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram import Router

from states import DeadlineUpdate
from speech_functions import *

update_deadline = Router()

@update_deadline.message(Command("update_deadline"))
async def update_deadline_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE user_id=? and status not like('Завершён')", (user_id,)) as cursor:
        deadlines = await cursor.fetchall()

        if not deadlines:
            text = 'You have no deadlines.'
            text = await language_text(user_id, text)
            await message.answer(text)
            return

        response = "Your deadlines:\n"
        for deadline_id, deadline, date, time, status in deadlines:
            response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

        response += "Enter the ID of deadline which you want to update:"
        response = await language_text(user_id, response)
        await message.answer(response)
        await state.set_state(DeadlineUpdate.waiting_for_deadline_id)

@update_deadline.message(DeadlineUpdate.waiting_for_deadline_id)
async def process_task_id(message: Message, state: FSMContext):
    deadline_id = message.text
    if not deadline_id.isdigit():
        text = "Please, enter thr integer ID of deadline."
        text = await language_text(message.from_user.id, text)
        await message.answer(text)
        return

    await state.update_data(deadline_id=deadline_id)
    # здесь надо изменить на сообщение выбора, что хотят изменить + кнопочки (дата, время, статус)
    # await message.answer("Выберите новый статус задачи:\n1. Выполнено\n2. Выполнено частично\n3. Отложено")
    # await state.set_state(TaskUpdate.waiting_for_new_status)
    pass