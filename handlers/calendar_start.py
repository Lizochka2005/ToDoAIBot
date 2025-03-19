from functools import partial

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiosqlite
from speech_functions import *
from datetime import date
from aiogram_dialog import DialogManager, Window, Dialog
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.text import Format
from initialisation import dp

from aiogram.fsm.context import FSMContext
from states import Registration, Question, MySG, DeadlineCreation


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    state = manager.start_data.get("state")  # Получаем state из start_data
    if not state:
        await callback.message.answer("Error: State not found")
        await manager.done()
        return

    deadline_or_task_text = manager.start_data.get("deadline_or_task_text", "No deadline or task text")
    flag = manager.start_data.get("flag", "No flag")
    formatted_deadline_or_task = await Format("{start_data[deadline_or_task_text]}").render_text(
        {"start_data": {"deadline_or_task_text": deadline_or_task_text}}, manager
    )
    formatted_flag = await Format("{start_data[flag]}").render_text(
        {"start_data": {"flag": flag}}, manager
    )
    if formatted_flag == "dd":
        text = "Your new deadline:"
    elif formatted_flag == "tsk":
        text = "You entered a new task:"
    elif formatted_flag == "upd_dd":
        text = "You updated the date of the deadline:"
    elif formatted_flag == "upd_tsk":
        text = "You updated the date of the task:"
    else:
        await callback.message.answer("Error: Incorrect usage of calendar")
        await manager.done()
    text = await language_text(callback.from_user.id, text)
    if formatted_flag == "dd" or formatted_flag == "tsk":
        await callback.message.answer(f"{text}\n{selected_date} - {formatted_deadline_or_task}")
    elif formatted_flag == "upd_dd" or formatted_flag == "upd_tsk":
        await callback.message.answer(f"{text}\n{selected_date}")
    await state.update_data({"data": selected_date})
    text = 'Enter time in format HH:MM'
    text = await language_text(callback.from_user.id, text)
    await callback.message.answer(text)
    await manager.done()

calendar = Calendar(id='calendar', on_click=on_date_selected)

main_window = Window(Format("{start_data[text_from_chat]}"), calendar, state=MySG.main)

dialog = Dialog(main_window)
