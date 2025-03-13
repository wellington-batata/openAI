
import openai
from typing import Optional
import os
from dotenv import find_dotenv, load_dotenv

# load the api key
_ = load_dotenv(find_dotenv())


class OpenAIClient:
    def __init__(self):
        key = os.getenv("API_KEY")
        if key == None:
            raise ValueError("API_KEY not found in environment variables")
        self.api_key = key
        # openai.api_key = self.api_key

    def get_client(self) -> openai:
        client = openai.Client(api_key=self.api_key)
        return client


# Example usage:
"""
from client_openai import OpenAIClient

# Initialize client
client = OpenAIClient(api_key="your-api-key-here")

# Get OpenAI client
openai_client = client.get_client()

# Use the client
response = openai_client.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)
"""
