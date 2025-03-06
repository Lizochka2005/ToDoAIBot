# !pip install gTTS
# !pip install aiogram asyncio
# !pip install langchain
# !pip install langchain-groq
# !pip install googletrans

from gtts import gTTS
import os
from googletrans import Translator

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

def text_to_speech(text, lang):
  res = gTTS(text=text, lang=lang)
  filename = "output.mp3"
  res.save(filename)
  os.system(f"start {filename}")

async def translate_text(text):
  translator = Translator()
  try:
    out_text = await translator.translate(text, dest='ru')
    return out_text.text
  except Exception as e:
    print('Переводчик не робит :(')
    print(f"Произошла ошибка: {e}")

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
        template="{input_text}\n Please make answer shorter. Pease don't use ** in your answer."
    )
    solver_chain = LLMChain(llm=llm, prompt=prompt_template, output_key='answer')
    print('Промпт отправлен')
    ans = solver_chain.invoke({"input_text": message.text})['answer']
    await state.update_data(answer_en=ans)
    await state.update_data(lan='en')
    print('Ответ получен')
    builder = InlineKeyboardBuilder()
    builder.button(text="Озвучить 🎤", callback_data = 'Озвучить')
    builder.button(text="Перевести 🌐", callback_data = 'Перевести')
    await message.answer(ans, reply_markup=builder.as_markup())

  except Exception as e:
    print(f"Произошла ошибка: {e}")

@dp.callback_query(F.data == 'Перевести')
async def send_transl_text(call: CallbackQuery, state: FSMContext):
  await call.message.answer('Подождите, я думаю...')
  await call.message.answer_photo('https://i.pinimg.com/originals/d7/b4/5a/d7b45a0869e4c2300e81f633343f2c65.png')
  data = await state.get_data()
  ans = data.get('answer_en')
  text = await translate_text(ans)
  print('Текст переведён ну или всё хуйня')
  await state.update_data(answer_ru=text)
  await state.update_data(lan='ru')
  builder = InlineKeyboardBuilder()
  builder.button(text="Озвучить 🎤", callback_data = 'Озвучить')
  try:
    await call.message.answer(text, reply_markup=builder.as_markup())
  except Exception as e:
    await call.message.answer('Прошу прощения, текст оказался слишком большой :)')


@dp.callback_query(F.data == 'Озвучить')
async def send_voice(call: CallbackQuery, state: FSMContext):
  await call.message.answer('Подождите, я думаю...')
  await call.message.answer_photo('https://i.pinimg.com/originals/d7/b4/5a/d7b45a0869e4c2300e81f633343f2c65.png')
  data = await state.get_data()
  lan = data.get('lan')
  if lan == 'ru':
    ans = data.get('answer_ru')
  else:
    ans = data.get('answer_en')
  text_to_speech(ans, lan)
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