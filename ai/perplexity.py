"""Perplexity"""

import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from agents import (
    OpenAIChatCompletionsModel,
    Agent,
    Runner,
    set_tracing_disabled,
    trace,
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

    async def agent(
        self,
        name: str,
        instructions: str,
        prompt: str,
        trace_name: str,
        is_tracing_disabled: bool = False,
    ):
        """Perplexity's own agent with OpenAI SDK"""

        # Disable tracing to avoid using a platform tracing key; adjust as needed.
        set_tracing_disabled(disabled=is_tracing_disabled)

        # setting up perplexity client
        perplexity_ai = AsyncOpenAI(base_url=BASE_URL, api_key=PERPLEXITY_API_KEY)

        agent = Agent(
            name=name,
            instructions=instructions,
            model=OpenAIChatCompletionsModel(model=MODEL, openai_client=perplexity_ai),
        )

        with trace(trace_name):
            result = await Runner.run(agent, prompt)
            print("\nAnswer: ", result.final_output, "\n")
            return result.final_output
