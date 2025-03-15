import os
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
from utils.conversion import object_to_dict

# Загружаем переменные окружения
load_dotenv()

# Создаем клиент OpenAI
client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "what's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://i.pinimg.com/originals/8e/43/05/8e4305e5ca2524e022a75c5fdf0f1803.jpg",
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
    )

    pprint(object_to_dict(response))
    
except Exception as e:
    print("Error during OpenAI API communication occurred:", e)

