"""
通过断点，实现人工审阅和编辑状态
"""
import uuid
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command


class State(TypedDict):
    summary: str

def generate_summary(state: State) -> State:
    return {"summary": "The cat sat on the mat and looked at the stars."}

def human_review(state: State) -> State:
    result = interrupt({
        "task": "Please review and edit the generated summary if necessary.",
        "generate_summary": state["summary"]
    })
    return {"summary": result["edited_summary"]}

def downstream_use(state: State) -> State:
    print(f"✅ Using edited summary: {state['summary']}")
    return state

builder = StateGraph(State)
builder.add_node(generate_summary)
builder.add_node(human_review)
builder.add_node(downstream_use)

builder.add_edge(START, generate_summary.__name__)
builder.add_edge(generate_summary.__name__, human_review.__name__)
builder.add_edge(human_review.__name__, downstream_use.__name__)
builder.add_edge(downstream_use.__name__, END)
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({}, config=config)
print(result)

edit_summary =  "The cat lay on the rug, gazing peacefully at the night sky."
resumed_result = graph.invoke(Command(resume={"edited_summary": edit_summary}), config=config)
print("\n", resumed_result)
