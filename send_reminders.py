import aiosqlite
from initialisation import bot
from datetime import datetime, timedelta
from speech_functions import *
import keyboards as kb
from database.database_and_functions_GetStatistics import get_daily_stats

date = datetime.today().strftime('%Y-%m-%d')

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

                    response = f"Your tasks on {date}:"
                    response = await language_text(user_id, response)
                    response+='\n'
                    for task, time, status in tasks:
                        if await check_language_ru(user_id):
                            response += f"- {task} (Статус: {status}, Время: {time})\n"
                        else:
                            status = await translate_text_to_en(status)
                            response += f"- {task} (Status: {status}, Time: {time})\n"

                    await bot.send_message(chat_id=user_id,text=response)

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

                    response = f"Your tasks on {date}:"
                    response = await language_text(user_id, response)
                    response+='\n'
                    for deadline, time, status in deadlines:
                        if await check_language_ru(user_id):
                            response += f"- {deadline} (Статус: {status}, Время: {time})\n"
                        else:
                            status = await translate_text_to_en(status)
                            response += f"- {deadline} (Status: {status}, Time: {time})\n"

                    await bot.send_message(chat_id=user_id,text=response)

async def send_reminders_task(diff = 0):
    curr_time = datetime.now()
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

            for row in rows:
                user_id = row[0]
                async with db.execute(
                    "SELECT task, time, status FROM tasks WHERE user_id = ? AND date = ? AND time = ?",
                    (user_id, date, (curr_time+timedelta(minutes=diff)).strftime('%H:%M'), )
                ) as cursor:
                    tasks = await cursor.fetchall()

                    if not tasks:
                        continue

                    response = f"Your tasks starts in {diff} minutes:"
                    response = await language_text(user_id, response)
                    response+='\n'
                    for task, time, status in tasks:
                        if await check_language_ru(user_id):
                            response += f"- {task} (Статус: {status}, Время: {time})\n"
                        else:
                            status = await translate_text_to_en(status)
                            response += f"- {task} (Status: {status}, Time: {time})\n"

                    if diff == 0:
                        if await check_language_ru(user_id):
                            await bot.send_message(chat_id=user_id,text=response,reply_markup=kb.update_status_task_ru)
                        else:
                            await bot.send_message(chat_id=user_id,text=response,reply_markup=kb.update_status_task_en)
                    else:
                        await bot.send_message(chat_id=user_id,text=response)

async def send_reminders_deadline(diff = 0):
    curr_time = datetime.now()
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

            for row in rows:
                user_id = row[0]
                async with db.execute(
                    "SELECT deadline, time, status FROM deadlines WHERE user_id = ? AND date = ? AND time = ?",
                    (user_id, date, (curr_time+timedelta(minutes=diff)).strftime('%H:%M'), )
                ) as cursor:
                    deadlines = await cursor.fetchall()

                    if not deadlines:
                        continue

                    response = f"Your deadlines starts in {diff} minutes:"
                    response = await language_text(user_id, response)
                    response+='\n'
                    for deadline, time, status in deadlines:
                        if await check_language_ru(user_id):
                            response += f"- {deadline} (Статус: {status}, Время: {time})\n"
                        else:
                            status = await translate_text_to_en(status)
                            response += f"- {deadline} (Status: {status}, Time: {time})\n"

                    if diff == 0:
                        if await check_language_ru(user_id):
                            await bot.send_message(chat_id=user_id,text=response,reply_markup=kb.update_deadline_ru)
                        else:
                            await bot.send_message(chat_id=user_id,text=response,reply_markup=kb.update_deadline_en)
                    else:
                        await bot.send_message(chat_id=user_id,text=response)

async def send_reminders_statistic():
    curr_time = datetime.now()
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

            for row in rows:
                user_id = row[0]
                total_tasks, completed_tasks = await get_daily_stats(user_id)
                text = 'Statistic for today:'
                text = await language_text(user_id, text)
                text+='\n'
                if total_tasks == 0:
                    text1 = 'Today you had no tasks.'
                    text1 = await language_text(user_id, text1)
                    await bot.send_message(chat_id=user_id, text=text+text1)
                    return
                text1 = 'Today you have been done'
                text1 = await language_text(user_id, text1)
                text2 = 'tasks from'
                text2 = await language_text(user_id, text2)
                await bot.send_message(chat_id=user_id, text=f"{text}{text1} {completed_tasks} {text2} {total_tasks}.")


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

# Функция для отправки уведомлений вечером статистика
async def send_evening_reminders():
    await send_reminders_statistic()