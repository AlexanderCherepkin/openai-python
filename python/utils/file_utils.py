import os
import re
from urllib.parse import urlparse

def generate_file_name_with_extension(prompt, dir, extension):
    """
    Генерирует имя файла на основе prompt и директории.
    """
    # Преобразуем prompt в нижний регистр, заменяем пробелы на "_", ограничиваем до 25 символов
    base_file_name = "_".join(prompt.lower().split()[:25])[:25]

    # Используем правильную переменную dir вместо dir_path
    version = get_next_version_number(base_file_name, extension, dir)

    return f"{base_file_name}_v{version}.{extension}"


def get_next_version_number(base_file_name, extension, dir):
    """
    Определяет следующий номер версии файла, проверяя существующие файлы в директории.
    """
    file_pattern = re.compile(rf"^{re.escape(base_file_name)}_v(\d+)\.{re.escape(extension)}$")
    highest_version = 0

    if not os.path.exists(dir):
        return 1

    for file in os.listdir(dir):
        match = file_pattern.match(file)
        if match:
            file_version = int(match.group(1))
            highest_version = max(highest_version, file_version)

    return highest_version + 1
  
import os
import json

def write_image_data_to_json_file(file_path, data):
    """
    Записывает данные в JSON-файл. Если файл уже существует, добавляет данные в список.
    """
    # Проверяем, существует ли файл и не пуст ли он
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)  # Загружаем JSON-данные
                if not isinstance(existing_data, list):  
                    existing_data = [existing_data]  # Преобразуем в список, если это не массив
        except (json.JSONDecodeError, IOError):
            existing_data = []  # Если файл повреждён или пуст, создаём пустой список
    else:
        existing_data = []  # Если файла нет, создаём пустой список

    # Добавляем новые данные
    existing_data.append(data)

    # Записываем обновлённые данные обратно в файл
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)


