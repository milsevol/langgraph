"""
人机交互，暂停以等待人工输入。恢复时，附加人工输入。
"""
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import task, entrypoint
from langgraph.types import interrupt, Command


@task
def step_1(query):
    return f"{query} bar"

@task
def human_feedback(query):
    feedback = interrupt(f"please provide feedback: {query}")
    return f"{query} {feedback}"

@task
def step_3(query):
    return f"{query} qux"

@entrypoint(checkpointer=InMemorySaver())
def graph(query: str):
    result_1 = step_1(query).result()
    result_2 = human_feedback(result_1).result()
    result_3 = step_3(result_2).result()
    return result_3

config = {"configurable": {"thread_id": "1"}}

for chunk in graph.stream("foo", config):
    print(chunk)
    print("\n")

# 模拟人工输入
for event in graph.stream(Command(resume="baz"), config):
    print(event)
    print("\n")
