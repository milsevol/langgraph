"""
使用Reducer函数(operator.add)进行State更新
"""
import operator
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph

class MyState(TypedDict):
    extra_filed: int
    messages: Annotated[list[AnyMessage], operator.add]
def update_node(state: MyState):
    new_message = AIMessage(content="Hello, world!")
    # 只返回更新数据，operator.add会自动更新状态数据
    return {"messages": [new_message], "extra_filed": 1}

# 定义简单图
graph_builder = StateGraph(MyState)
graph_builder.add_node("node1", update_node)
graph_builder.set_entry_point("node1")
graph = graph_builder.compile()

# 运行图
result = graph.invoke({"messages": [HumanMessage(content="Hi")]})
for message in result["messages"]:
    message.pretty_print()