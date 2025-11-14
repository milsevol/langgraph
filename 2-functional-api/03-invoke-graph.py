"""
由于功能API和图形 API共享相同的底层运行时，因此可以在同一个应用程序中一起使用。
"""
from typing import TypedDict

from langgraph.func import entrypoint
from langgraph.graph import StateGraph


class State(TypedDict):
    foo: int

def double(state: State) -> State:
    return {"foo": state["foo"] * 2}


builder = StateGraph(State)
builder.add_node(double)
builder.set_entry_point(double.__name__)
graph = builder.compile()

@entrypoint()
def workflow(x: int) -> dict:
    result = graph.invoke({"foo": x})
    return {"result": result["foo"]}

print(workflow.invoke(2))
