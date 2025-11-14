"""
高级工具功能：立即返回
"""
from pprint import pprint

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def add(a: int, b: int) -> int:
    """返回两个数字的和"""
    return a + b

@tool(return_direct=True)
def add_direct(a: int, b: int) -> int:
    """返回两个数字的和"""
    return a + b

pprint("---add---")
agent = create_react_agent(model=init_chat_model("deepseek:deepseek-chat"), tools=[add])
result = agent.invoke({"messages": [{"role": "user", "content": "计算1加2"}]})
pprint(result)

pprint("\n---add_direct---")
agent = create_react_agent(model=init_chat_model("deepseek:deepseek-chat"), tools=[add_direct])
result = agent.invoke({"messages": [{"role": "user", "content": "计算1加2"}]})
pprint(result)