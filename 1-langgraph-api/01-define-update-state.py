"""
定义和更新State
"""
from typing import TypedDict
from pathlib import Path
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph

"""
定义状态 三种方式：
1-TypedDict: 适合简单场景，不需要验证或默认值
2-Pydantic: 提供数据验证、序列化、默认值等功能, 适合复杂场景，需要数据验证
3-dataclass: 提供简洁的类定义语法, 适合中等复杂度场景
"""
# 方式1
class MyState(TypedDict):
    extra_filed: int
    messages: list[AnyMessage]
# 方式2
# class MyState(BaseModel):
#     extra_filed: int
#     messages: list[AnyMessage]
# 方式3
# @dataclass
# class MyState:
#     extra_filed: int
#     messages: list[AnyMessage]

# 更新状态
def update_node(state: MyState):
    messages = state["messages"]
    new_message = AIMessage(content="Hello, world!")
    return {"messages": messages + [new_message], "extra_filed": 1}

# 定义简单图
graph_builder = StateGraph(MyState)
graph_builder.add_node("node1", update_node)
graph_builder.set_entry_point("node1")
graph = graph_builder.compile()

# 运行图
result = graph.invoke({"messages": [HumanMessage(content="Hi")], "extra_filed": 0})
for message in result["messages"]:
    message.pretty_print()

# 绘制图
output_file_path = '../data/image/langgraph-api/01-define-update-state.png'
Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)
graph.get_graph().draw_mermaid_png(output_file_path=output_file_path)