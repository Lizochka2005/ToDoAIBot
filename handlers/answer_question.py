from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import os

from states import Question
from initialisation import llm
from initialisation import bot
import keyboards as kb
from speech_functions import recognize_speech
from speech_functions import language_text, check_language_ru


answer_question = Router()


@answer_question.message(Command("answer_question"))
async def user_question(message: Message, state: FSMContext):
    text = "Ready to answer your question! Choose the option:"
    text = await language_text(message.from_user.id, text)
    if await check_language_ru(message.from_user.id):
        await message.answer(text, reply_markup=kb.quest_ru)
    else:
        await message.answer(text, reply_markup=kb.quest_en)


@answer_question.message(Question.text)
async def llm_answer(message: Message, state: FSMContext):
    try:
        print("УАУАУАУАУА")
        print("Промпт отправлен")
        if await check_language_ru(message.from_user.id):
            chosen_language = "Русский"
        else:
            chosen_language = "Английский"
        llm_promt = await language_text(
            message.from_user.id,
            str(message.text) + f" для ответа используй {chosen_language} язык"
        )
        ans = llm.invoke(llm_promt).content
        print("Ответ получен")
        if await check_language_ru(message.from_user.id):
            await state.update_data(answer_ru=ans)
            await state.update_data(lan="ru")
            await message.answer(ans, reply_markup=kb.say_ru)
        else:
            await state.update_data(answer_en=ans)
            await state.update_data(lan="en")
            await message.answer(ans, reply_markup=kb.say_en)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await state.clear()
        return


# Хэндлер для обработки голосовых сообщений
@answer_question.message(F.voice, Question.voice)
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
            text = await recognize_speech(local_filename, "ru")
        else:
            text = await recognize_speech(local_filename, "en")

       # message.answer(
       #     f"{await language_text(message.from_user.id, 'Распознан текст')}:\n{text}"
       # )
        # Отправка распознанного текста
        if text:
            try:
                print("УАУАУАУАУА")
                print("Промпт отправлен")
                if await check_language_ru(message.from_user.id):
                    chosen_language = "Русский"
                else:
                    chosen_language = "Английский"
                llm_promt = await language_text(
                    message.from_user.id,
                    str(text) + f" для ответа используй {chosen_language} язык"
                )
                ans = llm.invoke(llm_promt).content
                print("Ответ получен")
                if await check_language_ru(message.from_user.id):
                    await state.update_data(answer_ru=ans)
                    await state.update_data(lan="ru")
                    await message.answer(ans, reply_markup=kb.say_ru)
                else:
                    await state.update_data(answer_en=ans)
                    await state.update_data(lan="en")
                    await message.answer(ans, reply_markup=kb.say_en)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                return
        else:
            answ = "Failed to recognize speech. Try again."
            answ = await language_text(message.from_user.id, answ)
            await message.answer(f"❌ {answ}")
    except Exception as e:
        answ = "Error processing of audio:"
        answ = await language_text(message.from_user.id, answ)
        await message.answer(f"⚠ {answ} {str(e)}")
    finally:
        # Удаление загруженного файла
        os.remove(local_filename)
