"""
Functional API 使用两个关键构建块：
1、@entrypoint
    将某个函数标记为工作流的起点，封装逻辑并管理执行流程，包括处理长时间运行的任务和中断。
2、@task
    表示一个独立的工作单元，例如 API 调用或数据处理步骤，可以在入口点内异步执行。
    任务返回一个类似 Future 的对象，可以等待或同步执行。

创建简单的工作流程
"""
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import task, entrypoint


@task
def is_even(number: int) -> bool:
    return number % 2 == 0

@task
def format_msg(is_even: bool):
    return "number is even" if is_even else "number is odd"

checkpointer = InMemorySaver()

@entrypoint(Checkpointer=checkpointer)
def workflow(inputs: dict):
    event = is_even(inputs["number"]).result()
    return format_msg(event)


result = workflow.invoke({"number": 2})
print(result.result())