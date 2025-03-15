import openai
from dotenv import load_dotenv
from pprint import pprint
from utils.conversion import object_to_dict

# Загружаем переменные окружения
load_dotenv()

# Инициализируем клиента OpenAI
client = openai.OpenAI()


try:
    # Вызов API с явным упоминанием JSON
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You must respond strictly in valid JSON format.",
            },  # 👈 Добавлено требование JSON-ответа
            {
                "role": "user",
                "content": "Extract the event information and return it as a JSON object. Alice and Bob are going to a meeting on 2024-08-06.",
            },
        ],
        store=True,
        metadata={
            "role": "programmer",
            "language": "Java",
        },
    )
    
    pprint(object_to_dict(completion.choices[0]))


except Exception as e:
    print("Error creating chat completion:", e)
