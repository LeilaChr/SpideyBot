from dotenv import load_dotenv
import requests
import os


class ChatBot:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def ask(self, question, context):
        pre_prompt = "You're a chatbot for a quick one to one chat application with a human. Limit your responses to the following questions to a sentence or 2 max."
        context = [{"role": "assistant", "content": pre_prompt}] + context
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": context + [{"role": "user", "content": question}],
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
