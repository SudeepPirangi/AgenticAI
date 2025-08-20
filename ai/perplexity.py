"""Perplexity"""

import os
from dotenv import load_dotenv
from openai import OpenAI

from constants import AI

load_dotenv(override=True)

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

MODEL = AI["PERPLEXITY"]["MODEL"]
BASE_URL = AI["PERPLEXITY"]["BASE_URL"]


class Perplexity:
    """Perplexity AI"""

    def __init__(self, role="user"):
        """Initialize the class"""
        self.role = role
        self.client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url=BASE_URL)

    def ask(self, question):
        """Query OpenAI with Perplexity"""
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": self.role, "content": question}],
        )

        answer = response.choices[0].message.content

        print("\nAnswer: ", answer, "\n")

        return answer
