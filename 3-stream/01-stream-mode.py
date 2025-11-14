"""
多种流模式示例
"""
from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.constants import START,END
from langgraph.graph import StateGraph


class State(TypedDict):
    topic: str
    joke: str

def node_topic(state: State):
    writer = get_stream_writer()
    writer("custom node topic")
    return {"topic": state["topic"] + " and cats"}

def node_joke(state: State):
    return {"joke": f"This is a joke about {state['topic']}"}

graph = (
    StateGraph(State)
    .add_node(node_topic)
    .add_node(node_joke)
    .add_edge(START, node_topic.__name__)
    .add_edge(node_topic.__name__, node_joke.__name__)
    .add_edge(node_joke.__name__, END)
    .compile()
)

print(f"-----stream_mode=['updates']-----")
for chunk in graph.stream({"topic": "ice cream"},
                          stream_mode=["updates"]):
    print(chunk)
    print("\n")

print(f"-----stream_mode=['values']-----")
for chunk in graph.stream({"topic": "ice cream"},
                          stream_mode=["values"]):
    print(chunk)
    print("\n")

print(f"-----stream_mode=['custom']-----")
for chunk in graph.stream({"topic": "ice cream"},
                          stream_mode=["custom"]):
    print(chunk)
    print("\n")

print(f"-----组合模式 stream_mode=['custom', 'updates']-----")
for chunk in graph.stream({"topic": "ice cream"},
                          stream_mode=["custom", "updates"]):
    print(chunk)
    print("\n")

print(f"-----stream_mode=['debug]-----")
for chunk in graph.stream({"topic": "ice cream"},
                          stream_mode=["debug"]):
    print(chunk)
    print("\n")