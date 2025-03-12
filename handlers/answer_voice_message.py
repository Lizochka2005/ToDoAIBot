from aiogram import Router
from aiogram import types
import os
from aiogram import F

from initialisation import bot
from speech_functions import recognize_speech

answer_voice_message = Router()


# Хэндлер для обработки голосовых сообщений
@answer_voice_message.message(F.voice)
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
            await message.answer(f"🎤 Распознанный текст:\n\n{text}")
        else:
            await message.answer("❌ Не удалось распознать речь. Попробуйте еще раз.")
    except Exception as e:
        await message.answer(f"⚠ Ошибка обработки аудио: {str(e)}")
    finally:
        # Удаление загруженного файла
        os.remove(local_filename)