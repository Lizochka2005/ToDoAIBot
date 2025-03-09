@dp.message(Command("add_deadline"), Start.question)
async def add_task_cmd(message: Message, state: FSMContext):
  await message.answer("Введите название дэдлайна:")
  await state.set_state(DeadlineCreation.waiting_for_deadline)

@dp.message(DeadlineCreation.waiting_for_deadline)
async def process_task(message: Message, state: FSMContext):
  await state.update_data(deadline=message.text)
  await message.answer("Выберите дату, когда истекает срок дэдлайна")
  await state.set_state(DeadlineCreation.waiting_for_date)

@dp.message(DeadlineCreation.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
  # здесь должен быть календарь Феди
  # await message.answer('Введите время в формате HH:MM')
  await state.set_state(DeadlineCreation.waiting_for_time)
  pass

#Это будет функция коллбэка на выбранную дату для выбора времени
@dp.message(DeadlineCreation.waiting_for_time)
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
  # await state.set_state(Start.question)
  pass