"""
递归循环限制
"""
import operator
from typing import TypedDict, Annotated, Literal

from langchain_core.runnables import RunnableConfig
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.managed import RemainingSteps

class MyState(TypedDict):
    aggregate: Annotated[list[str], operator.add]
    # 内置的递归循环限制字段
    remaining_steps: RemainingSteps

def a(state: MyState):
    print(f'Node A sees {state["aggregate"]}')
    return {"aggregate": ["A"]}

def b(state: MyState):
    print(f'Node B sees {state["aggregate"]}')
    return {"aggregate": ["B"]}

def route(state: MyState) -> Literal[b.__name__, END]:
    if state["remaining_steps"] <= 2:
        return END
    else:
        return b.__name__

builder = StateGraph(MyState)
builder.add_node(a)
builder.add_node(b)

builder.add_edge(START, a.__name__)
builder.add_conditional_edges(a.__name__, route)
builder.add_edge(b.__name__, a.__name__)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="../data/image/langgraph-api/11-recursion-loop.png")
# recursion_limit设置初始循环次数
print(graph.invoke({"aggregate": []}, config=RunnableConfig(recursion_limit=4)))
