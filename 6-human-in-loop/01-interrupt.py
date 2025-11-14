"""
动态断点
"""
import uuid
from pprint import pprint
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command


class State(TypedDict):
    some_text: str

def human_node(state: State):
    value = interrupt(
        {"text_to_revise": state["some_text"]}
    )
    return {"some_text": value}


builder = StateGraph(State)
builder.add_node(human_node)
builder.add_edge(START, human_node.__name__)
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({"some_text": "hello"}, config)
pprint(result)
print("\n")
# 图将从最初调用的节点的开头恢复执行
pprint(graph.invoke(Command(resume="Edited text"), config=config))
