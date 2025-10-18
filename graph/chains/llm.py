"""LLM initialization and configuration."""
from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

