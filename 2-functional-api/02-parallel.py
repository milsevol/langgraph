"""
并行执行
"""
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import task, entrypoint


@task
def add_one(number: int) -> int:
    return number + 1

@entrypoint()
def graph(numbers: list[int]) -> list[str]:
    futures = [add_one(number) for number in numbers]
    return [str(future.result()) for future in futures]

print(graph.invoke([1, 2, 3, 4, 5]))
