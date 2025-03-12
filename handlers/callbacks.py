from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import os
from aiogram import Router, F


from speech_functions import translate_text, text_to_speech

callbacks = Router()


@callbacks.callback_query(lambda callback: callback.data == "Перевести")
async def send_transl_text(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Подождите, я думаю...")
    await call.message.answer_photo(
        "https://i.pinimg.com/originals/d7/b4/5a/d7b45a0869e4c2300e81f633343f2c65.png"
    )
    data = await state.get_data()
    ans = data.get("answer_en")
    text = await translate_text(ans)
    print("Текст переведён ну или всё хуйня")
    await state.update_data(answer_ru=text)
    await state.update_data(lan="ru")
    builder = InlineKeyboardBuilder()
    builder.button(text="Озвучить 🎤", callback_data="Озвучить")
    try:
        await call.message.answer(text, reply_markup=builder.as_markup())
    except Exception as e:
        await call.message.answer("Прошу прощения, текст оказался слишком большой :)")
    


@callbacks.callback_query(lambda callback: callback.data == "Озвучить")
async def send_voice(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Подождите, я думаю...")
    await call.message.answer_photo(
        "https://i.pinimg.com/originals/d7/b4/5a/d7b45a0869e4c2300e81f633343f2c65.png"
    )
    data = await state.get_data()
    lan = data.get("lan")
    if lan == "ru":
        ans = data.get("answer_ru")
    else:
        ans = data.get("answer_en")
    text_to_speech(ans, lan)
    try:
        audio_file = FSInputFile("output.mp3")
        await call.message.answer_voice(voice=audio_file)
        os.remove("output.mp3")
    except Exception as e:
        await call.message.answer("Не удалось преобразовать в голосовое сообщение")
        print("Голосовое хуйня, не отправилось")


@callbacks.callback_query(lambda callback: callback.data == "Остановить ответы на вопросы")
async def stop_answering(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Нейросеть больше не отвечает на вопросы, выберите команду")
    await state.clear()

