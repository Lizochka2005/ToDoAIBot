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
        user_id INTEGER, points INTEGER,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id))''')

        await db.commit()

#Функция для получения стастистики
async def get_daily_stats(user_id: int):
  async with aiosqlite.connect("users.db") as db:
      today = datetime.date.today().strftime("%Y-%m-%d")
      async with db.execute("SELECT SUM(points) FROM tasks WHERE user_id = ? AND date = ?", (user_id, today)) as cursor:
          result = cursor.fetchone()[0] or 0
  return result


async def add_task(user_id: int, points: int, date: str):
    async with aiosqlite.connect("users.db") as db:
        db.execute("INSERT INTO tasks (user_id, points, date) VALUES (?, ?, ?)", (user_id, points, date))
        db.commit()

