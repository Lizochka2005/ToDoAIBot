from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram import F
import aiosqlite
import keyboards as kb
from states import Registration
from speech_functions import language_text, check_language_ru

notifications = Router()

# @notifications.message(F.text == "Напоминания", Registration.confirmated)
# async def setNotifications(message: Message):
#     text = 'Would you like to receive daily reminders?'
#     text = language_text(message.from_user.id, text)
#     if await check_language_ru(message.from_user.id):
#         await message.answer(text, reply_markup=kb.setNotifications_ru,)
#     else:
#         await message.answer(text, reply_markup=kb.setNotifications_en,)

@notifications.message(Command("notifications_on"))
async def enable_notifications(message: Message):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE users SET subscribed = TRUE WHERE user_id = ?",
            (message.from_user.id,),
        )
        await db.commit()

    text = 'Notifications are enabled. Now you will receive a reminder every day.'
    text = await language_text(message.from_user.id, text)
    await message.answer(text)

@notifications.message(Command("notifications_off"))
async def disable_notifications(message: Message):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE users SET subscribed = FALSE WHERE user_id = ?",
            (message.from_user.id,),
        )
        await db.commit()

    text = 'Notifications are disabled. You will not receive reminders.'
    text = await language_text(message.from_user.id, text)
    await message.answer(text)