from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import os
from aiogram import Router, F
from aiogram_dialog import DialogManager, StartMode
from handlers.start import *
from states import Registration, TaskUpdate, MySG, EditProfile, Question

from speech_functions import language_text, text_to_speech, translate_text_to_en
import keyboards as kb
import aiosqlite

callbacks = Router()


@callbacks.callback_query(lambda callback: callback.data == "lan ru")
async def lan_ru(call: CallbackQuery, state: FSMContext):
    await state.update_data(lan="ru")
    await state.set_state(Registration.waiting_for_language)
    await process_language(call.message, state)


@callbacks.callback_query(lambda callback: callback.data == "lan en")
async def lan_ru(call: CallbackQuery, state: FSMContext):
    await state.update_data(lan="en")
    await state.set_state(Registration.waiting_for_language)
    await process_language(call.message, state)


@callbacks.callback_query(lambda callback: callback.data == "Озвучить")
async def send_voice(call: CallbackQuery, state: FSMContext):
    if await check_language_ru(call.from_user.id):
        await call.message.answer("Подождите, я думаю...")
    else:
        await call.message.answer("Wait, I am thinking...")
    await call.message.answer_photo(
        "https://i.pinimg.com/originals/d7/b4/5a/d7b45a0869e4c2300e81f633343f2c65.png"
    )

    data = await state.get_data()
    lan = data.get("lan")
    if lan is None:
        # Обработка случая, когда ключ отсутствует
        print("Ключ 'lan' отсутствует в data")
        return
    if lan == "ru":
        ans = data.get("answer_ru")
    else:
        ans = data.get("answer_en")
    # text_to_speech(ans, lan)

    try:
        voice_path = await text_to_speech(call.message.text, 1.25, lan)
        # Отправляем голосовое сообщение
        voice = FSInputFile(voice_path)
        await call.message.answer_voice(voice=voice)

        # Удаляем временный OGG
        os.remove(voice_path)
    except Exception as e:
        text = "Unable to convert to voice message :("
        text = await language_text(call.from_user.id, text)
        await call.message.answer(text)
        await call.message.answer_photo(
            "https://sun9-53.userapi.com/impg/mHfnSoKv3i2bNVdL6ENDOLcYuED8sBP9GVXV4w/PWekFpK_g_A.jpg?size=736x736&quality=96&sign=2bddc00da433a4a004004deb8a148055&c_uniq_tag=VuDSAXPVfTsJ24WT7KHnkqGRaxYNBXVdiZJoowjfQhM&type=album"
        )
        print("Голосовое хуйня, не отправилось")


@callbacks.callback_query(lambda callback: callback.data == "время задача")
async def update_task_time(call: CallbackQuery, state: FSMContext):
    text = "Enter the time you want to change the task execution in format HH:MM :"
    text = await language_text(call.from_user.id, text)
    await call.message.answer(text)
    await state.set_state(TaskUpdate.waiting_for_new_time)


# @callbacks.callback_query(lambda callback: callback.data == "время дэдлайн")
# async def update_deadline_time(call: CallbackQuery, state: FSMContext):
#     text = 'Enter the time you want to change the deadline execution in format HH:MM :'
#     text = await language_text(call.from_user.id, text)
#     await call.message.answer(text)
#     await state.set_state(DeadlineUpdate.waiting_for_new_time)

# @callbacks.callback_query(lambda callback: callback.data == "дата дэдлайн")
# async def update_deadline_date(call: CallbackQuery, state: FSMContext, dialog_manager: DialogManager):
#     text = 'Choose the date you want to change the deadline execution:'
#     text = await language_text(call.from_user.id, text)
#     await call.message.answer(text)
#     await state.update_data(user_id=call.from_user.id)
#     await dialog_manager.start(MySG.main,
#                                data={"text_from_chat": text, "flag": "upd_dd",
#                                      "state": state},
#                                mode=StartMode.RESET_STACK)
#     await state.set_state(DeadlineUpdate.waiting_for_new_date)


@callbacks.callback_query(lambda callback: callback.data == "дата задача")
async def update_task_date(
    call: CallbackQuery, state: FSMContext, dialog_manager: DialogManager
):
    text = "Choose the date you want to change the task execution:"
    text = await language_text(call.from_user.id, text)
    await call.message.answer(text)
    await state.update_data(user_id=call.from_user.id)
    await dialog_manager.start(
        MySG.main,
        data={"text_from_chat": text, "flag": "upd_tsk", "state": state},
        mode=StartMode.RESET_STACK,
    )
    await state.set_state(TaskUpdate.waiting_for_new_date)


# @callbacks.callback_query(lambda callback: callback.data == "статус дэдлайн")
# async def update_deadline_date(call: CallbackQuery, state: FSMContext):
#     text = 'Enter new status for the deadline:'
#     text = await language_text(call.from_user.id, text)
#     user_data = await state.get_data()
#     id = user_data['deadline_id']
#     if await check_language_ru(call.from_user.id):
#         await call.message.answer(text, reply_markup=kb.create_deadline_status_ru(id))
#     else:
#         await call.message.answer(text, reply_markup=kb.create_deadline_status_en(id))


@callbacks.callback_query(lambda callback: callback.data == "статус задача")
async def update_task_date(call: CallbackQuery, state: FSMContext):
    text = "Enter new status for the task:"
    text = await language_text(call.from_user.id, text)
    user_data = await state.get_data()
    id = user_data["task_id"]
    if await check_language_ru(call.from_user.id):
        await call.message.answer(text, reply_markup=kb.create_task_status_ru(id))
    else:
        await call.message.answer(text, reply_markup=kb.create_task_status_en(id))


@callbacks.callback_query(F.data.startswith("completed task_"))
async def update_task_status_completed(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    id = int(call.data.split("_")[-1])
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET status = 'Выполнено' WHERE id=?",
            (id,),
        )
        await db.commit()

    await call.message.answer_photo(
        "https://sun9-5.userapi.com/impf/c841333/v841333163/39bb7/JP8QeOP6rII.jpg?size=1200x630&quality=96&sign=c35431318cdb25da8a14a74f1bd02fcd&c_uniq_tag=1GSxfeUXOaFJuOidE7sYqjGg1jrexqegniQbwMczCVc&type=album"
    )

    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)
        ) as cursor:
            tasks = await cursor.fetchall()

            response = "Your task:"
            response = await language_text(user_id, response)
            response += "\n"
            for task_id, task, date, time, status in tasks:
                if await check_language_ru(user_id):
                    response += f"{task_id}. {task} (Дата: {date}, Время: {time}, Статус: {status})\n"
                else:
                    status = await translate_text_to_en(status)
                    response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

            await call.message.answer(response)
            await state.clear()


@callbacks.callback_query(F.data.startswith("partially completed task_"))
async def update_task_status_part_completed(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    id = int(call.data.split("_")[-1])
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET status = 'Частично выполнено' WHERE id=?",
            (id,),
        )
        await db.commit()

    await call.message.answer_photo(
        "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_6750b29200cd8b773bae1bfe_6750b3838d61f41716a88c22/scale_1200"
    )

    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)
        ) as cursor:
            tasks = await cursor.fetchall()

            response = "Your task:"
            response = await language_text(user_id, response)
            response += "\n"
            for task_id, task, date, time, status in tasks:
                if await check_language_ru(user_id):
                    response += f"{task_id}. {task} (Дата: {date}, Время: {time}, Статус: {status})\n"
                else:
                    status = await translate_text_to_en(status)
                    response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

            await call.message.answer(response)
            await state.clear()


@callbacks.callback_query(F.data.startswith("not completed task_"))
async def update_task_status_not_completed(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    id = int(call.data.split("_")[-1])
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "UPDATE tasks SET status = 'Не выполнено' WHERE id=?",
            (id,),
        )
        await db.commit()

    await call.message.answer_photo(
        "https://www.meme-arsenal.com/memes/d1072c2b2e028f0d5e6dcaf75bf62ef9.jpg"
    )

    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT id, task, date, time, status FROM tasks WHERE id = ?", (id,)
        ) as cursor:
            tasks = await cursor.fetchall()

            response = "Your task:"
            response = await language_text(user_id, response)
            response += "\n"
            for task_id, task, date, time, status in tasks:
                if await check_language_ru(user_id):
                    response += f"{task_id}. {task} (Дата: {date}, Время: {time}, Статус: {status})\n"
                else:
                    status = await translate_text_to_en(status)
                    response += f"{task_id}. {task} (Date: {date}, Time: {time}, Status: {status})\n"

            await call.message.answer(response)
            await state.clear()


# @callbacks.callback_query(F.data.startswith("not completed deadline_"))
# async def update_task_status_not_completed(call: CallbackQuery, state: FSMContext):
#     user_id = call.from_user.id
#     id = int(call.data.split("_")[-1])
#     async with aiosqlite.connect("users.db") as db:
#         await db.execute(
#             "UPDATE deadlines SET status = 'Не завершён' WHERE id=?", ( id,),
#         )
#         await db.commit()

#     await call.message.answer_photo('https://avatars.dzeninfra.ru/get-zen_doc/1616946/pub_5cb6b80ba4186400b437bd1f_5cb6b81c98204d00b3fdb1dc/scale_1200')

#     async with aiosqlite.connect('users.db') as db:
#       async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE id = ?", (id,)) as cursor:
#         deadlines = await cursor.fetchall()

#         response = "Your deadline:"
#         response = await language_text(user_id, response)
#         response += '\n'
#         for deadline_id, deadline, date, time, status in deadlines:
#             if await check_language_ru(user_id):
#                 response += f"{deadline_id}. {deadline} (Дата: {date}, Время: {time}, Статус: {status})\n"
#             else:
#                 status = await translate_text_to_en(status)
#                 response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

#         await call.message.answer(response)
#         await state.clear()


# @callbacks.callback_query(F.data.startswith("completed deadline_"))
# async def update_task_status_not_completed(call: CallbackQuery, state: FSMContext):
#     user_id = call.from_user.id
#     id = int(call.data.split("_")[-1])
#     async with aiosqlite.connect("users.db") as db:
#         await db.execute(
#             "UPDATE deadlines SET status = 'Завершён' WHERE id=?", ( id,),
#         )
#         await db.commit()

#     await call.message.answer_photo('https://sun9-5.userapi.com/impf/c841333/v841333163/39bb7/JP8QeOP6rII.jpg?size=1200x630&quality=96&sign=c35431318cdb25da8a14a74f1bd02fcd&c_uniq_tag=1GSxfeUXOaFJuOidE7sYqjGg1jrexqegniQbwMczCVc&type=album')

#     async with aiosqlite.connect('users.db') as db:
#       async with db.execute("SELECT id, deadline, date, time, status FROM deadlines WHERE id = ?", (id,)) as cursor:
#         deadlines = await cursor.fetchall()

#         response = "Your deadline:"
#         response = await language_text(user_id, response)
#         response += '\n'
#         for deadline_id, deadline, date, time, status in deadlines:
#             if await check_language_ru(user_id):
#                 response += f"{deadline_id}. {deadline} (Дата: {date}, Время: {time}, Статус: {status})\n"
#             else:
#                 status = await translate_text_to_en(status)
#                 response += f"{deadline_id}. {deadline} (Date: {date}, Time: {time}, Status: {status})\n"

#         await call.message.answer(response)
#         await state.clear()


@callbacks.callback_query(
    EditProfile.waiting_for_choice, F.data.in_(["edit_name", "edit_language"])
)
async def process_edit_choice(call: CallbackQuery, state: FSMContext):
    choice = call.data
    if choice == "edit_name":
        text = "Enter new name:"
        text = await language_text(call.from_user.id, text)
        await call.message.answer(text)
        await state.set_state(EditProfile.waiting_for_name)
    elif choice == "edit_language":
        user_id = call.from_user.id
        async with aiosqlite.connect("users.db") as db:
            async with db.execute(
                "SELECT language FROM users WHERE user_id=?", (user_id,)
            ) as cursor:
                user_data = await cursor.fetchone()
                if user_data:
                    current_language = user_data[0]
                    new_language = "ru" if current_language == "en" else "en"
                    await db.execute(
                        "UPDATE users SET language=? WHERE user_id=?",
                        (new_language, user_id),
                    )
                    await db.commit()
                    text = "Language successfully changed to"
                    text = await language_text(user_id, text)
                    await call.message.answer(text + " " + new_language + ".")
                else:
                    text = "Profile is not found."
                    text = await language_text(user_id, text)
                    await call.message.answer(text)
    await call.answer()


@callbacks.callback_query(lambda callback: callback.data == "voice enter")
async def voice_input(call: CallbackQuery, state: FSMContext):
    text = "Waiting for voice message 🎧."
    text = await language_text(call.from_user.id, text)
    await call.message.answer(text)
    await state.set_state(Question.voice)


@callbacks.callback_query(lambda callback: callback.data == "text enter")
async def text_input(call: CallbackQuery, state: FSMContext):
    text = "Waiting for text message 📄."
    text = await language_text(call.from_user.id, text)
    await call.message.answer(text)
    await state.set_state(Question.text)
