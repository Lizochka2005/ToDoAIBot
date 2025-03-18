import aiosqlite
from initialisation import bot
from datetime import datetime, timedelta
from speech_functions import *
import keyboards as kb


date = datetime.today().date()
curr_time = datetime.now()

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
                    if diff == 0:
                        if await check_language_ru(user_id):
                            await bot.send_message(response,reply_markup=kb.update_status_task_ru)
                        else:
                            await bot.send_message(response,reply_markup=kb.update_status_task_en)

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
                    if diff == 0:
                        if await check_language_ru(user_id):
                            await bot.send_message(response,reply_markup=kb.update_deadline_ru)
                        else:
                            await bot.send_message(response,reply_markup=kb.update_deadline_en)

# Функция для отправки уведомлений утром списком
async def send_morning_reminders():
    await send_reminders_task_day_list()
    await send_reminders_deadline_day_list()

# Функция для отправки уведомлений за час до начала задачи
async def send_reminders_1_hour_before():
    await send_reminders_task(60)
    await send_reminders_deadline(60)

# Функция для отправки уведомлений за 30 минут до начала задачи
async def send_reminders_30_minutes_before():
    await send_reminders_task(30)
    await send_reminders_deadline(30)

# Функция для отправки уведомлений за 15 минут до начала задачи
async def send_reminders_15_minutes_before():
    await send_reminders_task(15)
    await send_reminders_deadline(15)

# Функция для отправки уведомлений в момент начала задачи
async def send_reminders_at_start():
    await send_reminders_task(0)
    await send_reminders_deadline(0)