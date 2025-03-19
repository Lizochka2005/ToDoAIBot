
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

        response = "Your tasks:"
        response = await language_text(user_id, response)
        response += '\n'
        for task_id, task, date, time, status in tasks:
            if await check_language_ru(user_id):
                response += f"{task_id}. {task} (Дата: {date}, Время: {time}, Статус: {status})\n"
            else:
                status = await translate_text_to_en(status)
                response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        text = "Enter the ID of task which you want to update:"
        text = await language_text(user_id, text)
        response += text
        await message.answer(response)
        await state.set_state(TaskUpdate.waiting_for_task_id)

@update_task.message(TaskUpdate.waiting_for_task_id)
async def process_task_id(message: Message, state: FSMContext):
    task_id = message.text
    if not task_id.isdigit():
        text = 'Please, enter thr integer ID of task.'
        text = await language_text(message.from_user.id, text)
        await message.answer(text)
        await state.set_state(Registration.confirmed)
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
        elif (int(a[0][:1]) != 0 and int(a[0]) > 23) or (int(a[1][:1]) != 0 and int(a[1]) >= 60):
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

        response = "Your task:"
        response = await language_text(user_id, response)
        response += '\n'
        for task_id, task, date, time, status in tasks:
            if await check_language_ru(user_id):
                    response += f"{task_id}. {task} (Дата: {date}, Время: {time}, Статус: {status})\n"
            else:
                status = await translate_text_to_en(status)
                response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

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
            or int(a[0][:1]) == 0
        ):
            text = 'Incorrect date, please try again!'
            text = await language_text(user_id, text)
            await message.answer(text)
            await state.set_state(Registration.confirmed)
            return
        elif (int(a[1][:1]) != 0 and int(a[1]) > 12) or (int(a[2][:1]) != 0 and int(a[2]) > 31):
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

        response = 'Your task:'
        response = await language_text(user_id, response)
        response += '\n'
        for task_id, task, date, time, status in tasks:
            if await check_language_ru(user_id):
                response += f"{task_id}. {task} (Дата: {date}, Время: {time}, Статус: {status})\n"
            else:
                status = await translate_text_to_en(status)
                response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        await message.answer(response)
        await state.set_state(Registration.confirmed)
    