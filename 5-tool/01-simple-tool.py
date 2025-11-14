"""
简单使用工具示例
"""
from pprint import pprint

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


@tool
def multiple(a:int, b: int) -> int:
    """计算两个数字的乘积"""
    return a * b

agent = create_react_agent(model=init_chat_model("deepseek:deepseek-chat"), tools=[multiple])

response = agent.invoke({"messages":[{"role": "user", "content": "计算41乘以2"}]})
pprint(response)
