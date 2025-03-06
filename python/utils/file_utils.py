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
