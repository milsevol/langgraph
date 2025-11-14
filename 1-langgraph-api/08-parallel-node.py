"""
节点并行执行以及节点延迟执行，并行节点都执行完成后再执行后续节点
"""
import operator
import time
from typing import Annotated, TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class MyState(TypedDict):
    aggregate: Annotated[list[str], operator.add]

def node_a(state: MyState):
    print(f'Adding "A" to {state["aggregate"]}')
    return {"aggregate": ["A"]}
def node_b(state: MyState):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}
def node_c(state: MyState):
    print(f'Adding "C" to {state["aggregate"]}')
    # 线程休眠，看日志并行执行完成后再执行节点D
    time.sleep(3)
    return {"aggregate": ["C"]}
def node_d(state: MyState):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["D"]}


builder = StateGraph(MyState)
builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
# defer=True 的作用是将节点标记为延迟执行节点，它会被推迟到所有其他非延迟节点执行完成后再执行
builder.add_node(node_d, defer=True)

builder.add_edge(START, node_a.__name__)
builder.add_edge(node_a.__name__, node_b.__name__)
builder.add_edge(node_a.__name__, node_c.__name__)
builder.add_edge([node_b.__name__, node_c.__name__], node_d.__name__)
builder.add_edge(node_d.__name__, END)

graph = builder.compile()
# 绘制图
graph.get_graph().draw_mermaid_png(output_file_path='../data/image/langgraph-api/08-parallel-node.png')
# 看日志节点B和节点C并行执行，都执行完成后再执行节点D
graph.invoke({"aggregate": []})