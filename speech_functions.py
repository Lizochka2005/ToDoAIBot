from gtts import gTTS
import os
from googletrans import Translator
import asyncio
import whisper
import aiosqlite


def text_to_speech(text, lang):
    res = gTTS(text=text, lang=lang)
    filename = "output.mp3"
    res.save(filename)
    os.system(f"start {filename}")


async def translate_text(text):
    translator = Translator()
    try:
        out_text = await translator.translate(text, dest="ru")
        return out_text.text
    except Exception as e:
        print("Переводчик не робит :(")
        print(f"Произошла ошибка: {e}")


async def translate_text_to_en(text):
    translator = Translator()
    try:
        out_text = await translator.translate(text)
        return out_text.text
    except Exception as e:
        print("Переводчик не робит :(")
        print(f"Произошла ошибка: {e}")

async def recognize_speech(audio_path, language="ru"):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=language)
    return result["text"].strip()

async def language_text(user_id, text):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)) as cursor:
            language = await cursor.fetchone()
            if language[0] == 'ru':
                return await translate_text(text)
            else:
                return text

async def check_language_ru(user_id):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)) as cursor:
            language = await cursor.fetchone()
            if language[0] == 'ru':
                return True
            else:
                return False
