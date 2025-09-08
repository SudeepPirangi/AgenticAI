"""Simple LangGraph app"""

from math import prod
from typing import TypedDict, List
from langgraph.graph import StateGraph
# from IPython.display import Image, display


class AppState(TypedDict):
    """Graph state schema"""

    operation: str
    values: List[int]
    result: int
    message: str


def calculate_list(state: AppState) -> AppState:
    """calculates as per operation"""

    operation = input(
        "\nEnter any one of the operations to be performed among [ + | * ]: "
    )

    state["operation"] = operation
    if operation == "+":
        state["result"] = sum(state["values"])
        state["message"] = f"Sum of all the values is {state['result']}"

    if operation == "*":
        state["result"] = prod(state["values"])
        state["message"] = f"Product of all the values is {state['result']}"

    print(state)
    return state


# Initialize Graph
graph = StateGraph(AppState)

# Graph nodes
CALCULATE = "calculate"

# Attach nodes to the Graph
graph.add_node(CALCULATE, calculate_list)

# Setup entry and finish points of the Graph
graph.set_entry_point(CALCULATE)
graph.set_finish_point(CALCULATE)

# Compile the Graph
app = graph.compile()

# To view graph in Jupyter notebook
# display(Image(app.get_graph().draw_mermaid_png()))

# Runs the Graph
result = app.invoke({"operation": "*", "values": [10, 20, 30, 40]})

print(f"\n{result['message']}", "\n")
