from aiogram import Router
from aiogram import types
import os
from aiogram import F
from aiogram.fsm.context import FSMContext
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from initialisation import bot
from initialisation import llm
from speech_functions import recognize_speech, language_text, check_language_ru
from states import Question, Registration
import keyboards as kb

answer_voice_message = Router()


# Хэндлер для обработки голосовых сообщений
@answer_voice_message.message(F.voice, Question.voice)
async def voice_handler(message: types.Message, state: FSMContext):
    voice = message.voice
    file = await bot.get_file(voice.file_id)
    file_path = file.file_path
    local_filename = f"voice_{message.from_user.id}.ogg"

    # Скачивание файла
    await bot.download_file(file_path, local_filename)

    try:
        # Распознавание речи
        if await check_language_ru(message.from_user.id):
            text = recognize_speech(local_filename, 'ru')
        else:
            text = recognize_speech(local_filename, 'en')

        # Отправка распознанного текста
        if text:
            try:
                print("УАУАУАУАУА")
                prompt_template = PromptTemplate(
                    input_variables=["input_text"],
                    template="{input_text}\n Please make answer shorter. Pease don't use ** in your answer.",
                )
                solver_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="answer")
                print("Промпт отправлен")
                ans = solver_chain.invoke({"input_text": message.text})["answer"]
                await state.update_data(answer_en=ans)
                await state.update_data(lan="en")
                print("Ответ получен")
                ans = await language_text(message.from_user.id, ans)
                if await check_language_ru(message.from_user.id):
                    await message.answer(ans, reply_markup=kb.say_ru)
                    await state.set_state(Registration.confirmed)
                else:
                    await message.answer(ans, reply_markup=kb.say_en)
                    await state.set_state(Registration.confirmed)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                await state.set_state(Registration.confirmed)
                return
        else:
            answ = 'Failed to recognize speech. Try again.'
            answ = language_text(message.from_user.id, answ)
            await message.answer(f"❌ {answ}")
    except Exception as e:
        answ = 'Error processing of audio:'
        answ = language_text(message.from_user.id, answ)
        await message.answer(f"⚠ {answ} {str(e)}")
    finally:
        # Удаление загруженного файла
        os.remove(local_filename)