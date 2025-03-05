import os
import json
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
    "А если спрашивают о чат-бота о чем-то другом отвечай как обычно!"
)


def get_stock_price(stock):
    stock_prices = {
        "VZ": 38.24,  # Verizon Communications Inc.
        "T": 16.52,  # AT&T Inc.
        "CMCSA": 43.17,  # Comcast Corporation
        "CHL": 29.82,  # China Mobile Limited
        "NTT": 30.45,  # Nippon Telegraph and Telephone Corporation
        "ORAN": 11.30,  # Orange S.A.
        "TEF": 4.21,  # Telefónica, S.A.
        "AMX": 19.14,  # América Móvil, S.A.B. de C.V.
        "BCE": 42.67,  # BCE Inc.
        "BT": 11.78,  # BT Group plc
    }

    symbol = stock.get("symbol")
    stock_price = {
        "symbol": symbol,
        "price": f"${stock_prices.get(symbol, 100.00)}",
    }

    return json.dumps(stock_price)


def process_user_text_input(user_text, system_text):
    model = "gpt-4o"
    messages = []
    available_functions = {
        "get_stock_price": get_stock_price,
    }

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Get the current stock price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string", "description": "The stock symbol"}
                    },
                    "additionalProperties": False,
                    "required": ["symbol"],
                },
                "strict": True,
            },
        }
    ]

    # STEP 0 – Set system text
    messages.append(
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_text,
                }
            ],
        }
    )

    # ------------------------------------------------------------------

    # STEP 1 - Send initial user request
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_text,
                }
            ],
        }
    )

    first_response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )

    # pprint(object_to_dict(first_response), indent=1)  # Для отладки

    # --------------------------------------------------------------------

    tool_calls = first_response.choices[0].message.tool_calls

    if tool_calls:
        # STEP 2 - Call a function locally
        print("\nСледует вызвать функцию!")
        function_name = tool_calls[0].function.name
        function_to_call = available_functions[function_name]

        function_arguments_to_pass = json.loads(tool_calls[0].function.arguments)
        function_response = function_to_call(function_arguments_to_pass)

        print(f'\nРезультат вызова функции "{function_name}": {function_response}')

        # STEP 3 -- update list of messages by appending response from the assistant and result of the tool call
        first_assistant_message = first_response.choices[0].message
        messages.append(first_assistant_message)

        tool_call_id = tool_calls[0].id
        tool_response_message = {
            "role": "tool",
            "content": [
                {
                    "type": "text",
                    "text": function_response,
                }
            ],
            "tool_call_id": tool_call_id,
        }

        messages.append(tool_response_message)

        # pprint(object_to_dict(messages), indent=1)  # Для отладки

        # STEP 4 – send result of the function call to the assistant
        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )

        print("\nОтвет от чат-бота: ", second_response.choices[0].message.content)

    else:
        print("\nНе было инструкции вызвать функцию\n")
        print(first_response.choices[0].message.content)

    print("\n******************************************************\n")


# Бесконечный цикл обработки запросов
while True:
    print("Спросите о стоимости акций, чтобы вызвать локальную функцию.\n")

    user_input = input("Введите запрос к чат-боту (или 'exit' для выхода):\n>>>> ")

    if user_input.lower() == "exit":
        print("\nВыход из программы. До свидания!")
        break

    process_user_text_input(user_text=user_input, system_text=system_text)
