"""Configuration management for the research agent."""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash-lite")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LangSmith Tracing (Optional)
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

# Search Configuration
WEB_SEARCH_MAX_RESULTS = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "3"))
WIKIPEDIA_MAX_DOCS = int(os.getenv("WIKIPEDIA_MAX_DOCS", "2"))

# Interview Configuration
MAX_INTERVIEW_TURNS = int(os.getenv("MAX_INTERVIEW_TURNS", "2"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validation
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY environment variable is required")

