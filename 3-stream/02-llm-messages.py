"""
messages模式的流输出是一个元组(message_chunk, metadata)，其中：
1、message_chunk：来自 LLM 的标记或消息段。
2、metadata：包含有关图形节点和 LLM 调用的详细信息的字典。
"""
from dataclasses import dataclass

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.constants import START
from langgraph.graph import StateGraph

@dataclass
class MyState:
    topic: str
    joke: str

llm = init_chat_model(model="deepseek:deepseek-chat")

def call_model(state: MyState):
    """call the llm to generate a joke about topic"""
    llm_response = llm.invoke([
        HumanMessage(content=f"Tell me a joke about {state.topic}")
    ])
    return {"joke": llm_response.content}


graph = (
    StateGraph(MyState)
    .add_node(call_model)
    .add_edge(START, call_model.__name__)
    .compile()
)

for message_chunk, metadata in graph.stream({"topic": "ice cream", "joke": ""},
                                            stream_mode="messages"):
    if message_chunk.content:
        print(message_chunk.content, end="", flush=True)
