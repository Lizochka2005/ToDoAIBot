from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from aiogram.filters import Command

from states import Question
from initialisation import llm
import keyboards as kb


answer_question = Router()


@answer_question.message(Command("answer_question"))
async def user_question(message: Message, state: FSMContext):
    await message.answer("Готов ответить на твой вопрос!")
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
        await message.answer(ans, reply_markup=kb.say_and_translate)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    await message.answer("Выбери команду")

