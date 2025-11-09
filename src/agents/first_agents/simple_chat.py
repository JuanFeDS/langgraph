"""simple.py"""
import json
import re

from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END, MessagesState

load_dotenv()
llm = ChatOpenAI(
    model="gpt-4o-mini"
)

class State(MessagesState):
    """State of the agent"""
    customer_name: str | None = None
    customer_age: int| None = None

def check_info(state: State):
    """Validates if user information is available

    Args:
        state (State): General agent state
    """
    if state.get("customer_name") is None and state.get("customer_age") is None:
        return {
            "next": "ask_info"
        }
    else:
        return {
            "next": "greet"
        }

def ask_info(state: State):
    """Requests personal information from the user

    Args:
        state (State): General agent state

    Returns:
        dict: Dictionary with the user's answer
    """
    ai_msg = AIMessage(
        content = "Hola, puedes decirme tu nombre y edad?"
    )

    hum_msg = HumanMessage(
        content = input('') 
    )

    return {
        "messages": [hum_msg]
    }

def extract_info(state: State):
    """Extracts personal information from the user's message

    Args:
        state (State): General agent state
    """
    last_user_message = None

    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content
            break

    if last_user_message:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
                Extract the user's name and age from their message. 
                Respond in JSON with keys 'customer_name' and 'customer_age'. 
                If unknown, use null.
            """),
            ("human", last_user_message)
        ])

        result = llm.invoke(prompt.format())
        raw = result.content.strip()

        if "```" in raw:
            raw = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "").strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {}

        return data

    return {}

def greet(state: State):
    """Greet the user

    Args:
        state (State): General agent state
    """
    name = state.get("customer_name")
    ai_msg = AIMessage(
        content=f"Hola, {name}!. En qué puedo ayudarte?"
    )

    return {
        "messages": [ai_msg]
    }

# Build the agent
builder = StateGraph(State)

builder.add_node('check_info', check_info)
builder.add_node('ask_info', ask_info)
builder.add_node('extract_info', extract_info)
builder.add_node('greet', greet)

# Edge definitions
builder.add_edge(START, "check_info")

builder.add_conditional_edges(
    "check_info", 
    lambda state: check_info(state)["next"],
    {
        "ask_info": "ask_info",
        "greet": "greet"
    }
)

builder.add_edge("ask_info", "extract_info")
builder.add_edge("extract_info", "greet")
builder.add_edge("greet", END)

agent = builder.compile()
