"""
通过断点，实现人工批准或拒绝
"""
import uuid
from pprint import pprint
from typing import TypedDict, Literal

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    llm_output: str
    decision: str

def generate_llm_output(state: State):
    return {"llm_output": "This is the generated output."}

def approved_node(state: State) -> State:
    print("✅ Approved path taken.")
    return state

def rejected_node(state: State) -> State:
    print("❌ Rejected path taken.")
    return state

def human_approval(state: State) -> Command[Literal["approved_node", "rejected_node"]]:
    decision = interrupt({
        "question": "Do you approve the following output?",
        "llm_output": state["llm_output"]
    })
    if decision == "approve":
        return Command(goto="approved_node", update={"decision": "approved"})
    else:
        return Command(goto="rejected_node", update={"decision": "rejected"})


builder = StateGraph(State)
builder.add_node(generate_llm_output)
builder.add_node(approved_node)
builder.add_node(rejected_node)
builder.add_node(human_approval)

builder.add_edge(START, generate_llm_output.__name__)
builder.add_edge(generate_llm_output.__name__, human_approval.__name__)
builder.add_edge(approved_node.__name__, END)
builder.add_edge(rejected_node.__name__, END)

graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": uuid.uuid4()}}

result = graph.invoke({}, config)
print(result)

print("\n---获取状态历史记录---")
state_history_list = list(graph.get_state_history(config))
pprint(state_history_list)

print("\n---断点执行结果---")
final_output = graph.invoke(Command(resume="rejected"), config=config)
print("\n", final_output)