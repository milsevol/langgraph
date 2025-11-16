import operator
import time
from pathlib import Path
from typing import Annotated, TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

class MyState(TypedDict):
    aggregate: Annotated[list[str], operator.add]

def node_a(state: MyState):
    return {"aggregate": ["A"]}

def node_b(state: MyState):
    time.sleep(1)
    return {"aggregate": ["B"]}

def node_c(state: MyState):
    return {"aggregate": ["C"]}

def node_e(state: MyState):
    time.sleep(5)
    return {"aggregate": ["E"]}

def node_d(state: MyState):
    return {"aggregate": ["D"]}

builder = StateGraph(MyState)
builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_e)
builder.add_node(node_d, defer=True)

builder.add_edge(START, node_a.__name__)
builder.add_edge(node_a.__name__, node_b.__name__)
builder.add_edge(node_a.__name__, node_c.__name__)
builder.add_edge(node_a.__name__, node_e.__name__)
builder.add_edge([node_b.__name__, node_c.__name__], node_d.__name__)
builder.add_edge(node_d.__name__, END)

graph = builder.compile()

output_file_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "image"
    / "langgraph-api"
    / "08-parallel-node01.png"
)
output_file_path.parent.mkdir(parents=True, exist_ok=True)
graph.get_graph().draw_mermaid_png(output_file_path=str(output_file_path))
graph.invoke({"aggregate": []})