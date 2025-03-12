from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(model="llama3-70b-8192")

TOKEN_BOT = "7685591016:AAG8M4rZPovKNrOuKqq6sMwT8stOg1vk2rc"

bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())