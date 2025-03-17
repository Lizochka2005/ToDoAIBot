from send_reminders import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

def setup_scheduler():
    # Уведомления утром списком (например, в 8:00 утра)
    scheduler.add_job(send_morning_reminders, 'cron', hour=8, minute=0)

    # Уведомления за час до начала задачи
    scheduler.add_job(send_reminders_1_hour_before, 'interval', minutes=60)

    # Уведомления за 30 минут до начала задачи
    scheduler.add_job(send_reminders_30_minutes_before, 'interval', minutes=30)

    # Уведомления за 15 минут до начала задачи
    scheduler.add_job(send_reminders_15_minutes_before, 'interval', minutes=15)

    # Уведомления в момент начала задачи
    scheduler.add_job(send_reminders_at_start, 'interval', minutes=1)

    # Запуск планировщика
    scheduler.start()