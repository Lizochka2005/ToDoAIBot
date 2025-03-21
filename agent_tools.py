from langchain.tools import BaseTool
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from initialisation import llm

memory = ConversationBufferMemory(memory_key="chat_history")

prompt_template = PromptTemplate(
            input_variables=["input_text"],
            template="{input_text}\n Please make answer shorter. Pease don't use ** in your answer.",
        )
solver_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="answer")

class ShortenTextTool(BaseTool):
    name: str = "Shorten Text"
    description: str = "Use this tool to shorten the input text and remove any ** formatting."

    def _run(self, input_text: str):
        # Используем solver_chain для обработки текста
        result = solver_chain.invoke({"input_text": input_text})["answer"]
        return result

    async def _arun(self, input_text: str) -> str:
        # Асинхронная версия (если требуется)
        result = await solver_chain.ainvoke({"input_text": input_text})["answer"]
        return result

shorten_text_tool = ShortenTextTool()
tools = [shorten_text_tool]
agent = initialize_agent(
    tools,
    llm,
    agent="conversational-react-description",
    verbose=True,
    memory=memory,
)