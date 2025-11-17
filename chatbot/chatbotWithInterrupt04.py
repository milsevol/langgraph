import os
from typing import Annotated

from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langgraph.types import Command, interrupt

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
llm = init_chat_model(
    "deepseek:deepseek-chat",
    api_key=deepseek_key,
)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"] 
@tool
def get_weather(location: str):
    """获取指定城市当前天气的简要描述"""
    if location.lower() in ["sf", "san francisco", "旧金山"]:
        return "旧金山今天多雾，气温约15℃。"
    elif location.lower() in ["beijing", "北京"]:
        return "北京晴，最高气温22℃，夜间有微风。"
    elif location.lower() in ["shanghai", "上海"]:
        return "上海多云，最高气温24℃，适合外出。"
    else:
        return "暂时无法获取该城市的天气，请换一个地点。"

tools = [get_weather, human_assistance]
llm_with_tools = llm.bind_tools(tools)  

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?" 
config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)   

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()


