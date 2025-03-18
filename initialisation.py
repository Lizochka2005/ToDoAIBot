from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from langchain_groq import ChatGroq
# from langchain_gigachat import GigaChat
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(model="llama3-70b-8192")

# token = 'YjVjZWU4OWItZTJkMC00N2ZkLWJiODMtZDViOGRlMDQyNWM5OmFlMTBlNzEyLTI3MDItNDdlMC05NWM2LTI1NTAyM2NiM2NmZg=='

# llm = GigaChat(credentials=token, model='GigaChat:latest', verify_ssl_certs=False)

TOKEN_BOT = "7401240457:AAGiBui89YjbXBc1J9MVSAYdPJChYp5GEV8"

bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())