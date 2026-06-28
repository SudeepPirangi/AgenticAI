"""Atomesus"""

import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel

from constants import AI

load_dotenv(override=True)

ATOMESUS_API_KEY = os.getenv("ATOMESUS_API_KEY")

MODEL = AI["ATOMESUS"]["MODEL"]
BASE_URL = AI["ATOMESUS"]["BASE_URL"]


class Atomesus:
    """Atomesus AI"""

    def __init__(self, role="user"):
        """Initialize the class"""
        self.role = role
        self.client = OpenAI(api_key=ATOMESUS_API_KEY, base_url=BASE_URL)

    def ask(self, question, stream=False):
        """Query OpenAI-compatible API with Atomesus"""
        return self.chat([{"role": self.role, "content": question}], stream=stream)

    def chat(self, messages, stream=False):
        """Query Atomesus with full conversation history"""
        if stream:
            return self._chat_stream(messages)

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )

        answer = response.choices[0].message.content
        print("\nAnswer: ", answer, "\n")
        self._print_usage(response.usage)

        return answer

    def _chat_stream(self, messages):
        """Stream Atomesus response and print token usage"""
        stream = self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            stream_options={"include_usage": True},
        )

        print("\nAnswer: ", end="", flush=True)

        answer_parts = []
        usage = None

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                answer_parts.append(content)
            if chunk.usage:
                usage = chunk.usage

        answer = "".join(answer_parts)
        print()
        self._print_usage(usage)

        return answer

    def _print_usage(self, usage):
        """Print token usage for the current prompt"""
        if not usage:
            print("\nUsage: unavailable\n")
            return

        print(
            f"\nUsage: prompt={usage.prompt_tokens} | "
            f"completion={usage.completion_tokens} | "
            f"total={usage.total_tokens}\n"
        )

    async def agent(
        self,
        name: str,
        instructions: str,
        tools=[],
        handoff_description="",
        handoffs=[],
        input_guardrails=[],
        output_type=None,
        model: str = MODEL,
    ):
        """Atomesus agent with OpenAI Agent SDK"""
        print(f"Atomesus | model: {model} | Agent: {name}")
        atomesus_ai = AsyncOpenAI(base_url=BASE_URL, api_key=ATOMESUS_API_KEY)

        return Agent(
            name=name,
            instructions=instructions,
            model=OpenAIChatCompletionsModel(model=model, openai_client=atomesus_ai),
            tools=tools,
            handoff_description=handoff_description,
            handoffs=handoffs,
            input_guardrails=input_guardrails,
            output_type=output_type,
        )
