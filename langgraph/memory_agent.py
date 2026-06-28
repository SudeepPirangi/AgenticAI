"""LangGraph - Memory Agent"""

from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from common import GEMINI_KEY, GEMINI_MODEL, GEMINI_URL


llm = ChatOpenAI(
    api_key=GEMINI_KEY,
    model=GEMINI_MODEL,
    base_url=GEMINI_URL,
)


class AgentState(TypedDict):
    "State schema"

    messages: List[Union[HumanMessage, AIMessage]]


ASK = "Ask"
FILE_PATH = "memory_agent_log.txt"


def ask_model(state: AgentState) -> AgentState:
    """Send a query to an AI Model and get the answer"""
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print("\nAI -> ", response.content)

    return state


graph = StateGraph(AgentState)

graph.add_node(ASK, ask_model)

graph.add_edge(START, ASK)
graph.add_edge(ASK, END)

agent = graph.compile()

conversation = []

user_input = input("\nHuman -> ")
while user_input != "q":
    conversation.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation})
    conversation = result["messages"]
    user_input = input('\n(press "q" to quit)\nHuman  -> ')

with open(FILE_PATH, "w", encoding="utf-8") as file:
    file.write("Conversation History: \n\n")

    for message in conversation:
        if isinstance(message, HumanMessage):
            file.write(f"Human -> {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI -> {message.content}\n\n")
    file.write("End of Conversation")

print(f"Conversation saved to {FILE_PATH}")
