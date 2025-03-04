
# pip install gTTS
# pip install aiogram
# pip install asyncio
# pip install langchain
# pip install langchain-groq

from gtts import gTTS
import os

def text_to_speech(text):
  res = gTTS(text=text, lang='en')
  filename = "output.mp3"
  res.save(filename)
  os.system(f"start {filename}")

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import asyncio

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(model="llama3-70b-8192")

token_bot = '7685591016:AAG8M4rZPovKNrOuKqq6sMwT8stOg1vk2rc'

bot = Bot(token=token_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

class Start(StatesGroup):
  question = State()

@dp.message(CommandStart(), State(None))
async def cmd_start(message: Message, state: FSMContext):
  await message.answer('Привет, готов ответить на твой вопрос!')
  await state.set_state(Start.question)

@dp.message(F.text, Start.question)
async def llm_answer(message: Message, state: FSMContext):
  try:
    print('УАУАУАУАУА')
    prompt_template = PromptTemplate(
        input_variables=["input_text"],
        template="{input_text}"
    )
    solver_chain = LLMChain(llm=llm, prompt=prompt_template, output_key='answer')
    print('Промпт отправлен')
    answer = solver_chain.invoke({"input_text": message.text})['answer']
    ans.answer = answer
    print('Ответ получен')
    builder = InlineKeyboardBuilder()
    builder.button(text="Озвучить 🎤", callback_data = 'Озвучить')
    text_to_speech(answer)
    print('Аудио версия ответа ллм записана')
    await message.answer(answer, reply_markup=builder.as_markup())

  except Exception as e:
    print(f"Произошла ошибка: {e}")

@dp.callback_query(F.data == 'Озвучить')
async def send_voice(call: CallbackQuery):
  try:
    audio_file = FSInputFile('output.mp3')
    await call.message.answer_voice(voice=audio_file)
    os.remove('output.mp3')
  except Exception as e:
    await call.message.answer('Не удалось преобразовать в голосовое сообщение')
    print('Голосовое хуйня, не отправилось')


async def main():
  # dp.startup.register(start_bot)
  try:
    print("Бот запущен...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
  finally:
    await bot.session.close()
    print("Бот остановлен")

await main()