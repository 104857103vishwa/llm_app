import os
from mistralai import Mistral

class ChatMistralClient:
    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        self.api_key = api_key
        self.model = model
        self.client = Mistral(api_key=self.api_key)

    def ask_question(self, question: str) -> str:
        """
        Send a question to the Mistral model and get the response.
        """
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": question}],
        )
        return chat_response.choices[0].message.content

    def __call__(self, question: str) -> str:
        """Makes the client callable like a function."""
        return self.ask_question(question)