"""Gemini"""

import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from agents import (
    OpenAIChatCompletionsModel,
    Agent,
)

from constants import AI

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = AI["GEMINI"]["MODEL"]
BASE_URL = AI["GEMINI"]["BASE_URL"]


class Gemini:
    """Gemini AI"""

    def __init__(self, role="user"):
        """Initialize the class"""
        self.role = role
        self.client = OpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

    def ask(self, question):
        """Query OpenAI with Gemini"""
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": self.role, "content": question}],
        )

        answer = response.choices[0].message.content

        print("\nAnswer: ", answer, "\n")

        return answer

    async def agent(
        self,
        name: str,
        instructions: str,
        tools=[],
        handoff_description="",
        handoffs=[],
        model: str = MODEL,
    ):
        """Gemini's own agent with OpenAI Agent SDK"""
        # setting up gemini client
        gemini_ai = AsyncOpenAI(base_url=BASE_URL, api_key=GEMINI_API_KEY)

        return Agent(
            name=name,
            instructions=instructions,
            model=OpenAIChatCompletionsModel(model=model, openai_client=gemini_ai),
            tools=tools,
            handoff_description=handoff_description,
            handoffs=handoffs,
        )
