"""
添加运行时配置:
1、定义配置类
2、节点新增参数Runtime[配置类]
3、StateGraph新增参数context_schema指定配置类
"""
from typing import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

# 方式1： Runtime[ContextSchema]
# Specify config schema
class ContextSchema(TypedDict):
    my_runtime_value: str

class MyState(TypedDict):
    my_state_value: str

def node_1(state: MyState, runtime: Runtime[ContextSchema]):
    if runtime.context["my_runtime_value"] == "a":
        return {"my_state_value": "a"}
    elif runtime.context["my_runtime_value"] == "b":
        return {"my_state_value": "b"}
    else:
        raise ValueError("Invalid value")

# 指定context_schema类
builder = StateGraph(MyState, context_schema=ContextSchema)
builder.add_node(node_1)
builder.add_edge(START, node_1.__name__)
builder.add_edge(node_1.__name__, END)
graph = builder.compile()

print(graph.invoke({}, context={"my_runtime_value": "a"}))
print(graph.invoke({}, context={"my_runtime_value": "b"}))


# 方式2：RunnableConfig
def node_2(state: MyState, config: RunnableConfig):
    my_runtime_value = config["configurable"]["my_runtime_value"]
    if my_runtime_value == "a":
        return {"my_state_value": "a"}
    elif my_runtime_value == "b":
        return {"my_state_value": "b"}
    else:
        raise ValueError("Invalid value")

builder1 = StateGraph(MyState)
builder1.add_node(node_2)
builder1.add_edge(START, node_2.__name__)
builder1.add_edge(node_2.__name__, END)
graph1 = builder1.compile()

print("\n---graph1----")
print(graph1.invoke({},  {"configurable": {"my_runtime_value": "a"}}))
print(graph1.invoke({},  {"configurable": {"my_runtime_value": "b"}}))
