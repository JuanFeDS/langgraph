"""simple_schema.py"""
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END

# Load environment variables
load_dotenv()
RAG = os.getenv("OPENAI_RAG_ID_PAPELERIA")

# Initialize LLM
model = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)

# Initialize tools
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": [RAG]
}

model = model.bind_tools([file_search_tool])

# Schema
class ContactInfo(BaseModel):
    """Contact information"""
    name: str = Field(description="Name of the contact")
    email: str = Field(description="Email of the contact")
    phone: int = Field(description="Phone number of the contact")
    age: int = Field(description="Age of the contact")
    sentiment: str = Field(description="Sentiment of the conversation")
    nationality: str = Field(description="Nationality of the contact")

llm_schema = model.with_structured_output(schema=ContactInfo)

# State class
class State(MessagesState):
    """State of the agent"""
    customer_name: str | None = None
    customer_age: int | None = None
    customer_email: str | None = None
    customer_phone: int | None = None
    customer_sentiment: str | None = None
    customer_nationality: str | None = None

# Agent nodes
def extractor(state: State):
    """Extractor node
    
    Args:
        state (State): State of the agent
    """
    history = state['messages']

    customer_name = state.get("customer_name", None)

    system_message = '''
        You are a helpful assistant that can extract information from a conversation 
        You return it in a JSON format. 
        You can't make up information that is not in the conversation.
        Do not include any additional information that is not in the conversation.
        In case of missing information, return None.
        If you do not have some of the numeric information, return -2.
        The current year is 2025.
    '''

    new_state = {}

    if customer_name is None:
        schema = llm_schema.invoke([system_message] + history[-3:])
        new_state["customer_name"] = schema.name
        new_state["customer_age"] = schema.age
        new_state["customer_email"] = schema.email
        new_state["customer_phone"] = schema.phone
        new_state["customer_sentiment"] = schema.sentiment
        new_state["customer_nationality"] = schema.nationality

    return new_state

def conversation(state: State):
    """Conversation node
    
    Args:
        state (State): State of the agent
    """
    new_state = {}
    history = state['messages']

    system_message = '''
        You are a helpful assistant that can help the user with their questions.
        Act as a wizard that can answer any question the user has.
    '''
    if history == []:
        ai_message = model.invoke([system_message])
    else:
        ai_message = model.invoke([system_message] + history[-3:])

    new_state["messages"] = [ai_message]

    return new_state

# Build the agent
builder = StateGraph(State)

builder.add_node('extractor', extractor)
builder.add_node('conversation', conversation)

builder.add_edge(START, 'extractor')
builder.add_edge('extractor', 'conversation')
builder.add_edge('conversation', END)

agent = builder.compile()
