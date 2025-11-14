"""
多代理架构:supervisor，各个代理由中央主管代理协调。主管控制所有通信流程和任务委托，并根据当前上下文和任务需求决定调用哪个代理。
pip install langgraph-supervisor
"""
from pprint import pprint

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor


def book_hotel(hotel_name: str):
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."

def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."

# 定义agent
hotel_assistant = create_react_agent(
    model="deepseek:deepseek-chat",
    tools=[book_hotel],
    prompt="You are a hotel booking assistant",
    name="hotel_assistant"
)
flight_assistant = create_react_agent(
    model="deepseek:deepseek-chat",
    tools=[book_flight],
    prompt="You are a flight booking assistant",
    name="flight_assistant"
)

supervisor = create_supervisor(
    agents=[hotel_assistant, flight_assistant],
    model=init_chat_model("deepseek:deepseek-chat"),
    prompt=(
        "You manage a hotel booking assistant and a"
        "flight booking assistant. Assign work to them."
    )
).compile()

for chunk in supervisor.stream({
    "messages":[{"role": "user", "content": "预定一张机票从北京到上海，并预定一家酒店。"}]
}):
    pprint(chunk)
    print("\n")


