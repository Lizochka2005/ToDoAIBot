@dp.message(Command("my_nearest_deadlines"), Start.question)
async def show_tasks_for_today(message: Message):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT deadline, date, time FROM deadlines WHERE user_id=? and status not like('Завершён')", (user_id,)) as cursor:
        deadlines = cursor.fetchall()

        if not deadlines:
            await message.answer("У вас нет ближайших дэдлайнов.")
            return

        response = "Ваши ближайшие дэдлайны:\n"
        for deadline, date, time in deadlines:
            response += f"- {deadline} (Дата: {date}, Время: {time})\n"
        await message.answer(response)
