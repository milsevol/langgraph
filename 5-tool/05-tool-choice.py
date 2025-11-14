"""
强制使用工具
"""
from pprint import pprint

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool(return_direct=True)
def greet(user_name: str) -> str:
    """Greet the user by name."""
    return f"Hello {user_name}!"

tools = [greet]
llm = init_chat_model("deepseek:deepseek-chat")
llm_with_tools = llm.bind_tools(tools, tool_choice="greet")
# llm_with_tools = llm.bind_tools(tools)

agent = create_react_agent(model=llm_with_tools, tools=tools)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi, I am Bob"}]}
)
pprint(result)
