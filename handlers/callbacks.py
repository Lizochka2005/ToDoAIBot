from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import os
from aiogram import Router, F
from states import *

from speech_functions import *
import keyboards as kb
import aiosqlite

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
async def stop_answering(call: CallbackQuery):
    text = 'Neuro-network no longer answers questions. Choose the option.'
    text = await language_text(call.message.from_user.id, text)
    await call.message.answer(text)

@callbacks.callback_query(lambda callback: callback.data == "время задача")
async def update_task_time(call: CallbackQuery, state: FSMContext):
    text = 'Enter the time you want to change the task execution in format HH:MM :'
    text = await language_text(call.message.from_user.id, text)
    await call.message.answer(text)
    await state.set_state(TaskUpdate.waiting_for_new_time)

@callbacks.callback_query(lambda callback: callback.data == "время дэдлайн")
async def update_deadline_time(call: CallbackQuery, state: FSMContext):
    text = 'Enter the time you want to change the deadline execution in format HH:MM :'
    text = await language_text(call.message.from_user.id, text)
    await call.message.answer(text)
    await state.set_state(DeadlineUpdate.waiting_for_new_time)

@callbacks.callback_query(lambda callback: callback.data == "дата дэдлайн")
async def update_deadline_date(call: CallbackQuery, state: FSMContext):
    text = 'Enter the date you want to change the deadline execution in format YYYY-MM-DD:'
    text = await language_text(call.message.from_user.id, text)
    await call.message.answer(text)
    await state.set_state(DeadlineUpdate.waiting_for_new_date)

@callbacks.callback_query(lambda callback: callback.data == "дата задача")
async def update_task_date(call: CallbackQuery, state: FSMContext):
    text = 'Enter the date you want to change the task execution in format YYYY-MM-DD:'
    text = await language_text(call.message.from_user.id, text)
    await call.message.answer(text)
    await state.set_state(TaskUpdate.waiting_for_new_date)

@callbacks.callback_query(lambda callback: callback.data == "статус дэдлайн")
async def update_deadline_date(call: CallbackQuery):
    text = 'Enter new status for the deadline:'
    text = await language_text(call.message.from_user.id, text)
    if check_language_ru(Message.from_user.id):
        await call.message.answer(text, reply_markup=kb.update_status_deadline_ru)
    else:
        await call.message.answer(text, reply_markup=kb.update_status_deadline_en)

@callbacks.callback_query(lambda callback: callback.data == "статус задача")
async def update_task_date(call: CallbackQuery):
    text = 'Enter new status for the task:'
    text = await language_text(call.message.from_user.id, text)
    if check_language_ru(Message.from_user.id):
        await call.message.answer(text, reply_markup=kb.update_status_task_ru)
    else:
        await call.message.answer(text, reply_markup=kb.update_status_task_en)

@callbacks.callback_query(lambda callback: callback.data == "completed task")
async def update_task_status_completed(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = call.message.from_user.id
    id = user_data["task_id"]
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET status = 'Выполнено' WHERE id=?", ( id,),
        )
        await db.commit()
    
    await call.message.answer_photo('https://sun9-5.userapi.com/impf/c841333/v841333163/39bb7/JP8QeOP6rII.jpg?size=1200x630&quality=96&sign=c35431318cdb25da8a14a74f1bd02fcd&c_uniq_tag=1GSxfeUXOaFJuOidE7sYqjGg1jrexqegniQbwMczCVc&type=album')

    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)) as cursor:
        tasks = await cursor.fetchall()

        response = "Your task:\n"
        for task_id, task, date, time, status in tasks:
            status = await translate_text_to_en(user_id, status)
            response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        response = await language_text(user_id, response)
        await call.message.answer(response)
        await state.set_state(Registration.confirmed)

@callbacks.callback_query(lambda callback: callback.data == "partially completed task")
async def update_task_status_part_completed(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = call.message.from_user.id
    id = user_data["task_id"]
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET status = 'Частично выполнено' WHERE id=?", ( id,),
        )
        await db.commit()

    await call.message.answer_photo('https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_6750b29200cd8b773bae1bfe_6750b3838d61f41716a88c22/scale_1200')
    
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)) as cursor:
        tasks = await cursor.fetchall()

        response = "Your task:\n"
        for task_id, task, date, time, status in tasks:
            status = await translate_text_to_en(user_id, status)
            response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        response = await language_text(user_id, response)
        await call.message.answer(response)
        await state.set_state(Registration.confirmed)

@callbacks.callback_query(lambda callback: callback.data == "not completed task")
async def update_task_status_not_completed(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = call.message.from_user.id
    id = user_data["task_id"]
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET status = 'Не выполнено' WHERE id=?", ( id,),
        )
        await db.commit()

    await call.message.answer_photo('https://www.meme-arsenal.com/memes/d1072c2b2e028f0d5e6dcaf75bf62ef9.jpg')
    
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)) as cursor:
        tasks = await cursor.fetchall()

        response = "Your task:\n"
        for task_id, task, date, time, status in tasks:
            status = await translate_text_to_en(user_id, status)
            response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

        response = await language_text(user_id, response)
        await call.message.answer(response)
        await state.set_state(Registration.confirmed)


@callbacks.callback_query(lambda callback: callback.data == "not completed deadline")
async def update_task_status_not_completed(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = call.message.from_user.id
    id = user_data["deadline_id"]
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE deadlines SET status = 'Не завершён' WHERE id=?", ( id,),
        )
        await db.commit()
    
    await call.message.answer_photo('https://avatars.dzeninfra.ru/get-zen_doc/1616946/pub_5cb6b80ba4186400b437bd1f_5cb6b81c98204d00b3fdb1dc/scale_1200')

    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE id = ?", (id,)) as cursor:
        deadlines = await cursor.fetchall()

        response = "Your deadline:\n"
        for deadline_id, deadline, date, time, status in deadlines:
            status = await translate_text_to_en(user_id, status)
            response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

        response = await language_text(user_id, response)
        await call.message.answer(response)
        await state.set_state(Registration.confirmed)

@callbacks.callback_query(lambda callback: callback.data == "completed deadline")
async def update_task_status_not_completed(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = call.message.from_user.id
    id = user_data["deadline_id"]
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE deadlines SET status = 'Завершён' WHERE id=?", ( id,),
        )
        await db.commit()
    
    await call.message.answer_photo('https://sun9-5.userapi.com/impf/c841333/v841333163/39bb7/JP8QeOP6rII.jpg?size=1200x630&quality=96&sign=c35431318cdb25da8a14a74f1bd02fcd&c_uniq_tag=1GSxfeUXOaFJuOidE7sYqjGg1jrexqegniQbwMczCVc&type=album')
    
    async with aiosqlite.connect('users.db') as db:
      async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE id = ?", (id,)) as cursor:
        deadlines = await cursor.fetchall()

        response = "Your deadline:\n"
        for deadline_id, deadline, date, time, status in deadlines:
            status = await translate_text_to_en(user_id, status)
            response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

        response = await language_text(user_id, response)
        await call.message.answer(response)
        await state.set_state(Registration.confirmed)