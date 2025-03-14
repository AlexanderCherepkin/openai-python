from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
import os
from base64 import b64decode
from utils.file_utils import generate_file_name_with_extension

# Загружаем переменные окружения
load_dotenv()

# Инициализируем клиента OpenAI
client = OpenAI()

# Настройки для генерации аудио
voice = "ash"  # Доступные голоса: alloy, echo, fable, onyx, nova, shimmer
model = "tts-1"  # Актуальная модель для генерации речи
content = "Я немного изменил текст, сделав его более естественным и плавным. Теперь он звучит так, как будто виртуальный ассистент действительно говорит с пользователем. Если нужно что-то подкорректировать — сообщи! "
format = "mp3"
audio_folder_name = "audio"

try:
    # Создание аудиофайла с помощью OpenAI API
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=content,
        response_format=format
    )
    
    # Создание директории для сохранения
    module_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(module_dir, audio_folder_name, format)
    os.makedirs(audio_dir, exist_ok=True)
    
    # Генерация имени файла
    file_name = generate_file_name_with_extension(
        prompt=content, dir=audio_dir, extension=format
    )
    file_path = os.path.join(audio_dir, file_name)
    
    # Запись аудиофайла на диск
    with open(file_path, "wb") as file:
        file.write(response.content)
    
    print("Successfully saved generated audio file:", file_name)
    
except Exception as e:
    print("Some error occurred:", e)
