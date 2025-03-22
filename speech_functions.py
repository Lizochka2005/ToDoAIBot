from gtts import gTTS
# import pyttsx3
import os
from translate import Translator
import whisper

import aiosqlite

from pydub import AudioSegment


async def text_to_speech(text: str, speed: float = 1.25, lang: str = "ru") -> str:
    """Озвучивает текст, возвращает путь к голосовому"""
    # Создаем временный файл MP3
    tts = gTTS(text=text, lang=lang, slow=False)
    mp3_path = "temp_voice.mp3"
    tts.save(mp3_path)

    # Конвертируем MP3 в OGG (формат, принимаемый Telegram)
    ogg_path = "temp_voice.ogg"
    audio = AudioSegment.from_mp3(mp3_path)
    audio = audio.speedup(playback_speed=speed)  # Ускоряем в 1.5 раза
    audio.export(ogg_path, format="ogg")

    # Удаляем временный MP3
    os.remove(mp3_path)
    return ogg_path

# def text_to_speech(text, lang):
#     engine = pyttsx3.init()

#     # Установка языка (если поддерживается)
#     voices = engine.getProperty('voices')
#     if lang == 'en':
#         engine.setProperty('voice', voices[1].id)  # Английский
#     elif lang == 'ru':
#         engine.setProperty('voice', voices[0].id)  # Русский 
#     else:
#         print(f"Язык {lang} не поддерживается. Используется язык по умолчанию.")
#     engine.save_to_file(text, 'output.mp3')
#     engine.runAndWait()


async def recognize_speech(audio_path, language="ru"):
    """С помощью whisper распознает текст в голосовом и возвращает его"""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=language)
    return result["text"].strip()


async def translate_text(text):
    """Переводит text с английского на русский"""
    # translator = Translator()
    translator = Translator(from_lang="en", to_lang="ru")
    try:
        # out_text = await translator.translate(text, dest="ru")
        # return out_text.text
        out_text = translator.translate(text)
        return str(out_text)
    except Exception as e:
        print("Переводчик не робит :(")
        print(f"Произошла ошибка: {e}")


async def translate_text_to_en(text):
    """Переводит text с русского на английский"""
    # translator = Translator()
    translator = Translator(from_lang="ru", to_lang="en")
    try:
        # out_text = await translator.translate(text)
        # return out_text.text
        out_text = translator.translate(text)
        return str(out_text)
    except Exception as e:
        print("Переводчик не робит :(")
        print(f"Произошла ошибка: {e}")


async def language_text(user_id, text):
    """Если выбран русский язык, переводит с английского на русский, иначе ничего просто возвращает тот же текст"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            language = await cursor.fetchone()
            if language[0] == "ru":
                return await translate_text(text)
            else:
                return text


async def check_language_ru(user_id):
    """Если выбран русский, возвращает True, иначе False"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            language = await cursor.fetchone()
            if language[0] == "ru":
                return True
            else:
                return False
