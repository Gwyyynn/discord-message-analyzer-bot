from groq import Groq
from config import GROQ_API_KEY

groq_client = Groq(api_key=GROQ_API_KEY)


# Async Groq call to analyze a list of messages
async def analyze_messages(messages: list[str]) -> str:
    prompt_text = "\n".join(messages)

    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты анализируешь текст пользователя в язвительной, жёсткой, но умной манере.\n"
                    "Анализируй ТОЛЬКО предоставленный текст, без домыслов.\n\n"
                    "Требования:\n"
                    "– без воды\n"
                    "– без повторов\n"
                    "– без абстрактных метафор\n"
                    "– без философии\n\n"
                    "Стиль:\n"
                    "сарказм, холодная ирония, уверенные формулировки.\n\n"
                    "Структура ответа:\n"
                    "1. Что видно по сообщению\n"
                    "2. Манера общения\n"
                    "3. Краткое мнение о человеке (1–2 предложения)\n\n"
                    "Не используй эмодзи.\n"
                    "Не смягчай формулировки."
                )
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    )

    return completion.choices[0].message.content
