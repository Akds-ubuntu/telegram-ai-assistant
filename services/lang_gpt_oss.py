from langchain_openai import ChatOpenAI
from config import settings
from schemas.response import QuizResponse
from prompts.template_prompts import prompt_template
import logging


llm = ChatOpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    model=settings.GROQ_LLM_MODEL,
    temperature=0.7,
    max_retries=2,
)

structured_llm = llm.with_structured_output(QuizResponse)

chain = prompt_template | structured_llm


async def evaluate_answer(
    question: str, correct_answer: str, user_answer: str, history: list = None
) -> QuizResponse:
    try:
        result = await chain.ainvoke(
            {
                "question": question,
                "correct_answer": correct_answer,
                "user_answer": user_answer,
                "chat_history": history or [],
            }
        )
        return result
    except Exception as e:
        logging.error(f"Ошибка при обращении к модели: {e}")
        return QuizResponse(
            is_correct=False, reply_text="Чет связь барахлит. Повтори-ка."
        )
