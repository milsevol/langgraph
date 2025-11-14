"""
工具调用
"""
from pprint import pprint

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, ToolCall, HumanMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degrees and foggy."
    else:
        return "It's 90 degrees and sunny."

def get_coolest_cities():
    """Get a list of coolest cities"""
    return "nyc, sf"

llm = init_chat_model("deepseek:deepseek-chat")

# 工具执行
print("\n----工具执行----")
tool_node = ToolNode([get_weather, get_coolest_cities])
messages = AIMessage(
    content="",
    tool_calls=[
        ToolCall(id="tool_call_id_1", name=get_coolest_cities.__name__, args={}, type="tool_call"),
        # ToolCall(id="tool_call_id_2", name=get_weather.__name__, args={"location": "sf"}, type="tool_call")
    ]
)
print(tool_node.invoke({"messages": [messages]}))

# 工具与LLM一起使用
print("\n----工具与LLM一起使用----")
tool_node_1 = ToolNode([get_weather])
llm_with_tool = llm.bind_tools([get_weather])

result = llm_with_tool.invoke("what's the weather in sf?")
pprint(result)
# 工具执行
tool_result = tool_node_1.invoke({"messages": [result]})
pprint(tool_result)
print("----工具结果----")
for tool_message in tool_result["messages"]:
    pprint(tool_message.content)


# 图中使用工具
print("\n----图中使用工具----")
tool_node_2 = ToolNode([get_weather])
llm_with_tool_2 = llm.bind_tools([get_weather])

def call_mode(state: MessagesState):
    response = llm_with_tool_2.invoke(state["messages"])
    return {"messages": [response]}

def continue_node(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    else:
        return END


builder = StateGraph(MessagesState)
builder.add_node(call_mode)
builder.add_node("tools", tool_node_2)
builder.add_edge(START, call_mode.__name__)
builder.add_conditional_edges(call_mode.__name__, continue_node, ["tools", END])
builder.add_edge("tools", call_mode.__name__)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path='../data/image/tool/03-tool-invoke.png')

graph_result = graph.invoke({"messages": [HumanMessage(content="what's the weather in sf?")]})
pprint(graph_result)
