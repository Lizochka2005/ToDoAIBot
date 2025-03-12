
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram import Router

from states import TaskUpdate

update_task = Router()

@update_task.message(Command("update_task"))
async def update_task_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, task, date, time, status FROM tasks WHERE user_id=? and status not like('Выполнено')", (user_id,)) as cursor:
        tasks = cursor.fetchall()

        if not tasks:
            await message.answer("У вас пока нет задач.")
            return

        response = "Ваши задачи:\n"
        for task_id, task, date, time, status in tasks:
            response += f"{task_id}. {task} (Дата: {date}, Время: {time}, Статус: {status})\n"

        await message.answer(response + "Введите ID задачи, которую хотите обновить:")
        await state.set_state(TaskUpdate.waiting_for_task_id)

@update_task.message(TaskUpdate.waiting_for_task_id)
async def process_task_id(message: Message, state: FSMContext):
    task_id = message.text
    if not task_id.isdigit():
        await message.answer("Пожалуйста, введите числовой ID задачи.")
        return

    await state.update_data(task_id=task_id)
    # здесь надо изменить на сообщение выбора, что хотят изменить + кнопочки (дата, время, статус)
    # await message.answer("Выберите новый статус задачи:\n1. Выполнено\n2. Выполнено частично\n3. Отложено")
    # await state.set_state(TaskUpdate.waiting_for_new_status)
    pass