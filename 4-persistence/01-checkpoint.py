"""
LangGraph 内置了持久层，通过检查点实现。检查点会checkpoint在每个超级步骤中保存图状态的副本。这些检查点保存到 中thread，可在图执行后访问。
线程在特定时间点的状态称为检查点。检查点是在每个超级步骤中保存的图状态的快照，
由StateSnapshot具有以下关键属性的对象表示：
- config：与此检查点相关的配置。
- metadata：与此检查点相关的元数据。
- values：此时状态通道的值。
- next 图中接下来要执行的节点名称的元组。
- tasks PregelTask：包含后续待执行任务信息的对象元组。
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

config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"foo": ""}, config)
print(result)

print("\n---最新检查点---")
print(graph.get_state(config))

print("\n---根据检查点ID获取检查点快照---")
checkpoint_id = graph.get_state(config).config["configurable"]["checkpoint_id"]
check_config = {"configurable": {"thread_id": "1", "checkpoint_id": checkpoint_id}}
print(graph.get_state(check_config))

print("\n---获取状态历史记录---")
state_history_list = list(graph.get_state_history(config))
pprint(state_history_list)

print("\n---重播,获取状态历史记录---")
state_snapshot = state_history_list[2]
state_checkpoint_id = state_snapshot.config["configurable"]["checkpoint_id"]
state_config = {"configurable": {"thread_id": "1", "checkpoint_id": state_checkpoint_id}}
graph.invoke(None, config=state_config)
history_list = list(graph.get_state_history(config))
pprint(history_list)