"""
在LangGraph中使用time-travel恢复执行断点或者重放某个节点
"""
import uuid
from pprint import pprint
from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from typing_extensions import NotRequired

class State(TypedDict):
    topic: NotRequired[str]
    joke: NotRequired[str]

llm = init_chat_model(model="deepseek:deepseek-chat", temperature=0)

def generate_topic(state: State):
    """LLM call to generate a topic for the joke"""
    msg = llm.invoke("给我一个有趣的主题，字数限制20个字")
    return {"topic": msg.content}

def write_joke(state: State):
    """LLM call to write a joke based on the topic"""
    msg = llm.invoke(f"写一个简短的笑话关于主题: {state['topic']}")
    return {"joke": msg.content}


builder = StateGraph(State)
builder.add_node(generate_topic)
builder.add_node(write_joke)

builder.add_edge(START, generate_topic.__name__)
builder.add_edge(generate_topic.__name__, write_joke.__name__)
builder.add_edge(write_joke.__name__, END)

graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": uuid.uuid4()}}

result = graph.invoke({}, config=config)
print("---执行结果----")
pprint(result)

print("\n---节点执行历史记录----")
state_history = list(graph.get_state_history(config=config))
for state in state_history:
    print(state.next)
    print(state.config["configurable"]["checkpoint_id"])
    print()

# 更新状态
selected_start = state_history[1]
print("\n---更新状态---")
new_config = graph.update_state(selected_start.config, {"topic": "小鸡"})
print(new_config)

# 从检查点恢复执行
result = graph.invoke(None, new_config)
print("---更新后的节点快照---")
pprint(graph.get_state(new_config))

print("\n---新的节点执行历史记录----")
new_state_history = list(graph.get_state_history(config=config))
for state in new_state_history:
    print(state.next)
    print(state.config["configurable"]["checkpoint_id"])
    print()
