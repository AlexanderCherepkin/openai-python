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
response_format = "vtt"  # Должно быть явно задано

# Имена папок и файлов
audio_folder_name = "audio"
translation_folder_name = "translation"

input_audio_name = "test-file_v1.m4a"
output_file_name = f"test-file_v1.{response_format}"

# Определяем пути к файлам
module_dir = os.path.dirname(os.path.abspath(__file__))
translation_dir = os.path.join(module_dir, audio_folder_name, translation_folder_name)

# Создаем папку, если ее нет
os.makedirs(translation_dir, exist_ok=True)

input_audio_file_path = os.path.join(translation_dir, input_audio_name)
output_file_path = os.path.join(translation_dir, output_file_name)

# Проверяем, существует ли файл перед обработкой
if not os.path.exists(input_audio_file_path):
    print(f"Ошибка: Файл '{input_audio_file_path}' не найден. Проверьте путь и попробуйте снова.")
else:
    try:
        # STEP 1 - Get audio translation (Исправлено)
        with open(input_audio_file_path, "rb") as input_audio_file:
            response = client.audio.translations.create(  # ← Исправленный вызов API
                model=model,
                file=input_audio_file,
                response_format=response_format,
            )

        # Вывод результата
        translation_data = object_to_dict(response)
        pprint(translation_data)

        # Сохраняем результат в файл в зависимости от формата
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            if response_format == "text":
                output_file.write(response)
            else:  # JSON или другой формат
                json.dump(translation_data, output_file, ensure_ascii=False, indent=4)

        print(f"Перевод успешно сохранен в '{output_file_path}'")

    except Exception as e:
        print("Ошибка во время обработки OpenAI API:", e)

