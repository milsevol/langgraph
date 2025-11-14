"""
缓存任务
"""
import time

from langgraph.cache.memory import InMemoryCache
from langgraph.func import task, entrypoint
from langgraph.types import CachePolicy


@task(cache_policy=CachePolicy(ttl=60))
def slow_add(x: int) -> int:
    print("slow_add")
    time.sleep(1)
    return x + 1

@entrypoint(cache=InMemoryCache())
def workflow(inputs: dict) -> dict:
    return {"result": slow_add(inputs["x"]).result()}

for chunk in workflow.stream({"x": 5}, stream_mode="values"):
    print(chunk)

# 第二次执行没有打印节点执行日志
for chunk in workflow.stream({"x": 5}, stream_mode="values"):
    print(chunk)
