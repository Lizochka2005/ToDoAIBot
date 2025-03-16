
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram import Router

from speech_functions import *
from states import TaskUpdate, Registration
import keyboards as kb

update_task = Router()

@update_task.message(Command("update_task"), Registration.confirmed)
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
    text = 'Choose what you want to update:'
    text = await language_text(message.from_user.id, text)
    if await check_language_ru(message.from_user.id):
        await message.answer(text, reply_markup=kb.update_task_ru)
    else:
        await message.answer(text, reply_markup=kb.update_task_ru)

@update_task.message(TaskUpdate.waiting_for_new_time)
async def set_new_time_for_task(message: Message, state: FSMContext):
    user_data = await state.get_data()
    time = message.text
    user_id = message.from_user.id
    id = user_data["task_id"]
    try:
        a = time.split(":")
        if (
            len(a) != 2
            or len(a[0]) != 2
            or len(a[1]) != 2
        ):
            text = 'Incorrect time, please try again!'
            text = await language_text(user_id, text)
            await message.answer(text)
            await state.set_state(Registration.confirmed)
            return
        elif (a[0][:1] != 0 and int(a[0]) > 23) or (a[1][:1] != 0 and a[1] >= 60):
            text = 'Incorrect time, please try again!'
            text = await language_text(user_id, text)
            await message.answer(text)
            await state.set_state(Registration.confirmed)
            return
    except Exception as e:
        text = 'Incorrect time, please try again!'
        text = await language_text(user_id, text)
        await message.answer(text)
        await state.set_state(Registration.confirmed)
        return

    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET time = ? WHERE id=?",
            (
                time,
                id,
            ),
        )
        await db.commit()
    
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)) as cursor:
        tasks = await cursor.fetchall()

        response = "Your task:\n"
        for task_id, task, date, time, status in tasks:
            status = await translate_text_to_en(user_id, status)
            response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        response = await language_text(user_id, response)
        await message.answer(response)
        await state.set_state(Registration.confirmed)


@update_task.message(TaskUpdate.waiting_for_new_date)
async def set_new_time_for_deadline(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = message.text
    user_id = message.from_user.id
    id = user_data["task_id"]

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
            await state.set_state(Registration.confirmed)
            return
        elif (a[1][:1] != 0 and int(a[1]) > 12) or (a[2][:1] != 0 and a[2] > 31):
            text = 'Incorrect date, please try again!'
            text = await language_text(user_id, text)
            await message.answer(text)
            await state.set_state(Registration.confirmed)
            return
    except Exception as e:
        text = 'Incorrect date, please try again!'
        text = await language_text(user_id, text)
        await message.answer(text)
        await state.set_state(Registration.confirmed)
        return
    
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET date = ? WHERE id=?",
            (
                date,
                id,
            ),
        )
        await db.commit()
    
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)) as cursor:
        tasks = await cursor.fetchall()

        response = "Your task:\n"
        for task_id, task, date, time, status in tasks:
            status = await translate_text_to_en(user_id, status)
            response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        response = await language_text(user_id, response)
        await message.answer(response)
        await state.set_state(Registration.confirmed)
    