"""simple.py"""
import os
import random
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END, MessagesState

load_dotenv()
RAG_PAPELERIA = os.getenv("OPENAI_RAG_ID_PAPELERIA")

file_search_tool = {
    "type": "file_search",
    "vector_store_ids": [RAG_PAPELERIA]
}

llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=1
)
llm = llm.bind_tools([file_search_tool])

class State(MessagesState):
    """State of the agent"""
    customer_name: str | None = None
    customer_age: int | None = None

def node_1(state: State):
    """Node 1"""
    new_state: State = {}

    if state.get("customer_name") is None:
        new_state["customer_name"] = "Juan"
    else:
        new_state["customer_age"] = random.randint(20, 70)

    history = state['messages']

    if history == []:
        ai_message = llm.invoke('')
    else:
        ai_message = llm.invoke(history[-3:])

    new_state["messages"] = [ai_message]

    return new_state

# Build the agent
builder = StateGraph(State)
builder.add_node('node_1', node_1)

builder.add_edge(START, 'node_1')
builder.add_edge('node_1', END)

agent = builder.compile()
