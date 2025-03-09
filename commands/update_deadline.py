@dp.message(Command("update_deadline"))
async def update_deadline_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE user_id=? and status not like('Завершён')", (user_id,)) as cursor:
        deadlines = cursor.fetchall()

        if not deadlines:
            await message.answer("У вас нет дэдлайнов.")
            return

        response = "Ваши дэдлайны:\n"
        for deadline_id, deadline, date, time, status in deadlines:
            response += f"{deadline_id}. {deadline} (Дата: {date}, Время: {time}, Статус: {status})\n"

        await message.answer(response + "Введите ID дэдлайна, который хотите обновить:")
        await state.set_state(DeadlineUpdate.waiting_for_deadline_id)

@dp.message(DeadlineUpdate.waiting_for_deadline_id)
async def process_task_id(message: Message, state: FSMContext):
    deadline_id = message.text
    if not deadline_id.isdigit():
        await message.answer("Пожалуйста, введите числовой ID дэдлайна.")
        return

    await state.update_data(deadline_id=deadline_id)
    # здесь надо изменить на сообщение выбора, что хотят изменить + кнопочки (дата, время, статус)
    # await message.answer("Выберите новый статус задачи:\n1. Выполнено\n2. Выполнено частично\n3. Отложено")
    # await state.set_state(TaskUpdate.waiting_for_new_status)
    pass