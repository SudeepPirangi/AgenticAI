"""
Simple Agentic AI Playground.

Entrypoint that loads environment variables and prints config.

Ask Perplexity a question and get the answer.

Usage:

python simple_question.py
(or)
uv run simple_question.py

"""

import os
from dotenv import load_dotenv
from openai import OpenAI

from constants import AI

load_dotenv(override=True)

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
MODEL, BASE_URL = AI["PERPLEXITY"].values()

client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url=BASE_URL)


def main():
    """
    Main function that loads environment variables and prints config.
    """

    question = input("\n\nAsk Perplexity - ")

    messages = [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    answer = response.choices[0].message.content

    print("\nAnswer: ", answer, "\n\n")


if __name__ == "__main__":
    main()
