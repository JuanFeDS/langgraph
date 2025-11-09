"""simple.py"""
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState

class State(MessagesState):
    """State of the agent"""
    customer_name: str | None = None
    customer_age: int | None = None

def node_1(state: State):
    """Node 1"""
    history = state['messages']

    if state.get('customer_name') is None:
        ai_msg = AIMessage(
            content = "Hola, podrias decirme tu nombre y edad para asistirte mejor?"
        )
        return {
            "messages": [ai_msg]
        }
    else:
        ai_msg = AIMessage(
            content=f'Hola, {state['customer_name']}! cómo puedo ayudarte hoy?'
        )
        return {
            "messages": [ai_msg]
        }

# Build the agent
builder = StateGraph(State)
builder.add_node('node_1', node_1)

builder.add_edge(START, 'node_1')
builder.add_edge('node_1', END)

agent = builder.compile()
