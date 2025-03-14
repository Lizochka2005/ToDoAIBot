import aiosqlite
import asyncio
import datetime

async def start_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        name TEXT,
                        language TEXT)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      task TEXT,
                      status TEXT DEFAULT 'Не выполнено',
                      date DATE,
                      time TIME,
                      FOREIGN KEY (user_id) REFERENCES users(user_id))''')
        await db.execute('''CREATE TABLE IF NOT EXISTS deadlines (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      deadline TEXT,
                      status TEXT DEFAULT 'Не завершён',
                      date DATE,
                      time TIME,
                      FOREIGN KEY (user_id) REFERENCES users(user_id))''')

        await db.commit()

# Функция для получения статистики за день
async def get_daily_stats(user_id: int):
    async with aiosqlite.connect("users.db") as db:

      today = datetime.date.today().strftime("%Y-%m-%d")
      # Считаем общее количество задач за сегодня
      async with db.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND date = ?", (user_id, today)) as cursor:
        total_tasks = cursor.fetchone()[0] or 0

      # Считаем количество выполненных задач за сегодня
      async with db.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND date = ? AND status = ?", (user_id, today, "выполнено")) as cursor:
        completed_tasks = cursor.fetchone()[0] or 0

    return total_tasks, completed_tasks