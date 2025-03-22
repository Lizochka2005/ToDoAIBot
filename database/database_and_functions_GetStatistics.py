import aiosqlite
import asyncio
import datetime

async def start_db():
    """Создает таблицы users, tasks, deadlines в базе данных users если их еще нет"""
    async with aiosqlite.connect("users.db") as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        name TEXT,
                        language TEXT,
                        subscribed BOOLEAN DEFAULT TRUE)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      task TEXT,
                      status TEXT DEFAULT 'Не выполнено',
                      date TEXT,
                      time TEXT,
                      FOREIGN KEY (user_id) REFERENCES users(user_id))''')
        # await db.execute('''CREATE TABLE IF NOT EXISTS deadlines (
        #               id INTEGER PRIMARY KEY AUTOINCREMENT,
        #               user_id INTEGER,
        #               deadline TEXT,
        #               status TEXT DEFAULT 'Не завершён',
        #               date TEXT,
        #               time TEXT,
        #               FOREIGN KEY (user_id) REFERENCES users(user_id))''')

        await db.commit()

# Функция для получения статистики за день
async def get_daily_stats(user_id: int):
    async with aiosqlite.connect("users.db") as db:

      today = datetime.date.today().strftime("%Y-%m-%d")
      # Считаем общее количество задач за сегодня
      async with db.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND date = ?", (user_id, today)) as cursor:
        total_tasks = await cursor.fetchone()
        total_tasks = total_tasks[0] or 0

      # Считаем количество выполненных задач за сегодня
      async with db.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND date = ? AND status = ?", (user_id, today, "Выполнено")) as cursor:
        completed_tasks = await cursor.fetchone()
        completed_tasks = completed_tasks[0] or 0

    return total_tasks, completed_tasks
