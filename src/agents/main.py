"""03 Hello Langchain"""
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

def get_weather(city: str) -> str:
    '''Devuelve el clima de una ciudad'''

    return f'El clima de {city} es soleado'

agent = create_agent(
    model = 'openai:gpt-4o-mini',
    tools = [get_weather],
    prompt = 'Eres un asistente útil y amigable'
)
