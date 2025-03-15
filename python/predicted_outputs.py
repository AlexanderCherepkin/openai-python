import openai
from dotenv import load_dotenv
from pprint import pprint
import os

# Загружаем переменные окружения
load_dotenv()

# Убедимся, что API-ключ загружен
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API ключ не найден. Укажите его в .env файле.")

# Инициализируем клиента OpenAI
client = openai.OpenAI(api_key=api_key)

try:
    code = """
    class User {
      firstName: string = "";
      lastName: string = "";
      username: string = "";
    }

    export default User;
    """

    refactor_prompt = """
    Replace the "username" property with an "email" property. Respond only 
    with code, and with no markdown formatting.
    """

    # Отправляем запрос в OpenAI с потоковой обработкой
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert TypeScript developer."},
            {"role": "user", "content": refactor_prompt},
            {"role": "user", "content": f"Here is the code:\n{code}"}
        ],
        stream=True
    )

    # Выводим потоковый результат посимвольно
    print("Generated Code:\n")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")

except Exception as e:
    print("Error creating chat completion:", e)
