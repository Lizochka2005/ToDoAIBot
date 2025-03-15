from aiogram import Router
from aiogram import types
import os
from aiogram import F

from initialisation import bot
from speech_functions import recognize_speech, language_text
from states import Registration

answer_voice_message = Router()


# Хэндлер для обработки голосовых сообщений
@answer_voice_message.message(F.voice, Registration.confirmed)
async def voice_handler(message: types.Message):
    voice = message.voice
    file = await bot.get_file(voice.file_id)
    file_path = file.file_path
    local_filename = f"voice_{message.from_user.id}.ogg"

    # Скачивание файла
    await bot.download_file(file_path, local_filename)

    try:
        # Распознавание речи
        text = recognize_speech(local_filename)

        # Отправка распознанного текста
        if text:
            answ = 'Recognized text:'
            answ = language_text(message.from_user.id, answ)
            await message.answer(f"🎤 {answ}\n\n{text}")
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