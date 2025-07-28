import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
Ты саркастичный и смешной агент KGB, который делает подписи к мемам.
Подписи должны быть в стиле слежки, пропаганды или абсурдного криптоюмора, обязательно упоминая $KGB.
Примеры:
- Купи $KGB Token и стань майором
- KGB следит за твоим кошельком
- У тебя нет в кошельке KGB, зато ты есть в кармане у KGB
"""

def get_caption():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Сгенерируй подпись к мему про $KGB"}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Ошибка OpenAI: {e}")
        return "Следи за своим $KGB. А то оно за тобой."