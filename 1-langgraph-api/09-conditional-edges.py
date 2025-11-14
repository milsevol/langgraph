"""
条件分支
"""

import operator
import time
from typing import Annotated, TypedDict, Literal

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class MyState(TypedDict):
    step: str
    aggregate: Annotated[list[str], operator.add]

def node_a(state: MyState):
    return {"aggregate": state["aggregate"]}
def node_b(state: MyState):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["BB"]}
def node_c(state: MyState):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["CC"]}
def node_d(state: MyState):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["DD"]}

def condition_edge(state: MyState) -> Literal[node_b.__name__, node_c.__name__, node_d.__name__]:
    step = state["step"]
    if step == "B":
        return node_b.__name__
    else:
        # 路由到多个节点
        return [node_c.__name__, node_d.__name__]


builder = StateGraph(MyState)
builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_d)

builder.add_edge(START, node_a.__name__)
builder.add_conditional_edges(node_a.__name__, condition_edge)
builder.add_edge([node_b.__name__, node_c.__name__, node_d.__name__], END)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="../data/image/langgraph-api/09-conditional-edges.png")

print(graph.invoke({"step": "B"}))
print(graph.invoke({"step": "CD"}))