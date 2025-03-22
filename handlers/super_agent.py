from aiogram import Bot, Router, F
from aiogram.types import Message, Voice
import aiosqlite
from aiogram.fsm.state import State, StatesGroup
import re
import json
from typing import Dict, Any
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from aiogram.fsm.context import FSMContext

from speech_functions import recognize_speech, check_language_ru
from initialisation import llm
from initialisation import llm
import keyboards as kb
from speech_functions import recognize_speech, language_text, check_language_ru


super_agent = Router()


def raw_str_to_dict(s):
    # Удаляем все лишние запятые перед закрывающими скобками
    fixed = re.sub(r",\s*(?=}|])", "", s)
    return json.loads(fixed)


@super_agent.message(F.voice | F.text, State(None))
async def handle_voice(message: Message, bot: Bot):
    if message.text:
        text = message.text
    else:
        voice = message.voice
        file = await bot.get_file(voice.file_id)
        file_path = file.file_path
        local_filename = f"voice_{message.from_user.id}.ogg"

        # Скачивание файла
        await bot.download_file(file_path, local_filename)
        # Распознавание речи
        if await check_language_ru(message.from_user.id):
            text = await recognize_speech(local_filename, "ru")
        else:
            text = await recognize_speech(local_filename, "en")

    # Системный промпт для LLM
    SYSTEM_PROMPT = (
        "Запрос пользователя: "
        + text
        + "\n"
        + """
    Анализируй запрос пользователя и возвращай JSON:
    {
        "intent": "Создать задачу|Обновить задачу|Задать вопрос нейросети|Уведомления|Сменить язык|Сменить имя",
        # Если в где-то в params пользователь не сообщил точное значение, ставь None
        "params": {
            "date": "YYYY-MM-DD", #если пользователь не указал дату, установи сегодняшнюю
            "time": "HH:MM",
            "task": "Название задачи",
            "status": "Выполнено|Не выполнено",
            "query": "Вопрос к нейросети",
            "notifications": "True, если пользователь хочет включить уведомления и False, если хочет выключить",
            "username": "Имя пользовател, на которое он хочет изменить",
            "language": "ru|en",
        }
    }
    Давай подумаем шаг за шагом.
    Верни только json и ничего больше. Без апострофов на концах и слова json. 
    Будь внимателен - четко соблюдай возможные варианты параметров.
    Не забывай закрывать скобки и ставить запятые.
    Пример вопроса:
    Напомни купить молоко в 18:00
    Пример ответа:
    {
        "intent": "Создать задачу",
        "params": {
            "date": "2025-03-22", #если пользователь не указал дату, установи сегодняшнюю
            "time": "18:00",
            "task": "Купить молоко",
            "status": "Не выполнено",
            "query": "None",
            "notifications": "None",
            "username": "None",
            "language": "None",
        }
    }
    """
    )

    # Анализ текста LLM
    intent_data = llm.invoke(SYSTEM_PROMPT).content
    print(intent_data)
    intent_data = raw_str_to_dict(intent_data)
    print(intent_data)

    # Роутинг к агенту
    agent = get_agent(intent_data["intent"])
    await agent.execute(intent_data["params"], message.from_user.id, message, bot)


class AddTask:
    async def execute(self, params, user_id, message: Message, bot: Bot):
        # Логика создания задачи
        print("Отработал AddTask")
        try:
            async with aiosqlite.connect("users.db") as db:
                await db.execute(
                    "INSERT INTO tasks(user_id, task, date, time) VALUES (?, ?, ?, ?)",
                    (user_id, params["task"], params["date"], params["time"]),
                )
                await db.commit()
        except Exception as e:
            print(f"Ошибка добавления задачи агентом:\n{str(e)}")
            return None
        await message.answer(
            f"Задача создана: {params['task']} {params['date']} в {params['time']}"
        )


class UpdateTask:
    async def execute(self, params, user_id, message: Message, bot: Bot):
        # Логика обновления задачи
        print("Отработал UpdateTask")
        task_id = params.get("task_id")
        try:
            async with aiosqlite.connect("users.db") as db:
                await db.execute(
                    "UPDATE tasks SET time = ? WHERE id=?",
                    (
                        params["time"],
                        task_id,
                    ),
                )
                await db.execute(
                    "UPDATE tasks SET date = ? WHERE id=?",
                    (
                        params["date"],
                        task_id,
                    ),
                )
                await db.commit()

            # async with aiosqlite.connect("users.db") as db:
            #     await db.commit()

        except Exception as e:
            print(f"Ошибка обновления задачи агентом:\n{str(e)}")
            return None
        await message.answer(
            f"Задача обновлена: {params['task']} {params['date']} в {params['time']}, статус: {params['status']}"
        )


class AskLlm:
    async def execute(self, params, user_id, message: Message, bot: Bot):
        print("Отработал AskLlm")
        # try:
        #     llm_answer = llm.invoke(params["query"].content)
        # except Exception as e:
        #     print(f"Ошибка запроса к нейросети агентом:\n{str(e)}")
        #     return None

        try:
            print("УАУАУАУАУА")
            print("Промпт отправлен")
            # ans = agent.run(message.text)
            if await check_language_ru(message.from_user.id):
                chosen_language = "Русский"
            else:
                chosen_language = "Английский"
            llm_promt = await language_text(
                message.from_user.id,
                message.text + f" для ответа используй {chosen_language} язык",
            )
            ans = llm.invoke(llm_promt).content
            print("Ответ получен")
            if await check_language_ru(message.from_user.id):
                # await state.update_data(answer_ru=ans)
                # await state.update_data(lan="ru")
                await message.answer(ans, reply_markup=kb.say_ru)
                # await state.clear()
            else:
                # await state.update_data(answer_en=ans)
                # await state.update_data(lan="en")
                await message.answer(ans, reply_markup=kb.say_en)
                # await state.clear()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            # await state.clear()
            return

        # return llm_answer


class Notifications:
    async def execute(self, params, user_id, message: Message, bot: Bot):
        print("Отработал Notifications")
        try:
            if params["notifications"] == str(True):
                async with aiosqlite.connect("users.db") as db:
                    await db.execute(
                        "UPDATE users SET subscribed = TRUE WHERE user_id = ?",
                        (user_id,),
                    )
                    await db.commit()
                await message.answer("Уведомления включены")
                print("Уведомления включены")
            elif params["notifications"] == str(False):
                async with aiosqlite.connect("users.db") as db:
                    await db.execute(
                        "UPDATE users SET subscribed = FALSE WHERE user_id = ?",
                        (user_id,),
                    )
                    await db.commit()
                await message.answer("Уведомления выключены")
                print("Уведомления выкключены")
        except Exception as e:
            print(f"Ошибка включения/выключения уведомлений агентом:\n{str(e)}")
            return None


class EditLanguage:
    async def execute(self, params, user_id, message: Message, bot: Bot):
        print("Отработал EditLanguage")
        if params["language"] is not None:
            user_id = message.from_user.id
            async with aiosqlite.connect("users.db") as db:
                async with db.execute(
                    "SELECT language FROM users WHERE user_id=?", (user_id,)
                ) as cursor:
                    user_data = await cursor.fetchone()
                    if user_data:
                        current_language = user_data[0]
                        new_language = "ru" if current_language == "en" else "en"
                        await db.execute(
                            "UPDATE users SET language=? WHERE user_id=?",
                            (new_language, user_id),
                        )
                        await db.commit()
                        text = "Language successfully changed to"
                        text = await language_text(user_id, text)
                        await message.answer(text + " " + new_language + ".")
                    else:
                        text = "Profile is not found."
                        text = await language_text(user_id, text)
                        await message.answer(text)


class EditName:
    async def execute(self, params, user_id, message: Message, bot: Bot):
        print("Отработал EditName")
        if params["username"] is not None:
            new_name = params["username"]
            user_id = message.from_user.id
            safe_name = new_name.replace("<", "&lt;").replace(">", "&gt;")
            async with aiosqlite.connect("users.db") as db:
                await db.execute(
                    "UPDATE users SET name=? WHERE user_id=?", (safe_name, user_id)
                )  # Не забудьте await!
                await db.commit()
            text = "Name successfully changed to"
            text = await language_text(user_id, text)
            await message.answer(text + " " + safe_name + ".")


def get_agent(intent):
    agents = {
        "Создать задачу": AddTask(),
        "Обновить задачу": UpdateTask(),
        "Задать вопрос нейросети": AskLlm(),
        "Уведомления": Notifications(),
        "Сменить язык": EditLanguage(),
        "Сменить имя": EditName(),
    }
    return agents.get(intent, DefaultAgent())


class DefaultAgent:
    async def execute(self, params=None):
        return "Я не совсем понял ваш запрос.\n" "Попробуйте сказать иначе"
