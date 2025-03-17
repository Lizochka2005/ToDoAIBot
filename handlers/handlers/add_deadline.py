
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from speech_functions import *
from states import Question, DeadlineCreation, Registration


add_deadline = Router()

@add_deadline.message(Command("add_deadline"), Registration.confirmed)
async def add_task_cmd(message: Message, state: FSMContext):
  text = 'Enter the name of the deadline:'
  text = await language_text(message.from_user.id, text)
  await message.answer(text)
  await state.set_state(DeadlineCreation.waiting_for_deadline)

@add_deadline.message(DeadlineCreation.waiting_for_deadline)
async def process_task(message: Message, state: FSMContext):
  await state.update_data(deadline=message.text)
  text = 'Choose the date on wich the term expires'
  text = await language_text(message.from_user.id, text)
  await message.answer(text)
  await state.set_state(DeadlineCreation.waiting_for_date)

@add_deadline.message(DeadlineCreation.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
  # здесь должен быть календарь Феди
  # await message.answer('Введите время в формате HH:MM')
  await state.set_state(DeadlineCreation.waiting_for_time)

#Это будет функция коллбэка на выбранную дату для выбора времени
@add_deadline.message(DeadlineCreation.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
  # time = message.text
  # try:
  #   a = time.split(':')
  #   if len(a)!=2 or len(a[0])!=2 or len(a[1])!=2:
  #     await message.answer('Некорректно введено время, попробуйте ещё раз!')
  #     return
  #   elif (a[0][:1]!=0 and int(a[0])>24) or (a[1][:1]!=0 and int(a[1])>=60):
  #     await message.answer('Некорректно введено время, попробуйте ещё раз!')
  #     return
  # except Exception as e:
  #   await message.answer('Некорректно введено время, попробуйте ещё раз!')
  #   return
  # await message.answer(f"Дэдлайн добавлен!\nДэдлайн: {deadline}\nДата: {date}\nВремя: {time}")
  # await state.set_state(Registration.confirmed)
  pass