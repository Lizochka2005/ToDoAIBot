from send_reminders import send_morning_reminders, send_reminders_1_hour_before, send_reminders_30_minutes_before, send_reminders_15_minutes_before, send_reminders_at_start, send_evening_reminders

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

def setup_scheduler():
    # Уведомления утром списком (например, в 8:00 утра)
    scheduler.add_job(send_morning_reminders, 'cron', hour=8, minute=8)

    # Уведомления за час до начала задачи
    scheduler.add_job(send_reminders_1_hour_before, 'interval', minutes=1)

    # Уведомления за 30 минут до начала задачи
    scheduler.add_job(send_reminders_30_minutes_before, 'interval', minutes=1)

    # Уведомления за 15 минут до начала задачи
    scheduler.add_job(send_reminders_15_minutes_before, 'interval', minutes=1)

    # Уведомления в момент начала задачи
    scheduler.add_job(send_reminders_at_start, 'interval', minutes=1)

    # Уведомления вечером статистика (например, в 21:00 вечера)
    scheduler.add_job(send_evening_reminders, 'cron', hour=21, minute=0)

    # Запуск планировщика
    scheduler.start()