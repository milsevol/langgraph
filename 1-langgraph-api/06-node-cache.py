"""
添加节点缓存
"""
from typing import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy

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
# 添加节点缓存
builder.add_node(node_1, cache_policy=CachePolicy(ttl=120))
builder.add_edge(START, node_1.__name__)
builder.add_edge(node_1.__name__, END)
# 图添加缓存类型
graph = builder.compile(cache=InMemoryCache())

print(graph.invoke({"my_state_value": "a"}))
# 第二次运行没有打印节点执行日志，因此节点缓存生效了
print(graph.invoke({"my_state_value": "a"}))
