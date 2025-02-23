import json
from openai import OpenAI
# from dotenv import load_dotenv
from pprint import pprint
from utils.conversion import object_to_dict


load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    # n=1,
    messages=[
        {"role": "system", "content": "Отвечай кратко, но с объяснением."},
        # или второй вариант
        # {"role": "system", "content": "Отвечай кратко, но с объяснением.Отвечай в формате JSON"},
        
        {"role": "user", "content": "Сколько тебе лет?"},
    ],
    response_format={'type': 'text'},  
    # или второй вариант
    # response_format={'type': 'json_object'},
    
    # temperature = 0.9
    # или второй вариант
    top_p = 0.9,
    # stop = 'нет',
    
)

# Получаем текст из ответа
raw_content = completion.choices[0].message.content

# Преобразуем строку в JSON-объект (если это JSON)
try:
    parsed_json = json.loads(raw_content)
    print(json.dumps(parsed_json, indent=4, ensure_ascii=False))  # Красиво выводим JSON
except json.JSONDecodeError:
    print(raw_content)  # Если не JSON, просто печатаем ответ
    


pprint(object_to_dict(completion), indent = 1)
