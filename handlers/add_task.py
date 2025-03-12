
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router


from states import TaskCreation, Question

add_task = Router()

@add_task.message(Command("add_task"))
async def add_task_cmd(message: Message, state: FSMContext):
  await message.answer("Введите задачу:")
  await state.set_state(TaskCreation.waiting_for_task)

#Эту функцию будем использовать в качестве коллбэка на кнопку под задачей, после присылания уведомления о начале времени задачи

# @dp.message(TaskCreation.waiting_for_task)
# async def process_task(message: Message, state: FSMContext):
#   await state.update_data(task=message.text)
#   await message.answer("Выберите статус задачи:\n1. Выполнено\n2. Выполнено частично\n3. Отложено")
#   await state.set_state(TaskCreation.waiting_for_status)

@add_task.message(TaskCreation.waiting_for_task)
async def process_task(message: Message, state: FSMContext):
  await state.update_data(task=message.text)
  await message.answer("Выберите дату, на которую хотите поставить выполнение задачи")
  await state.set_state(TaskCreation.waiting_for_date)

@add_task.message(TaskCreation.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
  # здесь должен быть календарь Феди
  await state.set_state(TaskCreation.waiting_for_time)
  pass

#Это будет функция коллбэка на выбранную дату для выбора времени
@add_task.message(TaskCreation.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
  # здесь должен быть календарь Феди
  # await message.answer(f"Задача добавлена!\nЗадача: {task}\nДата: {date}\nВремя: {time}")
  # await state.set_state(Start.question)
  pass