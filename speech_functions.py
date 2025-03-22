from gtts import gTTS
import pyttsx3
import os
# from googletrans import Translator
from translate import Translator
import asyncio
# import whisper
# import speech_recognition as sr
# from pydub import AudioSegment
import aiosqlite


# def text_to_speech(text, lang):
#     res = gTTS(text=text, lang=lang)
#     filename = "output.mp3"
#     res.save(filename)
#     os.system(f"start {filename}")

def text_to_speech(text, lang):
    engine = pyttsx3.init()

    # Установка языка (если поддерживается)
    voices = engine.getProperty('voices')
    if lang == 'en':
        engine.setProperty('voice', voices[1].id)  # Английский
    elif lang == 'ru':
        engine.setProperty('voice', voices[0].id)  # Русский (если доступен)
    else:
        print(f"Язык {lang} не поддерживается. Используется язык по умолчанию.")
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()


async def translate_text(text):
    # translator = Translator()
    translator = Translator(from_lang='en', to_lang='ru')
    try:
        # out_text = await translator.translate(text, dest="ru")
        # return out_text.text
        out_text = translator.translate(text)
        return str(out_text)
    except Exception as e:
        print("Переводчик не робит :(")
        print(f"Произошла ошибка: {e}")


async def translate_text_to_en(text):
    # translator = Translator()
    translator = Translator(from_lang='ru', to_lang='en')
    try:
        # out_text = await translator.translate(text)
        # return out_text.text
        out_text = translator.translate(text)
        return str(out_text)
    except Exception as e:
        print("Переводчик не робит :(")
        print(f"Произошла ошибка: {e}")

# async def recognize_speech(audio_path, language="ru"):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_path, language=language)
#     return result["text"].strip()

# async def recognize_speech(audio_path, language):
#     recognizer = sr.Recognizer()
    
#     # Загрузка аудиофайла с помощью pydub
#     audio = AudioSegment.from_file(audio_path)
#     audio.export("temp.wav", format="wav") 
    
#     try:
#          # Загрузка аудиофайла
#         with sr.AudioFile("temp.wav") as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data, language=language)  
#             return text.strip()
#     except sr.UnknownValueError:
#         return "Речь не распознана"
#     except sr.RequestError as e:
#         return f"Ошибка запроса к сервису распознавания речи: {e}"
#     except Exception as e:
#         return f"Произошла ошибка: {e}"

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
