from aiogram import Router
from aiogram.types import Message
from speech_functions import *

default_handler = Router()


# реакция на любое действие
@default_handler.message(flags={"priority": -100})
async def answerForEverything(message: Message):
    text = "Don't know what to answer😓 Try using commands"
    # text = await language_text(message.from_user.id, text)
    await message.answer(text)
