
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram import Router

from speech_functions import *
from states import TaskUpdate

update_task = Router()

@update_task.message(Command("update_task"))
async def update_task_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, task, date, time, status FROM tasks WHERE user_id=? and status not like('Выполнено')", (user_id,)) as cursor:
        tasks = await cursor.fetchall()

        if not tasks:
            text = 'You have no tasks.'
            text = await language_text(user_id, text)
            await message.answer(text)
            return

        response = "Your tasks:\n"
        for task_id, task, date, time, status in tasks:
            response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        response += "Enter the ID of task which you want to update:"
        response = await language_text(user_id, response)
        await message.answer(response)
        await state.set_state(TaskUpdate.waiting_for_task_id)

@update_task.message(TaskUpdate.waiting_for_task_id)
async def process_task_id(message: Message, state: FSMContext):
    task_id = message.text
    if not task_id.isdigit():
        text = 'Please, enter thr integer ID of task.'
        text = await language_text(message.from_user.id, text)
        await message.answer(text)
        return

    await state.update_data(task_id=task_id)
    # здесь надо изменить на сообщение выбора, что хотят изменить + кнопочки (дата, время, статус)
    # await message.answer("Выберите новый статус задачи:\n1. Выполнено\n2. Выполнено частично\n3. Отложено")
    # await state.set_state(TaskUpdate.waiting_for_new_status)
    pass