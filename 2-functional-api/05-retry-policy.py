"""
重试策略
"""
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import RetryPolicy

retry_policy = RetryPolicy(max_attempts=3)

@task(retry_policy=retry_policy)
def get_info():
    print("get info")
    num = 0
    if num < 2:
        raise Exception("num is less than 2")
    return "success"

checkpointer = InMemorySaver()

@entrypoint(checkpointer=checkpointer)
def main(inputs: dict):
    return get_info().result()


config = {
    "configurable": {
        "thread_id": "1"
    }
}
main.invoke({'any_input': 'foobar'}, config=config)
