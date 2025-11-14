"""
子图是指一个图被用作另一个图的节点
如果主图和子图的状态消息不一致，调用前需要进行转换
"""
import uuid
from pprint import pprint
from typing import TypedDict, Annotated

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph, MessagesState


class SubGraphState(TypedDict):
    subgraph_messages: Annotated[list[AnyMessage], add_messages]


llm = init_chat_model(model="deepseek:deepseek-chat", temperature=0)


def call_model(subgraph_state: SubGraphState):
    response = llm.invoke(subgraph_state["subgraph_messages"])
    return {"subgraph_messages": [response]}

subgraph_builder = StateGraph(SubGraphState)
subgraph_builder.add_node(call_model)
subgraph_builder.add_edge(START, call_model.__name__)
subgraph = subgraph_builder.compile()

def call_subgraph(state: MessagesState):
    result = subgraph.invoke({"subgraph_messages": state["messages"]})
    return {"messages": result["subgraph_messages"]}

builder = StateGraph(MessagesState)
builder.add_node(call_subgraph)
builder.add_edge(START, call_subgraph.__name__)
builder.add_edge(call_subgraph.__name__, END)
# 主图编译添加了检查点，会自动传递给子图，子图编译也可以定义子图的单独检查点
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": uuid.uuid4()}}
graph.get_graph().draw_mermaid_png(output_file_path="../data/image/subgraph/01-subgraph.png")

result = graph.invoke({"messages": [{"role": "user", "content": "hello"}]}, config=config)
print(result)

state_history = list(graph.get_state_history(config))
pprint(state_history)

