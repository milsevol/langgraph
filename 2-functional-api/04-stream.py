"""
Stream流
"""
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer
from langgraph.func import entrypoint

checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: dict):
    writer = get_stream_writer()
    # stream_mode=["custom"]才能接收自定义消息
    writer("started processing")
    result = inputs["x"] * 2
    writer(f"result is {result}")
    return result


config = {"configurable": {"thread_id": "abc"}}

for mode, chunk in workflow.stream({"x": 5},
                                   stream_mode=["custom", "updates"],
                                   config=config):
    print(f"{mode}:{chunk}")
