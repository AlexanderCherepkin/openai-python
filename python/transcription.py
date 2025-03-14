from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
import os
import json
from utils.conversion import object_to_dict

# Загружаем переменные окружения
load_dotenv()

# Инициализируем OpenAI клиент
client = OpenAI()

# Настройки модели и формата ответа
model = "whisper-1"
response_format = "srt"  # Должно быть явно задано

# Имена папок и файлов
audio_folder_name = "audio"
transcriptions_folder_name = "transcriptions"

input_audio_name = "test-file3.m4a"
output_file_name = "test-file3.srt"

# Определяем пути к файлам
module_dir = os.path.dirname(os.path.abspath(__file__))
transcriptions_dir = os.path.join(module_dir, audio_folder_name, transcriptions_folder_name)

# Создаем папку, если ее нет
os.makedirs(transcriptions_dir, exist_ok=True)

input_audio_file_path = os.path.join(transcriptions_dir, input_audio_name)
output_file_path = os.path.join(transcriptions_dir, output_file_name)

# Проверяем, существует ли файл перед обработкой
if not os.path.exists(input_audio_file_path):
    print(f"Ошибка: Файл '{input_audio_file_path}' не найден. Проверьте путь и попробуйте снова.")
else:
    try:
        # STEP 1 - Get audio transcription
        with open(input_audio_file_path, "rb") as input_audio_file:
            response = client.audio.transcriptions.create(
                model=model,
                file=input_audio_file,
                response_format=response_format,
            )

        # Вывод результата
        pprint(object_to_dict(response))

        # Сохраняем результат в файл в зависимости от формата
        if response_format == "text":
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(response)
        else:  # Если JSON или другой формат
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                json.dump(object_to_dict(response), output_file, ensure_ascii=False, indent=4)

        print(f"Транскрипция успешно сохранена в '{output_file_path}'")

    except Exception as e:
        print("Ошибка во время обработки OpenAI API:", e)
