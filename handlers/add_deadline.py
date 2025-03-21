from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode
import aiosqlite
from datetime import datetime

from speech_functions import *
from states import *


add_deadline = Router()

#Registration.confirmed убран, с ним не работает не стал разбираться почему
@add_deadline.message(Command("add_deadline"))
async def add_deadline_cmd(message: Message, state: FSMContext):
  text = 'Enter the name of the deadline:'
  text = await language_text(message.from_user.id, text)
  await message.answer(text)
  await state.set_state(DeadlineCreation.waiting_for_deadline)


#Не трогайте пожалуйста, оно очень хрупкое((
@add_deadline.message(DeadlineCreation.waiting_for_deadline)
async def process_deadline(message: Message, dialog_manager: DialogManager, state: FSMContext):
  await state.update_data(deadline=message.text)
  state_data = await state.get_data()
  deadline_text = state_data.get("deadline", "No deadline text")
  text = 'Choose the date on which the term expires:'
  text = await language_text(message.from_user.id, text)
  await dialog_manager.start(MySG.main, data={"text_from_chat": text, "deadline_or_task_text": deadline_text, "flag": "dd", "state": state},
                             mode=StartMode.RESET_STACK)
  # await message.answer('Введите время в формате HH:MM') оно в calendar_start: on_date_selected
  await state.set_state(DeadlineCreation.waiting_for_time)

#Это будет функция коллбэка на выбранную дату для выбора времени
@add_deadline.message(DeadlineCreation.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
  time = message.text
  user_data = await state.get_data()
  deadline = user_data['deadline']
  data = user_data['data']
  time = message.text
  try:
    a = time.split(':')
    if len(a)!=2 or len(a[0])!=2 or len(a[1])!=2:
      text = 'Incorrect time, please try again!'
      text = await language_text(message.from_user.id, text)
      await message.answer(text)
      return
    elif (a[0][:1]!=0 and int(a[0])>24) or (a[1][:1]!=0 and int(a[1])>=60):
      text = 'Incorrect time, please try again!'
      text = await language_text(message.from_user.id, text)
      await message.answer(text)
      return
  except Exception as e:
    text = 'Incorrect time, please try again!'
    text = await language_text(message.from_user.id, text)
    await message.answer(text)
    return

  async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT INTO deadlines(user_id, deadline, date, time) VALUES (?, ?, ?, ?)",
            (message.from_user.id, deadline, data, time),
        )
        await db.commit()

  date = datetime.strptime(date, '%Y-%m-%d')
  formatted_date = date.strftime('%d %B %Y')
  if await check_language_ru(message.from_user.id):
    date = formatted_date.split(' ')
    month = await language_text(message.from_user.id, date[1])
    formatted_date = f'{date[0]} {month} {date[-1]}'

  text1 = "Deadline added!"
  text1 = await language_text(message.from_user.id, text1)
  text2 = 'Deadline:'
  text2 = await language_text(message.from_user.id, text2)
  text3 = 'Date'
  text3 = await language_text(message.from_user.id, text3)
  text4 = 'Time'
  text4 = await language_text(message.from_user.id, text4)
  text = f'{text1}\n{text2} {deadline}\n{text3} {formatted_date}\n{text4} {time}'
  await message.answer(text)
  await state.clear()
