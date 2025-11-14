"""
LangGraph使用SendAPI, 发送并且数据到多个节点
"""
import operator
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Send

class OverallState(TypedDict):
    subjects: list[str]
    jokes: Annotated[list[str], operator.add]
    best_selected_joke: str

joke_map = {
    "lions": "Why don't lions like fast food? Because they can't catch it!",
    "elephants": "Why don't elephants use computers? They're afraid of the mouse!",
    "penguins": "Why don't penguins like talking to strangers at parties? Because they find it hard to break the ice."
}

def generate_joke(state: OverallState):
    return {"jokes": [joke_map[state["subject"]]]}
def best_joke(state: OverallState):
    return {"best_selected_joke": "penguins"}
def send_joke(state: OverallState):
    # Send发送数据到指定节点，同一个节点并行执行
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]


builder = StateGraph(OverallState)
builder.add_node(generate_joke)
builder.add_node(best_joke)

builder.add_conditional_edges(START, send_joke, [generate_joke.__name__])
builder.add_edge(generate_joke.__name__, best_joke.__name__)
builder.add_edge(best_joke.__name__, END)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="../data/image/langgraph-api/10-send-api.png")

for step in graph.stream({"subjects": ["lions", "elephants", "penguins"]}):
    print(step)