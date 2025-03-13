from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import os
from aiogram import Router, F


from speech_functions import translate_text, language_text, text_to_speech

callbacks = Router()


# @callbacks.callback_query(lambda callback: callback.data == "Перевести")
# async def send_transl_text(call: CallbackQuery, state: FSMContext):
#     await call.message.answer("Подождите, я думаю...")
#     await call.message.answer_photo(
#         "https://i.pinimg.com/originals/d7/b4/5a/d7b45a0869e4c2300e81f633343f2c65.png"
#     )
#     data = await state.get_data()
#     ans = data.get("answer_en")
#     text = await translate_text(ans)
#     print("Текст переведён ну или всё хуйня")
#     await state.update_data(answer_ru=text)
#     await state.update_data(lan="ru")
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Озвучить 🎤", callback_data="Озвучить")
#     try:
#         await call.message.answer(text, reply_markup=builder.as_markup())
#     except Exception as e:
#         await call.message.answer("Прошу прощения, текст оказался слишком большой :)")
    


@callbacks.callback_query(lambda callback: callback.data == "Озвучить")
async def send_voice(call: CallbackQuery, state: FSMContext):
    text = 'Wait, I am thinking...'
    text = await language_text(call.message.from_user.id, text)
    await call.message.answer(text)
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
        text = 'Unable to convert to voice message :('
        text = await language_text(call.message.from_user.id, text)
        await call.message.answer(text)
        await call.message.answer_photo(
            'https://sun9-53.userapi.com/impg/mHfnSoKv3i2bNVdL6ENDOLcYuED8sBP9GVXV4w/PWekFpK_g_A.jpg?size=736x736&quality=96&sign=2bddc00da433a4a004004deb8a148055&c_uniq_tag=VuDSAXPVfTsJ24WT7KHnkqGRaxYNBXVdiZJoowjfQhM&type=album'
        )
        print("Голосовое хуйня, не отправилось")


@callbacks.callback_query(lambda callback: callback.data == "Остановить ответы на вопросы")
async def stop_answering(call: CallbackQuery, state: FSMContext):
    text = 'Neuro-network no longer answers questions. Choose the option.'
    text = await language_text(call.message.from_user.id, text)
    await call.message.answer(text)
    await state.clear()

