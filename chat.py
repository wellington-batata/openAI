import openai
import os
from dotenv import find_dotenv, load_dotenv

# load the api key
_ = load_dotenv(find_dotenv())
client = openai.OpenAI(api_key=os.getenv("API_KEY"))


def get_response(msg):
    message = [{"role": "user", "content": msg}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=message,
        max_tokens=1000,
        temperature=0,
        stream=True
    )
    return response


print('Olá, sou seu assistente virtual. Como posso ajudar?')
print()
while True:
    print()
    user_input = input('User: ')
    if user_input.lower().__contains__('sair'):
        break
    response = get_response(user_input)
    print('')
    print('IA: ', end='')
    for i in response:
        txt = i.choices[0].delta.content
        if txt is not None:
            print(txt, end='')
    print()
