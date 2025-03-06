import os
import json
import sys
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint
from utils.conversion import object_to_dict

# Очистка консоли
os.system("cls" if os.name == "nt" else "clear")

load_dotenv()

client = OpenAI()

system_text = (
    "Если спрашивают о цене акций, то отвечай не просто с ценой акции, но и с небольшой аналитикой рынка не более 100 слов."
    "А если спрашивают чат-бота о чем-то другом, отвечай как обычно!"
)

function_to_call = 'get_stock_price_via_api'
# function_to_call = 'get_stock_price'

def get_stock_price(stock):
    stock_prices = {
        "VZ": 38.24, "T": 16.52, "CMCSA": 43.17,
        "CHL": 29.82, "NTT": 30.45, "ORAN": 11.30,
        "TEF": 4.21, "AMX": 19.14, "BCE": 42.67, "BT": 11.78,
    }

    symbol = stock.get("symbol")
    stock_price = {"symbol": symbol, "price": f"${stock_prices.get(symbol, 100.0000)}"}
    return json.dumps(stock_price)

def get_stock_price_via_api(stock):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        print("ALPHA_VANTAGE_API_KEY не найден. Проверьте переменные окружения.")
        sys.exit()

    symbol = stock.get("symbol")
    api_function = "TIME_SERIES_INTRADAY"
    url = f"https://www.alphavantage.co/query?function={api_function}&symbol={symbol}&interval=5min&apikey={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if "Error Message" in data:
                print("Ошибка API:", data["Error Message"])
                return None
            return json.dumps(data, indent=4)
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON-ответа.")
            return None
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return None

def process_user_text_input(user_text, system_text, function_to_call):
    model = "gpt-4o"
    messages = []
    available_functions = {
        "get_stock_price": get_stock_price,
        "get_stock_price_via_api": get_stock_price_via_api
    }

    tools = [
        {
            "type": "function",
            "function": {
                "name": function_to_call,
                "description": "Get the current stock price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string", "description": "The stock symbol"}
                    },
                    "additionalProperties": False,
                    "required": ["symbol"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_stock_price_via_api",
                "description": "Fetch stock price from Alpha Vantage API",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string", "description": "The stock symbol"}
                    },
                    "additionalProperties": False,
                    "required": ["symbol"],
                },
            },
        }
    ]

    messages.append({"role": "system", "content": [{"type": "text", "text": system_text}]})
    messages.append({"role": "user", "content": [{"type": "text", "text": user_text}]})

    first_response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )

    tool_calls = first_response.choices[0].message.tool_calls

    if tool_calls and len(tool_calls) > 0:
        print("\nСледует вызвать функцию!")
        function_name = tool_calls[0].function.name
        function_to_call = available_functions.get(function_name)
        if function_to_call:
            function_arguments_to_pass = json.loads(tool_calls[0].function.arguments)
            function_response = function_to_call(function_arguments_to_pass)
            print(f'\nРезультат вызова функции "{function_name}": {function_response}')
            first_assistant_message = first_response.choices[0].message
            messages.append(first_assistant_message)

            tool_call_id = tool_calls[0].id
            tool_response_message = {
                "role": "tool",
                "content": [{"type": "text", "text": function_response}],
                "tool_call_id": tool_call_id,
            }
            messages.append(tool_response_message)

            second_response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
            )
            print("\nОтвет от чат-бота: ", second_response.choices[0].message.content)
    else:
        print("\nНе было инструкции вызвать функцию\n")
        print(first_response.choices[0].message.content)

if __name__ == "__main__":
    print("Спросите о стоимости акций, чтобы вызвать локальную функцию.\n")
    while True:
        user_input = input("\n\nВведите запрос к чат-боту (или 'exit' для выхода):\n>>>> ")
        if user_input.lower() == "exit":
            print("\nВыход из программы. До свидания!")
            break
        process_user_text_input(user_text=user_input, system_text=system_text, function_to_call=function_to_call)
