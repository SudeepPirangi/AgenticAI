"""Simple Agent from OpenAI - Agents SDK"""

import asyncio

from common import PERPLEXITY_URL, PERPLEXITY_MODEL, perplexity_ai


async def main():
    """Make an agent with name, instructions, model"""

    try:
        await perplexity_ai.agent(
            name="Assistant",
            instructions="Be precise and concise.",
            prompt="What's the weather in Tokyo?",
            trace_name="Just Assistant",
        )

    except Exception as e:
        print(f"Error running agent: {e}")
        return "Sorry, I encountered an error processing your request."


if __name__ == "__main__":
    print(
        f"\nRunning OpenAI Agent with {PERPLEXITY_URL} and model as {PERPLEXITY_MODEL}"
    )
    asyncio.run(main())
