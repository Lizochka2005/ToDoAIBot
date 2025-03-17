from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from aiogram.filters import Command

from states import Question, Registration
from initialisation import llm
import keyboards as kb
from speech_functions import *


answer_question = Router()


@answer_question.message(Command("answer_question"), Registration.confirmed)
async def user_question(message: Message, state: FSMContext):
    text = 'Ready to answer your question!'
    text = await language_text(message.from_user.id, text)
    await message.answer(text)
    await state.set_state(Question.question)


@answer_question.message(F.text, Question.question)
async def llm_answer(message: Message, state: FSMContext):
    try:
        print("УАУАУАУАУА")
        prompt_template = PromptTemplate(
            input_variables=["input_text"],
            template="{input_text}\n Please make answer shorter. Pease don't use ** in your answer.",
        )
        solver_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="answer")
        print("Промпт отправлен")
        ans = solver_chain.invoke({"input_text": message.text})["answer"]
        await state.update_data(answer_en=ans)
        await state.update_data(lan="en")
        print("Ответ получен")
        ans = await language_text(message.from_user.id, ans)
        if await check_language_ru(message.from_user.id):
            await message.answer(ans, reply_markup=kb.say_ru)
            await state.set_state(Registration.confirmed)
        else:
            await message.answer(ans, reply_markup=kb.say_en)
            await state.set_state(Registration.confirmed)
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await state.set_state(Registration.confirmed)
        return

