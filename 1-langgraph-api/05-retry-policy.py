"""
添加重试策略
"""
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy


class MyState(TypedDict):
    my_state_value: str


def node_1(state: MyState):
    state_value = state["my_state_value"]
    # 控制台可以看到日志输出了多次
    print(f"node_1执行了")
    if state_value == "a":
        return {"my_state_value": state_value + "a"}
    else:
        raise ValueError("Invalid value")


builder = StateGraph(MyState)
# 节点添加重试策略
builder.add_node(node_1, retry_policy=RetryPolicy(
    max_attempts=3,
    retry_on=ValueError
))
builder.add_edge(START, node_1.__name__)
builder.add_edge(node_1.__name__, END)
graph = builder.compile()

print(graph.invoke({"my_state_value": "b"}))
