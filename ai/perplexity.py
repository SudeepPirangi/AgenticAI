"""Perplexity"""

import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from agents import (
    OpenAIChatCompletionsModel,
    Agent,
    function_tool,
)

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

    async def agent(self, name: str, instructions: str, tools=[], model: str = MODEL):
        """Perplexity's own agent with OpenAI SDK"""
        print("Setting model as", model)
        # setting up perplexity client
        perplexity_ai = AsyncOpenAI(base_url=BASE_URL, api_key=PERPLEXITY_API_KEY)

        return Agent(
            name=name,
            instructions=instructions,
            model=OpenAIChatCompletionsModel(model=model, openai_client=perplexity_ai),
            tools=tools,
        )


@function_tool
async def agent_tool(name: str, instructions: str, tools=[]):
    """Perplexity's own agent tool works only with model as sonar-pro/sonar-reasoning-pro"""

    # setting up perplexity client
    perplexity_ai = AsyncOpenAI(base_url=BASE_URL, api_key=PERPLEXITY_API_KEY)

    return Agent(
        name=name,
        instructions=instructions,
        model=OpenAIChatCompletionsModel(
            model="sonar-pro", openai_client=perplexity_ai
        ),
        tools=tools,
    )
