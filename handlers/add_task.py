
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram_dialog import DialogManager, StartMode
from datetime import datetime

from speech_functions import *
from states import TaskCreation, Question, Registration, MySG

add_task = Router()

#Registration.confirmed убран, с ним не работает не стал разбираться почему
@add_task.message(Command("add_task"))
async def add_task_cmd(message: Message, state: FSMContext):
  text = 'Enter task:'
  text = await language_text(message.from_user.id, text)
  await message.answer(text)
  await state.set_state(TaskCreation.waiting_for_task)

#Эту функцию будем использовать в качестве коллбэка на кнопку под задачей, после присылания уведомления о начале времени задачи

# @dp.message(TaskCreation.waiting_for_task)
# async def process_task(message: Message, state: FSMContext):
#   await state.update_data(task=message.text)
#   await message.answer("Выберите статус задачи:\n1. Выполнено\n2. Выполнено частично\n3. Отложено")
#   await state.set_state(TaskCreation.waiting_for_status)


#Не трогайте пожалуйста, оно очень хрупкое((
@add_task.message(TaskCreation.waiting_for_task)
async def process_deadline(message: Message, state: FSMContext, dialog_manager: DialogManager):
  await state.update_data(task=message.text)
  state_data = await state.get_data()
  task_text = state_data.get("task", "No deadline text")
  text = 'Choose the date you want to complete the task:'
  text = await language_text(message.from_user.id, text)
  await dialog_manager.start(MySG.main, data={"text_from_chat": text, "deadline_or_task_text": task_text, "flag": "tsk", "state": state},
                             mode=StartMode.RESET_STACK)
  # await message.answer('Введите время в формате HH:MM') оно в calendar_start: on_date_selected
  await state.set_state(TaskCreation.waiting_for_time)

#Это будет функция коллбэка на выбранную дату для выбора времени
@add_task.message(TaskCreation.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
  time = message.text
  user_data = await state.get_data()
  task = user_data['task']
  data = user_data['data']
  time = message.text
  try:
    a = time.split(':')
    if len(a)!=2 or len(a[0])!=2 or len(a[1])!=2:
      text = 'Incorrect time, please try again!'
      text = await language_text(message.from_user.id, text)
      await message.answer(text)
      text = 'Enter time in format HH:MM'
      text = await language_text(message.from_user.id, text)
      await message.answer(text)
      await state.set_state(TaskCreation.waiting_for_time)
    elif (a[0][:1]!=0 and int(a[0])>24) or (a[1][:1]!=0 and int(a[1])>=60):
      text = 'Incorrect time, please try again!'
      text = await language_text(message.from_user.id, text)
      await message.answer(text)
      text = 'Enter time in format HH:MM'
      text = await language_text(message.from_user.id, text)
      await message.answer(text)
      await state.set_state(TaskCreation.waiting_for_time)
  except Exception as e:
    text = 'Incorrect time, please try again!'
    text = await language_text(message.from_user.id, text)
    await message.answer(text)
    text = 'Enter time in format HH:MM'
    text = await language_text(message.from_user.id, text)
    await message.answer(text)
    await state.set_state(TaskCreation.waiting_for_time)

  async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT INTO tasks(user_id, task, date, time) VALUES (?, ?, ?, ?)",
            (message.from_user.id, task, data, time),
        )
        await db.commit()

  date = datetime.strptime(date, '%Y-%m-%d')
  formatted_date = date.strftime('%d %B %Y')
  if await check_language_ru(message.from_user.id):
    date = formatted_date.split(' ')
    month = await language_text(message.from_user.id, date[1])
    formatted_date = f'{date[0]} {month} {date[-1]}'

  text1 = "Task added!"
  text1 = await language_text(message.from_user.id, text1)
  text2 = 'Task:'
  text2 = await language_text(message.from_user.id, text2)
  text3 = 'Date'
  text3 = await language_text(message.from_user.id, text3)
  text4 = 'Time'
  text4 = await language_text(message.from_user.id, text4)
  text = f'{text1}\n{text2} {task}\n{text3} {formatted_date}\n{text4} {time}'
  await message.answer(text)
  await state.clear()
