from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states import Question, Registration
from initialisation import llm
from initialisation import bot
from agent_tools import agent
import keyboards as kb
from speech_functions import *


answer_question = Router()


@answer_question.message(Command("answer_question"), Registration.confirmed)
async def user_question(message: Message, state: FSMContext):
    text = 'Ready to answer your question! Choose the option:'
    text = await language_text(message.from_user.id, text)
    if await check_language_ru(message.from_user.id):
        await message.answer(text, reply_markup=kb.quest_ru)
    else:
        await message.answer(text, reply_markup=kb.quest_ru)


@answer_question.message(Question.text)
async def llm_answer(message: Message, state: FSMContext):
    try:
        print("УАУАУАУАУА")
        print("Промпт отправлен")
        ans = agent.run(message.text)
        print("Ответ получен")
        ans = await language_text(message.from_user.id, ans)
        if await check_language_ru(message.from_user.id):
            await state.update_data(answer_ru=ans)
            await state.update_data(lan="ru")
            await message.answer(ans, reply_markup=kb.say_ru)
            await state.set_state(Registration.confirmed)
        else:
            await state.update_data(answer_en=ans)
            await state.update_data(lan="en")
            await message.answer(ans, reply_markup=kb.say_en)
            await state.set_state(Registration.confirmed)
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await state.set_state(Registration.confirmed)
        return

@answer_question.message(Question.voice)
async def voice_handler(message: Message, state: FSMContext):
    voice = message.voice
    file = await bot.get_file(voice.file_id)
    file_path = file.file_path
    local_filename = f"voice_{message.from_user.id}.ogg"

    # Скачивание файла
    await bot.download_file(file_path, local_filename)

    try:
        # Распознавание речи
        if await check_language_ru(message.from_user.id):
            text = await recognize_speech(local_filename, 'ru')
        else:
            text = await recognize_speech(local_filename, 'en')

        # Отправка распознанного текста
        if text:
            try:
                print("УАУАУАУАУА")
                print("Промпт отправлен")
                ans = agent.run(message.text)
                print("Ответ получен")
                ans = await language_text(message.from_user.id, ans)
                if await check_language_ru(message.from_user.id):
                    await state.update_data(answer_ru=ans)
                    await state.update_data(lan="ru")
                    await message.answer(ans, reply_markup=kb.say_ru)
                    await state.set_state(Registration.confirmed)
                else:
                    await state.update_data(answer_en=ans)
                    await state.update_data(lan="en")
                    await message.answer(ans, reply_markup=kb.say_en)
                    await state.set_state(Registration.confirmed)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                await state.set_state(Registration.confirmed)
                return
        else:
            answ = 'Failed to recognize speech. Try again.'
            answ = await language_text(message.from_user.id, answ)
            await message.answer(f"❌ {answ}")
            await state.set_state(Registration.confirmed)
    except Exception as e:
        answ = 'Error processing of audio:'
        answ = await language_text(message.from_user.id, answ)
        await message.answer(f"⚠ {answ} {str(e)}")
        await state.set_state(Registration.confirmed)
    finally:
        # Удаление загруженного файла
        os.remove(local_filename)