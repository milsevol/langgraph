"""
创建一系列步骤,添加顺序节点
"""
from typing import TypedDict
from langgraph.constants import START
from langgraph.graph import StateGraph

class MyState(TypedDict):
    pass
def step_1(state: MyState):
    pass
def step_2(state: MyState):
    pass
def step_3(state: MyState):
    pass

# 使用add_sequence快速定义顺序图
builder = StateGraph(MyState).add_sequence([step_1, step_2, step_3])
builder.add_edge(START, step_1.__name__)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="../data/image/langgraph-api/07-sequence-node.png")