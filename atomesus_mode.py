"""
Simple Agentic AI Playground.

Chat with Atomesus until you type "exit".

Usage:

python atomesus_mode.py
(or)
uv run atomesus_mode.py

"""

from ai.atomesus import Atomesus


def main():
    """Chat with Atomesus in a loop until the user types exit."""
    atomesus = Atomesus()
    conversation = []

    user_input = input("\nAsk Atomesus - ")
    while user_input != "exit":
        conversation.append({"role": "user", "content": user_input})
        answer = atomesus.chat(conversation)
        conversation.append({"role": "assistant", "content": answer})
        user_input = input('\n(type "exit" to quit)\n\nAsk Atomesus - ')


if __name__ == "__main__":
    main()
