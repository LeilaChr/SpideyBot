from dotenv import load_dotenv
import requests
import os

# ChatBot class for interacting with the OpenAI GPT-3.5-turbo model
class ChatBot:
    def __init__(self):
        # Load environment variables, specifically the OpenAI API key
        load_dotenv()
        self.api_key = os.environ.get("OPENAI_API_KEY")

    # Method to ask a question and get a response from the GPT-3.5-turbo model
    def ask(self, question, context):
        pre_prompt = "You're a chatbot for a quick one to one chat application with a human. Limit your responses to the following questions to a sentence or 2 max."
        context = [{"role": "assistant", "content": pre_prompt}] + context

        # Define the OpenAI API endpoint
        url = "https://api.openai.com/v1/chat/completions"

        # Define headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        # Create data payload
        data = {
            "model": "gpt-3.5-turbo",
            "messages": context + [{"role": "user", "content": question}],
        }

        # Make a POST request to the OpenAI API
        response = requests.post(url, headers=headers, json=data)

        # Extract and return the content of the generated message from the API response
        return response.json()["choices"][0]["message"]["content"]
