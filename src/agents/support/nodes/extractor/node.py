"""extractor/node.py"""
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from agents.support.state import State
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Schema
class ContactInfo(BaseModel):
    """Contact information"""
    name: str = Field(description="Name of the contact")
    email: str = Field(description="Email of the contact")
    phone: int = Field(description="Phone number of the contact")
    age: int = Field(description="Age of the contact")
    sentiment: str = Field(description="Sentiment of the conversation")
    nationality: str = Field(description="Nationality of the contact")

# Initialize LLM
model = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)
llm_schema = model.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    """Extractor node
    
    Args:
        state (State): State of the agent
    """
    history = state['messages']
    customer_name = state.get("customer_name", None)

    new_state: State = {}

    if customer_name is None:
        schema = llm_schema.invoke([("system", SYSTEM_PROMPT)] + history[-3:])
        new_state["customer_name"] = schema.name
        new_state["customer_age"] = schema.age
        new_state["customer_email"] = schema.email
        new_state["customer_phone"] = schema.phone
        new_state["customer_sentiment"] = schema.sentiment
        new_state["customer_nationality"] = schema.nationality

    return new_state
