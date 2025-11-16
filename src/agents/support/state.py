"""state.py"""
from langgraph.graph import MessagesState

class State(MessagesState):
    """State of the agent"""
    customer_name: str | None = None
    customer_age: int | None = None
    customer_email: str | None = None
    customer_phone: int | None = None
    customer_sentiment: str | None = None
    customer_nationality: str | None = None
