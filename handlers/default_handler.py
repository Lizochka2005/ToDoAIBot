from aiogram import Router
from aiogram.types import Message

default_handler = Router()


# реакция на любое действие
@default_handler.message(flags={"priority": -100})
async def answerForEverything(messege: Message):
    await messege.answer("не знаю что на это ответить :( попробуй использовать команды")
