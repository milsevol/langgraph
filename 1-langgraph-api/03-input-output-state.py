"""
当指定不同的State时，内部模式仍将用于节点之间的通信。
输入State确保提供的输入符合预期的结构，
而输出State则根据定义的输出State过滤内部数据，仅返回相关信息。
"""
from typing import TypedDict
from langgraph.graph import StateGraph

class Node1OutputState(TypedDict):
    b: str

class Node2OutputState(TypedDict):
    c: str

class OverallState(Node1OutputState, Node2OutputState):
    a: str

def node1(state: OverallState) -> Node1OutputState:
    return {"b": "b"}

def node2(state: Node1OutputState) -> Node2OutputState:
    return {"c": "c"}

builder = StateGraph(OverallState, input_schema=OverallState, output_schema=Node2OutputState)
builder.add_sequence([node1, node2])
builder.set_entry_point(node1.__name__)
builder.set_finish_point(node2.__name__)
compiled = builder.compile()

# 输出为output_schema指定State
print(compiled.invoke({"a": "a"}))
