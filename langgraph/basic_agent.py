"""Basic Agent"""

from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from common import PERPLEXITY_KEY, PERPLEXITY_MODEL, PERPLEXITY_URL


perplexity = ChatOpenAI(
    api_key=PERPLEXITY_KEY,
    model=PERPLEXITY_MODEL,
    base_url=PERPLEXITY_URL,
)


class AgentState(TypedDict):
    "State schema"

    messages: List[HumanMessage]


ASK = "Ask"


def ask_model(state: AgentState) -> AgentState:
    """Send a query to an AI Model and get the answer"""
    response = perplexity.invoke(state["messages"])
    print("\nAnswer: ", response.content)

    return state


graph = StateGraph(AgentState)

graph.add_node(ASK, ask_model)

graph.add_edge(START, ASK)
graph.add_edge(ASK, END)

agent = graph.compile()

user_input = input("\nQuestion: ")
while user_input != "q":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input('\nQuestion (press "q" to quit): ')
