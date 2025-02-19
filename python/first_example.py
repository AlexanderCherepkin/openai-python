# import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# print(os.getenv('OPENAI_API_KEY'))

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    n = 1,
    messages=[
        {"role": "system", "content": "Отвечай кратко, но с обьяснением."},
        {"role": "user", "content": "Сколько тебе лет."},
    ],
)

print(completion.choices[0].message)


