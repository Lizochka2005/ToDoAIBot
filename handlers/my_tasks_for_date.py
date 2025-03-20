from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode
import aiosqlite

from states import Question, GetTaskListForDate, Registration, MySG
from speech_functions import *

from aiogram import Router

my_tasks_for_date = Router()


@my_tasks_for_date.message(Command("my_tasks_for_date"), Registration.confirmed)
async def ask_for_date(message: Message, state: FSMContext, dialog_manager: DialogManager):
    text = 'Choose the date:'
    text = await language_text(message.from_user.id, text)
    await state.update_data(user_id=message.from_user.id)
    await dialog_manager.start(MySG.main,
                               data={"text_from_chat": text, "flag": "tsk_fdt",
                                     "state": state},
                               mode=StartMode.RESET_STACK)
    await state.set_state(GetTaskListForDate.waiting_for_date)

@my_tasks_for_date.message(GetTaskListForDate.waiting_for_date)
async def show_tasks_for_date(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = user_data['data']
    user_id = user_data['user_id']

    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT task, status, date, time FROM tasks WHERE user_id=? and date=?",
            (
                user_id,
                date,
            ),
        ) as cursor:
            tasks = await cursor.fetchall()

            if not tasks:
                text = f'You have no tasks on {date}'
                text = await language_text(user_id, text)
                await message.answer(text)
                await state.set_state(Registration.confirmed)
                return

            response = f"Your tasks on {date}:"
            response = await language_text(user_id, response)
            response += '\n'
            for task, status, date, time in tasks:
                if await check_language_ru(user_id):
                    response += f"- {task} (Cтатус: {status}, Время: {time})\n"
                else:
                    status = await translate_text_to_en(status)
                    response += f"- {task} (Status: {status}, Time: {time})\n"
            
            await message.answer(response)
            await state.set_state(Registration.confirmed)
