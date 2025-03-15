import openai
from dotenv import load_dotenv
from pydantic import BaseModel
from pprint import pprint
from utils.conversion import object_to_dict

# Загружаем переменные окружения
load_dotenv()

# Инициализируем клиента OpenAI
client = openai.OpenAI()

# Определяем модель данных
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

try:
    # Вызов API с явным упоминанием JSON
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You must respond strictly in valid JSON format."},  # 👈 Добавлено требование JSON-ответа
            {"role": "user", "content": "Extract the event information and return it as a JSON object. Alice and Bob are going to a meeting on 2024-08-06."}
        ],
        response_format={"type": "json_object"}  # ✅ Правильный response_format
    )
    
    print(completion)
    print("\n_________\n")

    pprint(object_to_dict(completion))
    print("\n_________\n")

    event = completion.choices[0].message.content  # Получаем JSON-ответ
    print(event)

except Exception as e:
    print("Error creating chat completion:", e)

