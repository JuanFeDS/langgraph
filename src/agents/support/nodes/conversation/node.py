"""conversation/node.py"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from agents.support.state import State
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT
from agents.support.nodes.conversation.tools import tools

load_dotenv()

model = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)

model = model.bind_tools(tools)

def conversation(state: State):
    """Conversation node
    
    Args:
        state (State): State of the agent
    """
    new_state = {}
    history = state['messages']

    if history == []:
        ai_message = model.invoke([("system", SYSTEM_PROMPT)])
    else:
        ai_message = model.invoke([("system", SYSTEM_PROMPT)] + history[-3:])

    new_state["messages"] = [ai_message]

    return new_state
