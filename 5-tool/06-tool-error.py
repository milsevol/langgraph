"""
工具错误处理
"""
from pprint import pprint

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, create_react_agent


def multiply(a: int, b: int) -> int:
    """multiply two number"""
    if a == 42:
        raise ValueError("The ultimate error")
    return a * b

# 调用工具报错，指定错误信息返回
tool_node = ToolNode([multiply], handle_tool_errors="Cannot use 42 as a first operand!",)

llm = init_chat_model("deepseek:deepseek-chat")
agent = create_react_agent(model=llm, tools=tool_node)

pprint(agent.invoke({"messages": [{"role": "user", "content": "What is 42 * 7?"}]}))
