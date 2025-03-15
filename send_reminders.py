import aiosqlite
from initialisation import bot
from datetime import datetime, timedelta
from speech_functions import *


date = datetime.today().date()
curr_time = datetime.now().time()

async def send_reminders_task_day_list():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

            for row in rows:
                user_id = row[0]
                async with db.execute(
                    "SELECT task, time, status FROM tasks WHERE user_id = ? AND date = ?",
                    (user_id, date,)
                ) as cursor:
                    tasks = await cursor.fetchall()

                    if not tasks:
                        continue

                    response = f"Your tasks on {date}:\n"
                    for task, status, time in tasks:
                        status = await translate_text_to_en(user_id, status)
                        response += f"- {task} (Status: {status}, Time: {time})\n"

                    response = await language_text(user_id, response)
                    await bot.answer(response)

async def send_reminders_deadline_day_list():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

            for row in rows:
                user_id = row[0]
                async with db.execute(
                    "SELECT deadline, time, status FROM deadlines WHERE user_id = ? AND date = ?",
                    (user_id, date,)
                ) as cursor:
                    deadlines = await cursor.fetchall()

                    if not deadlines:
                        continue

                    response = f"Your tasks on {date}:\n"
                    for deadline, status, time in deadlines:
                        status = await translate_text_to_en(user_id, status)
                        response += f"- {deadline} (Status: {status}, Time: {time})\n"

                    response = await language_text(user_id, response)
                    await bot.answer(response)

async def send_reminders_task(diff = 0):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

            for row in rows:
                user_id = row[0]
                async with db.execute(
                    "SELECT task, time, status FROM tasks WHERE user_id = ? AND date = ? AND time = ?",
                    (user_id, date, (curr_time-timedelta(minutes=diff)).strftime('%H:%M:%S'), )
                ) as cursor:
                    tasks = await cursor.fetchall()

                    if not tasks:
                        continue

                    response = f"Your tasks starts in {diff} minutes:\n"
                    for task, status, time in tasks:
                        status = await translate_text_to_en(user_id, status)
                        response += f"- {task} (Status: {status}, Time: {time})\n"

                    response = await language_text(user_id, response)
                    await bot.answer(response)

async def send_reminders_deadline(diff = 0):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

            for row in rows:
                user_id = row[0]
                async with db.execute(
                    "SELECT deadline, time, status FROM deadlines WHERE user_id = ? AND date = ? AND time = ?",
                    (user_id, date, (curr_time-timedelta(minutes=diff)).strftime('%H:%M:%S'), )
                ) as cursor:
                    deadlines = await cursor.fetchall()

                    if not deadlines:
                        continue

                    response = f"Your deadlines starts in {diff} minutes:\n"
                    for deadline, status, time in deadlines:
                        status = await translate_text_to_en(user_id, status)
                        response += f"- {deadline} (Status: {status}, Time: {time})\n"

                    response = await language_text(user_id, response)
                    await bot.answer(response)