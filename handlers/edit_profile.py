from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import EditProfile
from speech_functions import language_text, check_language_ru
import aiosqlite
import keyboards as kb

edit_profile = Router()

@edit_profile.message(Command("edit_profile"))
async def edit_profile_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT name, language FROM users WHERE user_id=?", (user_id,)) as cursor:
            user_data = await cursor.fetchone()

            if not user_data:
                text = 'Profile is not found.'
                text = await language_text(user_id, text)
                await message.answer(text)
                return

            name, language = user_data
            text = []
            res = []
            text.append('Your current profile:')
            text.append('Name:')
            text.append('Language:')
            text.append('What do you want to change?')
            for el in text:
                res.append(await language_text(user_id, el))
            response = res[0]+'\n'+res[1]+' '+name+'\n'+res[2]+' '+language+'\n\n'+res[3]
            if await check_language_ru(user_id):
                await message.answer(response, reply_markup=kb.edit_profile_ru)
            else:
                await message.answer(response, reply_markup=kb.edit_profile_en)
            await state.set_state(EditProfile.waiting_for_choice)   

@edit_profile.message(EditProfile.waiting_for_name)
async def process_new_name(message: Message, state: FSMContext):
    new_name = message.text
    user_id = message.from_user.id
    safe_name = new_name.replace("<", "&lt;").replace(">", "&gt;")
    async with aiosqlite.connect('users.db') as db:
        await db.execute("UPDATE users SET name=? WHERE user_id=?", (safe_name, user_id))  # Не забудьте await!
        await db.commit()
    text = 'Name successfully changed to'
    text = await language_text(user_id, text)
    await message.answer(text + ' ' + safe_name +'.')
    await state.clear()
