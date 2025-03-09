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
import datetime

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(model="llama3-70b-8192")

token_bot = '7685591016:AAG8M4rZPovKNrOuKqq6sMwT8stOg1vk2rc'

bot = Bot(token=token_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

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

async def main():
  # dp.startup.register(start_bot)
  dp.startup.register(start_db)
  try:
    print("Бот запущен...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
  finally:
    await bot.session.close()
    print("Бот остановлен")

await main()