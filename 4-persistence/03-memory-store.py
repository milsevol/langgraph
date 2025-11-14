"""
跨线程共享信息，通过共享缓存store接口实现。
"""
from pprint import pprint

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.store.base import BaseStore, IndexConfig
from langgraph.store.memory import InMemoryStore
from langchain_ollama import OllamaEmbeddings

in_memory_store = InMemoryStore(index=IndexConfig(embed=OllamaEmbeddings(model='bge-m3'), dims=1024))
llm = init_chat_model(model="deepseek:deepseek-chat")

def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config["configurable"]["user_id"]
    # 记忆的命名空间为tuple
    namespace = ("memories", user_id)

    # 构建系统提示，包含用户记忆信息
    message_list = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    cache = store.get(namespace=namespace, key=str(user_id))
    cache_messages = []
    if cache:
        cache_messages = store.get(namespace=namespace, key=str(user_id)).value["data_list"]
        message_list.extend(cache_messages)

    # 当前对话
    curr_msg = {"role": "user", "content": state["messages"][-1].content}
    message_list.append(curr_msg)

    response = llm.invoke(message_list)

    # 缓存消息
    cache_messages.append(curr_msg)
    cache_messages.append({"role": "ai", "content": response.content})
    store.put(namespace, str(user_id), {"data_list": cache_messages})

    return {"messages": response}


builder = StateGraph(MessagesState)
builder.add_node(call_model)
builder.add_edge(START, call_model.__name__)
# 配置检查点，使用配置的内存存储
graph = builder.compile(
    checkpointer=MemorySaver(),
    store=in_memory_store,
)

config = {"configurable": {"thread_id": "1", "user_id": "1"}}
print("第一次对话:")
response = graph.invoke({"messages": [HumanMessage(content="Hi! my name is Kenney")]}, config=config)
pprint(response)

# 查看存储的记忆
print("\n存储的记忆内容:")
# 记忆的命名空间为tuple
namespace = ("memories", config["configurable"]["user_id"])
for memory in in_memory_store.search(namespace):
    print(memory.value)

# 测试场景2：读取记忆
config_2 = {"configurable": {"thread_id": "3", "user_id": "1"}}  # 用户2的对话配置
response2 = graph.invoke({"messages": [HumanMessage(content="what is my name?")]}, config=config_2)
pprint(response2)
