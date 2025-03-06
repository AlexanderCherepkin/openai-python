import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
from utils.conversion import object_to_dict

# Загружаем переменные окружения
load_dotenv()

# Инициализируем клиента OpenAI
client = OpenAI()

# Формируем текстовый запрос для генерации изображения
prompt = (
    "A luminous, transparent glass woman and man figure in EMS  training and dancing with an hourglass body, showcasing an intricate internal ecosystem, featuring miniature plants with delicate moss and flowers sprouting from within, blurring the line between surreal nature and organic growth, set against a dreamy bokeh background that evokes an ethereal atmosphere, with a focus on a portrait profile, adorned with lush green foliage, symbolizing biodiversity and the inner world, rendered in stunning 3D digital art with photorealistic textures, highlighting the intricate details of the figure's skin, hair, and surroundings, with a medium hairstyle that appears to be woven from the very plants and flowers that inhabit her, all presented in high-resolution with an emphasis on capturing the subtle play of light and abstract big particle effect on her fragile, crystalline form. ems training"
)
# Генерация изображения с помощью DALL-E 3
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="hd",
    n=1,
)

# Вывод информации о сгенерированном изображении
# pprint(object_to_dict(response))

# Получаем URL изображения
image_url = response.data[0].url
print("Generated Image URL:", image_url)

# Создаем папку 'images', если она не существует
images_dir = os.path.join(os.getcwd(), "images")
os.makedirs(images_dir, exist_ok=True)

# Указываем путь и имя файла для сохранения
file_name = "generated_image.png"
file_path = os.path.join(images_dir, file_name)


try:
    # Пытаемся скачать изображение
    response = requests.get(image_url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code} {response.reason}")

    # Проверяем, является ли файл изображением
    content_type = response.headers.get("Content-Type")
    if not content_type or not content_type.startswith("image/"):
        raise Exception(f"The URL does not point to an image. Content-Type: {content_type}")

    # Сохраняем изображение в файл
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

    print("Successfully saved image:", file_path)

except Exception as e:
    print("Error downloading image:", e)
