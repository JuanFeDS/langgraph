"""conversation/tools.py"""
import os
from dotenv import load_dotenv

load_dotenv()

RAG_PAPELERIA = os.getenv("OPENAI_RAG_ID_PAPELERIA")

file_search_tool = {
    "type": "file_search",
    "vector_store_ids": [RAG_PAPELERIA]
}

tools = [file_search_tool]