"""
动态选择工具
"""
from dataclasses import dataclass
from pprint import pprint
from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.runtime import Runtime

@tool
def weather() -> str:
    """return the current weather conditions"""
    return "It's nice and sunny"

@tool
def compass() -> str:
    """Returns the direction the user is facing."""
    return "North"


@dataclass
class CustomContext:
    tools: list[Literal["weather", "compass"]]

llm = init_chat_model("deepseek:deepseek-chat")

def configure_mode(state: AgentState, runtime: Runtime[CustomContext]):
    """Configure the model with tools based on runtime context."""
    selected_tools = [
        tool for tool in [weather, compass] if tool.name in runtime.context.tools
    ]
    return llm.bind_tools(selected_tools)

agent = create_react_agent(configure_mode, tools=[weather, compass])

output  = agent.invoke({
    "messages": [{"role": "user", "content": "Who are you and what tools do you have access to?"}]
}, context=CustomContext(tools=["compass"]))

pprint(output)
