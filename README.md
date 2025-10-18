# Research Agent

A sophisticated LangGraph-based research agent that generates AI analyst personas, conducts parallel interviews using web search and Wikipedia, and produces comprehensive research reports.

![Research Agent Workflow](research_graph.png)

## 🚀 Features

* **Dynamic Analyst Generation**: Creates multiple AI analyst personas based on research topics
* **Parallel Interviews**: Conducts simultaneous interviews across different perspectives
* **Multi-Source Research**: Combines web search (Tavily) and Wikipedia for comprehensive coverage
* **Human-in-the-Loop**: Allows feedback on generated analysts before proceeding
* **Automated Report Writing**: Generates structured reports with introduction, insights, and conclusion
* **Production-Ready**: Modular architecture with logging and state management

## 🏗️ Architecture

```
Researcher/
├── config.py                 # Configuration management
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── graph/                    # Graph components
│   ├── __init__.py
│   ├── state.py              # State definitions (TypedDict)
│   ├── models.py             # Pydantic models
│   ├── graph.py              # Graph construction
│   ├── routers.py            # Conditional edge routers
│   ├── logging_config.py     # Logging configuration
│   ├── chains/               # LLM chain components
│   │   ├── __init__.py
│   │   ├── llm.py            # LLM initialization
│   │   └── prompts.py        # Prompt templates
│   └── nodes/                # Graph node functions
│       ├── __init__.py
│       ├── analyst_nodes.py  # Analyst generation nodes
│       ├── interview_nodes.py # Interview conducting nodes
│       └── report_nodes.py   # Report writing nodes
└── tests/                    # Test suite
    ├── __init__.py
    ├── test_models.py        # Model tests
    └── test_nodes.py         # Node tests
```

## 🔧 Configuration

Create a `.env` file with the following variables:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional - LangSmith Tracing
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_project_name

# Optional - Defaults provided
MODEL_NAME=gemini-2.0-flash-lite
WEB_SEARCH_MAX_RESULTS=3
WIKIPEDIA_MAX_DOCS=2
MAX_INTERVIEW_TURNS=2
LOG_LEVEL=INFO
```

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or using uv
uv pip install -r requirements.txt
```

## 🚀 Usage

```bash
python main.py
```

The agent will:
1. Generate analyst personas based on the topic
2. Pause for human feedback (optional)
3. Conduct parallel interviews
4. Generate a comprehensive research report
5. Save the report to `research_report.md`

## 🔍 Workflow

### 1. Analyst Generation
- Analyzes research topic
- Creates diverse analyst personas with different perspectives
- Allows human feedback for refinement

### 2. Parallel Interviews
- Each analyst conducts an interview with an AI expert
- Uses web search and Wikipedia for sourcing information
- Automatically routes between questions and answers

### 3. Report Synthesis
- Writes individual sections from each interview
- Synthesizes insights into a coherent report
- Generates introduction and conclusion
- Compiles sources

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=graph --cov-report=html

# Run specific test file
pytest tests/test_models.py -v
```

## 📊 Graph Visualizations

The system generates PNG visualizations:
- `analyst_graph.png` - Analyst generation workflow
- `interview_graph.png` - Interview sub-graph
- `research_graph.png` - Complete research workflow

## 🛡️ Error Handling

- Comprehensive logging throughout the workflow
- Graceful handling of API failures
- State management with checkpointing
- Input validation

## 📄 License

MIT

## 🙏 Acknowledgments

- LangGraph for the workflow framework
- LangChain for LLM integration
- Google Gemini for the language model
- Tavily for web search capabilities
