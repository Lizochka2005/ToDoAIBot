import asyncio
import logging
from langchain_groq import ChatGroq

from database.database_and_functions_GetStatistics import start_db

# from handlers.calendar_start import calendar_start
# from handlers.add_deadline import add_deadline
from handlers.add_task import add_task
from handlers.my_nearest_tasks import my_nearest_tasks
from handlers.my_tasks_for_date import my_tasks_for_date
from handlers.my_tasks_for_today import my_tasks_for_today
from handlers.start import start

# from handlers.update_deadline import update_deadline
from handlers.update_task import update_task
from handlers.callbacks import callbacks
from handlers.default_handler import default_handler
from handlers.answer_question import answer_question
from handlers.calendar_start import dialog
from handlers.notifications import notifications
from handlers.edit_profile import edit_profile
from handlers.super_agent import super_agent
from initialisation import bot, dp
from aiogram_dialog import setup_dialogs
from set_scheduler import setup_scheduler


async def main():
    # dp.include_router(calendar_start)
    # Подключаем все роутеры
    dp.include_router(start)
    dp.include_router(answer_question)
    # dp.include_router(add_deadline)
    dp.include_router(add_task)
    # dp.include_router(my_nearest_deadlines)
    dp.include_router(my_nearest_tasks)
    dp.include_router(my_tasks_for_date)
    dp.include_router(my_tasks_for_today)
    # dp.include_router(update_deadline)
    dp.include_router(update_task)
    dp.include_router(callbacks)
    dp.include_router(notifications)
    dp.include_router(edit_profile)
    dp.include_router(super_agent)
    dp.include_router(default_handler)

    setup_scheduler()

    dp.include_router(dialog)
    setup_dialogs(dp)

    dp.startup.register(start_db)
    try:
        print("Бот запущен...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        print("Бот остановлен")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


"""git commit -m "Агенты работают" -m "Добавил агентов на все функции,
 пользоваться ими надо аккуратно, максимально точно формулировать запрос" """
