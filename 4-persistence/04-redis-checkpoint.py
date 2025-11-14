"""
使用Redis作为缓存来持久化MessageState的简单示例。
"""
from typing import Dict, List

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph

# 初始化LLM模型
llm = init_chat_model(model="deepseek:deepseek-chat")

# postgresql缓存
# with PostgresSaver.from_conn_string("postgresql://root:root@192.168.46.128:15432/test") as checkpointer:
# redis缓存
with RedisSaver.from_conn_string("redis://192.168.46.128:26379/0", ttl={"default_ttl": 1}) as checkpointer:
    checkpointer.setup()
    # 定义节点函数
    def chatbot(state: MessagesState, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
        """简单的聊天机器人节点，处理输入消息并返回响应"""
        # 这行代码包含了redis缓存数据和当前提问数据，在1分钟之内再次运行，会获取到之前缓存的数据
        message_list = state["messages"]
        response = llm.invoke(message_list)
        return {"messages": [response]}

    # 创建状态图
    builder = StateGraph(MessagesState)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    graph = builder.compile(checkpointer=checkpointer)

    user_id = "123"
    # 配置对话ID
    config = {"configurable": {"thread_id": user_id}}

    # 首次对话
    print("=== 首次对话 ===")
    input_message = HumanMessage(content="你好，我是小明")
    result = graph.invoke({"messages": [input_message]}, config=config)
    print(f"AI: {result['messages'][-1].content}")

    # 继续对话（使用相同的thread_id恢复状态）
    print("\n=== 继续对话 ===")
    input_message = HumanMessage(content="还记得我的名字吗？")
    result = graph.invoke({"messages": [input_message]}, config=config)
    print(f"AI: {result['messages'][-1].content}")

    # 再次运行， chatbot节点还能获取到之前的对话信息