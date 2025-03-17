from aiogram import Router
from aiogram.types import Message
from speech_functions import *
from aiogram.fsm.context import FSMContext

default_handler = Router()


# реакция на любое действие
@default_handler.message(flags={"priority": -100})
async def answerForEverything(message: Message, state: FSMContext):
    if state is None:
        text = 'You have no registration.😓 Please register your account!'
    else:
        text = "Don't know what to answer😓 Try using commands"
        text = await language_text(message.from_user.id, text)
    await message.answer(text)
