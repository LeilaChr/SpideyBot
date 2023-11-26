from dotenv import load_dotenv
import requests
import os


class ChatBot:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def ask(self, question):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": question},
            ],
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
