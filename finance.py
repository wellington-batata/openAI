
import openai
import os
import json
import yfinance as yf
from dotenv import find_dotenv, load_dotenv

# load the api key
_ = load_dotenv(find_dotenv())
client = openai.Client(api_key=os.getenv("API_KEY"))


def finance_quote_history(ticker, period="1mo", limit=50):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)["Close"]
    history.index = history.index.strftime("%d//%m/%Y")
    history = round(history, 2)
    if len(history) > limit:
        history = history[-limit:]
    else:
        history = history
    return history


tools = [
    {
        "type": "function",
        "function": {
            "name": "finance_quote_history",
            "description": "Get the historical quote of a stock",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker of the stock",
                    },
                    "period": {
                        "type": "string",
                        "description": "The period of the quote",
                        "enum": ["1d", "5d", "1mo"],
                    },
                },
                "required": ["ticker", "period"],
            },
        },
    }
]

avaliabble_functions = {
    "finance_quote_history": finance_quote_history,
}


def output_text(messages):
    output_message = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    tool_calls = output_message.choices[0].message.tool_calls

    if tool_calls:
        messages.append(output_message.choices[0].message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = avaliabble_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response.to_json(),
            })

    output = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        stream=True
    )
    return output


if __name__ == "__main__":
    print("Olá, sou seu assistente virtual FINANCEIRO. Como posso ajudar?")
    print()
    messages = []
    while True:
        print()
        user_input = input("User: ")
        if user_input.lower().__contains__("sair"):
            print("Saindo...")
            break
        messages.append({"role": "user", "content": user_input})
        output = output_text(messages)
        print('chatGPT: ', end='')
        for i in output:
            txt = i.choices[0].delta.content
            if txt is not None:
                print(txt, end='')
        print()
