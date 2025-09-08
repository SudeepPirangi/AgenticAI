"""Simple LangGraph app"""

from typing import TypedDict
from langgraph.graph import StateGraph
# from IPython.display import Image, display


class AppState(TypedDict):
    """Graph state schema"""

    message: str


def greet_user(state: AppState) -> AppState:
    """Simple Node that greets the users"""
    state["message"] = f"Hello {state['message']}, LangGraph welcomes you!"
    return state


# Initialize Graph
graph = StateGraph(AppState)

# Graph nodes
GREET_USER = "Greet User"

# Attach nodes to the Graph
graph.add_node(GREET_USER, greet_user)

# Setup entry and finish points of the Graph
graph.set_entry_point(GREET_USER)
graph.set_finish_point(GREET_USER)

# Compile the Graph
app = graph.compile()

# To view graph in Jupyter notebook
# display(Image(app.get_graph().draw_mermaid_png()))

# Runs the Graph
result = app.invoke({"message": "Sudeep"})

print(f"\n{result['message']}", "\n")
