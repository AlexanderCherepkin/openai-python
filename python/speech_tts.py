from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
import os
import requests
from utils.conversion import object_to_dict
from utils.file_utils import generate_file_name_with_extension

# Загружаем переменные окружения
load_dotenv()

# Инициализируем клиента OpenAI
client = OpenAI()

voice="shimmer"
model = "tts-1-hd"
input = "Hello! My name is Tatiana, I am a virtual assistant, created to help, inspire and find solutions for a variety of tasks. I sincerely like to simplify people's lives, to be a reliable support in work, study or creativity."
response_format = "wav"
audio_folder_name = "audio"

try:
    with client.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=input,
        response_format=response_format,
    ) as response:
        # STEP 2 – Save audio file in the folder
        module_dir = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(module_dir, audio_folder_name, response_format)
        os.makedirs(audio_dir, exist_ok=True)

        file_name = generate_file_name_with_extension(
            prompt=input, dir=audio_dir, extension=response_format
        )
        file_path = os.path.join(audio_dir, file_name)

        with open(file_path, "wb") as audio_file:
            for chunk in response.iter_bytes():
                audio_file.write(chunk)

        print("Successfully saved generated audio file:", file_name)

except Exception as e:
    print("Some error occurred:", e)
