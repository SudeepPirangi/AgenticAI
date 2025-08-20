"""
First ask the LLM to pick a business area that might be worth exploring for an Agentic AI opportunity.
Then ask the LLM to present a pain-point in that industry - something challenging that might be ripe for an Agentic solution.
Finally have 3 third LLM call propose the Agentic AI solution.
We will cover this at up-coming labs, so don't worry if you're unsure.. just give it a try!
"""

from ai.perplexity import Perplexity
from utils import display


def find():
    """Processes question & answers"""
    perplexity = Perplexity()

    display.divider()

    # First question
    question = "Pick a business area that might be worth exploring for an Agentic AI opportunity"

    print("Question: ", question)
    business_area = perplexity.ask(question)

    display.divider()

    # Second question
    ask_pain_point = "What is the pain point in this business area?"

    print("Question: ", ask_pain_point)
    ask_pain_point = business_area + ". " + ask_pain_point
    pain_point = perplexity.ask(ask_pain_point)

    display.divider()

    # Third question
    ask_solution = "What is the solution to this?"

    print("Question: ", ask_solution)
    ask_solution = pain_point + ". " + ask_solution
    perplexity.ask(ask_solution)


if __name__ == "__main__":
    find()
