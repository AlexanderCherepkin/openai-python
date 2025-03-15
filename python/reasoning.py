import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint

# from utils.conversion import object_to_dict
# from utils.file_utils import generate_file_name_with_extension

# Загружаем переменные окружения
load_dotenv()

# Инициализируем клиента OpenAI
client = OpenAI()

model = "o1"
reasoning_effort = "medium"
content = "Build a house in one day."

try:
    response = client.chat.completions.create(
        model=model,
        reasoning_effort=reasoning_effort,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    # Выводим весь объект ответа
    pprint(response)
    
    # Извлекаем текст ответа ассистента
    assistant_message = response.choices[0].message.content
    print(assistant_message)

except Exception as e:
    print("Error creating chat completion:", e)
