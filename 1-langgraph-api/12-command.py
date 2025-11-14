"""
将控制流和状态更新结合起来,Command更新和跳转。
"""
import random
from typing import TypedDict, Literal

from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import Command


class State(TypedDict):
    foo: str

def node_b(state: State):
    print("Called B")
    return {"foo": state["foo"] + "b"}

def node_c(state: State):
    print("Called C")
    return {"foo": state["foo"] + "c"}

def node_a(state: State) -> Command[Literal[node_b.__name__, node_c.__name__]]:
    print("Called A")
    goto = random.choice([node_b.__name__, node_c.__name__])
    return Command(
        goto=goto,
        update={"foo": goto},
        # 从子图中的一个节点导航到另一个子图（即父图中的另一个节点）
        # graph = Command.PARENT
    )


builder = StateGraph(State)
builder.add_edge(START, node_a.__name__)

builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path='../data/image/langgraph-api/12-command.png')

print(graph.invoke({"foo": ""}))