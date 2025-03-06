from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
import os
import requests
import base64
from datetime import datetime
from utils.conversion import object_to_dict
from utils.file_utils import generate_file_name_with_extension
from utils.file_utils import write_image_data_to_json_file

# Загружаем переменные окружения
load_dotenv()

# Инициализируем клиента OpenAI
client = OpenAI()

# Исправленный prompt (строка, без списка)**
prompt = "A dramatic and intense naval battle between pirate ships on a stormy sea. Two massive wooden vessels with tattered black sails engage in fierce combat, their cannons firing blazing projectiles that explode upon impact. The deck is chaotic, with pirates wielding cutlasses and pistols, swinging from ropes to board the enemy ship. Smoke and fire rise from the damaged hulls, while ocean waves crash violently against the sides. The sky is dark with heavy storm clouds, illuminated by flashes of lightning. The scene is filled with tension, action, and the raw power of an epic maritime battle."

# Параметры запроса**
model = "dall-e-3"
response_format = "b64_json"  # Формат base64
size = "1024x1024"
quality = "standard"
style = "natural"
n = 1

# Файл для хранения информации об изображениях**
json_filename = "images.json"

try:
    # Генерация изображения с помощью DALL-E 3**
    response = client.images.generate(
        model=model,
        prompt=prompt,  # ✅ Теперь передаётся как строка
        response_format=response_format,
        size=size,
        style=style,
    )

    # Вывод информации о сгенерированном изображении**
    # pprint(object_to_dict(response))

    b64_data = response.data[0].b64_json
    revised_prompt = response.data[0].revised_prompt

    if b64_data:
        # Создаём папку 'images', если её нет**
        images_dir = os.path.join(os.getcwd(), "images")
        os.makedirs(images_dir, exist_ok=True)

        # Формируем имя файла**
        file_name = generate_file_name_with_extension(prompt, images_dir, "png")
        file_path = os.path.join(images_dir, file_name)

        # Сохраняем изображение**
        image_bytes = base64.b64decode(b64_data)
        with open(file_path, "wb") as file:
            file.write(image_bytes)

        print("Successfully saved image:", file_path)

        # Создаём JSON-данные**
        image_data = {
            "prompt": prompt,
            "revised_prompt": revised_prompt,
            "size": size,
            "style": style,
            "model": model,
            "date": datetime.now().strftime("%d-%m-%Y"),
            "base64": b64_data,
        }

        # Сохраняем в JSON**
        json_file_path = os.path.join(images_dir, json_filename)
        write_image_data_to_json_file(json_file_path, image_data)

except Exception as e:
    print("Error generating or saving image:", e)
