import os
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.constants import END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pathlib import Path

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
llm = init_chat_model(
    "deepseek:deepseek-chat",
    api_key=deepseek_key,
)

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

tool_node = ToolNode([get_weather])
llm_with_tool = llm.bind_tools([get_weather])

def chatbot(state: State):
    return {"messages": [llm_with_tool.invoke(state["messages"])]}

def continue_node(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    else:
        return END

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", continue_node, ["tools", END])
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input }] }): 
        for value in event.values(): 
            print("Assistant:", value["messages"][-1].content) 

while True:
    try: 
        user_input = input("User: ")  
        if user_input.lower() in ["quit", "exit", "q"]: 
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except: 
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break

