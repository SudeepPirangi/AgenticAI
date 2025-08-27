"""Simple Agent from OpenAI - Agents SDK"""

import asyncio
from agents import (
    Runner,
    set_tracing_disabled,
    trace,
)
from openai.types.responses import ResponseTextDeltaEvent

from common import PERPLEXITY_URL, PERPLEXITY_MODEL, perplexity_ai


async def main():
    """Make an agent with name, instructions, model"""

    try:
        # Disable tracing to avoid using a platform tracing key; adjust as needed.
        set_tracing_disabled(disabled=False)  # default: False

        agent = await perplexity_ai.agent(
            name="Assistant",
            instructions="Be precise and concise.",
        )
        prompt = "What's the weather in Tokyo?"

        with trace("Just Assistant"):
            print("\nFully loaded response: ")
            result = await Runner.run(agent, prompt)
            print("Answer: ", result.final_output, "\n")

            # stream results
            result = Runner.run_streamed(agent, input=prompt)
            print("\nStreamed Response: ")
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    print(event.data.delta, end="", flush=True)

    except Exception as e:
        print(f"Error running agent: {e}")
        return "Sorry, I encountered an error processing your request."


if __name__ == "__main__":
    print(
        f"\nRunning OpenAI Agent with {PERPLEXITY_URL} and model as {PERPLEXITY_MODEL}"
    )
    asyncio.run(main())
