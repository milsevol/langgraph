"""
更新图表状态
"""
import operator
from pprint import pprint
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

class MyState(TypedDict):
    foo: str
    bar: Annotated[list[str], operator.add]

config = {"configurable": {"thread_id": "1"}}

def node_a(state: MyState):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: MyState):
    return {"foo": "b", "bar": ["b"]}

graph = (
    StateGraph(MyState)
    .add_node(node_a)
    .add_node(node_b)
    .add_edge(START, node_a.__name__)
    .add_edge(node_a.__name__, node_b.__name__)
    .add_edge(node_b.__name__, END)
    .compile(checkpointer=InMemorySaver())
)

result = graph.invoke({"foo": ""}, config)
print("\n---执行结果---")
print(result)

print("\n---更新结果---")
update_result = graph.update_state(config=config, values={"foo": "c", "bar": ["c"]})

print("\n---获取状态历史记录---")
state_history_list = list(graph.get_state_history(config))
pprint(state_history_list)