#pip install aiogram-dialog

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, Message, CallbackQuery
from aiogram.filters import Command
import logging
from aiogram_dialog import Dialog, DialogManager, Window, StartMode, setup_dialogs
from aiogram_dialog.widgets.kbd import Calendar
from aiogram.filters.state import State, StatesGroup
from datetime import date

from aiogram_dialog.widgets.text import Const

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token='8170498248:AAHxTsGCJ0NEP_7Qjs9xQQXTmhC19zEmQ_w')
dp = Dispatcher(storage=storage)

async def start_bot(dp: Dispatcher):
    commands = [BotCommand(command='menu', description='Перейти в меню'),
                BotCommand(command='info', description='Дополнительная информация')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    await callback.answer(str(selected_date))

calendar = Calendar(id='calendar', on_click=on_date_selected)

class MySG(StatesGroup):
    main = State()

main_window = Window(Const("Выберите дату:"), calendar, state=MySG.main)

dialog = Dialog(main_window)

dp.include_router(dialog)

@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)

setup_dialogs(dp)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is closed')
