from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram_dialog import DialogManager, StartMode

from speech_functions import language_text, check_language_ru
from states import TaskCreation, MySG
from datetime import datetime
import aiosqlite

add_task = Router()


# Registration.confirmed убран, с ним не работает не стал разбираться почему
@add_task.message(Command("add_task"))
async def add_task_cmd(message: Message, state: FSMContext):
    text = "Enter task:"
    text = await language_text(message.from_user.id, text)
    await message.answer(text)
    await state.set_state(TaskCreation.waiting_for_task)

# Не трогайте пожалуйста, оно очень хрупкое((
@add_task.message(TaskCreation.waiting_for_task)
async def process_deadline(
    message: Message, state: FSMContext, dialog_manager: DialogManager
):
    await state.update_data(task=message.text)
    state_data = await state.get_data()
    task_text = state_data.get("task", "No deadline text")
    text = "Choose the date you want to complete the task:"
    text = await language_text(message.from_user.id, text)
    await dialog_manager.start(
        MySG.main,
        data={
            "text_from_chat": text,
            "deadline_or_task_text": task_text,
            "flag": "tsk",
            "state": state,
        },
        mode=StartMode.RESET_STACK,
    )
    # await message.answer('Введите время в формате HH:MM') оно в calendar_start: on_date_selected
    await state.set_state(TaskCreation.waiting_for_time)


# Это будет функция коллбэка на выбранную дату для выбора времени
@add_task.message(TaskCreation.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    time = message.text
    user_data = await state.get_data()
    task = user_data["task"]
    date = user_data["date"]
    time = message.text
    correct_time = True
    try:
        a = time.split(":")
        if (
            (len(a) != 2 or len(a[0]) != 2 or len(a[1]) != 2)
            or (int(a[0][:1]) <= 0 and int(a[0]) >= 24)
            or (int(a[1][:1]) <= 0 and int(a[1]) >= 60)
        ):
            await message.answer(
                await language_text(
                    message.from_user.id, "Incorrect time, please try again!"
                )
            )
            await message.answer(
                await language_text(message.from_user.id, "Enter time in format HH:MM")
            )
            await state.set_state(TaskCreation.waiting_for_time)
            correct_time = False
    except Exception as e:
        await message.answer(
            await language_text(
                message.from_user.id, "Incorrect time, please try again!"
            )
        )
        await message.answer(
            await language_text(message.from_user.id, "Enter time in format HH:MM")
        )
        await state.set_state(TaskCreation.waiting_for_time)
        correct_time = False

    if correct_time == True:
        async with aiosqlite.connect("users.db") as db:
            await db.execute(
                "INSERT INTO tasks(user_id, task, date, time) VALUES (?, ?, ?, ?)",
                (message.from_user.id, task, date, time),
            )
            await db.commit()
        
        date = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date.strftime('%d %B %Y')
        if await check_language_ru(message.from_user.id):
            date = formatted_date.split(' ')
            month = await language_text(message.from_user.id, date[1])
            formatted_date = f'{date[0]} {month} {date[-1]}'
        await message.answer(
            f"""
{await language_text(message.from_user.id, "Task added")}!
{await language_text(message.from_user.id, "Task")}: {task}
{await language_text(message.from_user.id, "Date")}: {formatted_date}
{await language_text(message.from_user.id, "Time")}: {time}"""
        )
        await state.clear()
