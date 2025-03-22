
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram import Router

from states import DeadlineUpdate, Registration
from speech_functions import *
import keyboards as kb

update_deadline = Router()

@update_deadline.message(Command("update_deadline"))
async def update_deadline_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE user_id=? ORDER BY date, time", (user_id,)) as cursor:
        deadlines = await cursor.fetchall()

        if not deadlines:
            text = 'You have no deadlines.'
            text = await language_text(user_id, text)
            await message.answer(text)
            return

        response = "Your deadlines:"
        response = await language_text(user_id, response)
        response += '\n'
        for deadline_id, deadline, date, time, status in deadlines:
            if await check_language_ru(user_id):
                response += f"{deadline_id}. {deadline} (Дата: {date}, Время: {time}, Статус: {status})\n"
            else:
                status = await translate_text_to_en(status)
                response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

        text = "Enter the number of deadline which you want to update:"
        text = await language_text(user_id, text)
        response += text
        await message.answer(response)
        await state.set_state(DeadlineUpdate.waiting_for_deadline_id)

@update_deadline.message(DeadlineUpdate.waiting_for_deadline_id)
async def process_task_id(message: Message, state: FSMContext):
    deadline_id = message.text
    if not deadline_id.isdigit():
        text = "Please, enter the integer number of deadline."
        text = await language_text(message.from_user.id, text)
        await message.answer(text)
        return

    await state.update_data(deadline_id=deadline_id)
    text = 'Choose what you want to update:'
    text = await language_text(message.from_user.id, text)
    if await check_language_ru(message.from_user.id):
        await message.answer(text, reply_markup=kb.update_deadline_ru)
    else:
        await message.answer(text, reply_markup=kb.update_deadline_ru)

@update_deadline.message(DeadlineUpdate.waiting_for_new_time)
async def set_new_time_for_deadline(message: Message, state: FSMContext):
    user_data = await state.get_data()
    time = message.text
    user_id = message.from_user.id
    id = user_data["deadline_id"]
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
            text = 'Enter the time you want to change the deadline execution in format HH:MM :'
            text = await language_text(user_id, text)
            await message.answer(text)
            await state.set_state(DeadlineUpdate.waiting_for_new_time)
        elif (int(a[0][:1]) != 0 and int(a[0]) > 23) or (int(a[1][:1]) != 0 and a[1] >= 60):
            text = 'Incorrect time, please try again!'
            text = await language_text(user_id, text)
            await message.answer(text)
            text = 'Enter the time you want to change the deadline execution in format HH:MM :'
            text = await language_text(user_id, text)
            await message.answer(text)
            await state.set_state(DeadlineUpdate.waiting_for_new_time)
    except Exception as e:
        text = 'Incorrect time, please try again!'
        text = await language_text(user_id, text)
        await message.answer(text)
        text = 'Enter the time you want to change the deadline execution in format HH:MM :'
        text = await language_text(user_id, text)
        await message.answer(text)
        await state.set_state(DeadlineUpdate.waiting_for_new_time)

    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE deadlines SET time = ? WHERE id=?",
            (
                time,
                id,
            ),
        )
        await db.commit()
    
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE id = ?", (id,)) as cursor:
        deadlines = await cursor.fetchall()

        response = "Your deadline:"
        response = await language_text(user_id, response)
        response += '\n'
        for deadline_id, deadline, date, time, status in deadlines:
            if await check_language_ru(user_id):
                response += f"{deadline_id}. {deadline} (Дата: {date}, Время: {time}, Статус: {status})\n"
            else:
                status = await translate_text_to_en(status)
                response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

        await message.answer(response)
    await state.clear()


@update_deadline.message(DeadlineUpdate.waiting_for_new_date)
async def set_new_date_for_deadline(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = user_data['date']
    user_id = user_data['user_id']
    id = user_data["deadline_id"]
    
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE deadlines SET date = ? WHERE id=?",
            (
                date,
                id,
            ),
        )
        await db.commit()
    
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE id = ?", (id,)) as cursor:
        deadlines = await cursor.fetchall()

        response = "Your deadline:"
        response = await language_text(user_id, response)
        response += '\n'
        for deadline_id, deadline, date, time, status in deadlines:
            if await check_language_ru(user_id):
                response += f"{deadline_id}. {deadline} (Дата: {date}, Время: {time}, Статус: {status})\n"
            else:
                status = await translate_text_to_en(status)
                response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

        await message.answer(response)
    await state.clear()

    