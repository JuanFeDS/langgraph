"""03 Hello Langchain"""
from dotenv import load_dotenv
from langchain.agents import create_agent

from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import prompt_template

load_dotenv()


booking_node = create_agent(
    model = 'openai:gpt-4o-mini',
    tools = tools,
    prompt = prompt_template
)
