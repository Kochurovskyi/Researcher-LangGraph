"""Integration tests for the research agent."""
import pytest
from unittest.mock import Mock, patch
from graph.graph import build_analyst_generation_graph, build_interview_graph, build_research_graph
from graph.models import Analyst


@pytest.fixture
def sample_analyst():
    """Create a sample analyst for testing."""
    return Analyst(
        affiliation="Tech University",
        name="Dr. Test Analyst",
        role="AI Research Specialist",
        description="Expert in analyzing AI trends and patterns"
    )


def test_analyst_generation_graph_builds():
    """Test that the analyst generation graph can be built."""
    graph = build_analyst_generation_graph()
    assert graph is not None
    assert hasattr(graph, 'nodes')


def test_interview_graph_builds():
    """Test that the interview graph can be built."""
    graph = build_interview_graph()
    assert graph is not None
    assert hasattr(graph, 'nodes')


def test_research_graph_builds():
    """Test that the complete research graph can be built."""
    graph = build_research_graph()
    assert graph is not None
    assert hasattr(graph, 'nodes')


@patch('graph.chains.llm.llm')
def test_analyst_generation_flow(mock_llm, sample_analyst):
    """Test the analyst generation flow with mocked LLM."""
    from graph.models import Perspectives
    
    # Mock the LLM response
    mock_structured_llm = Mock()
    mock_structured_llm.invoke.return_value = Perspectives(analysts=[sample_analyst])
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    graph = build_analyst_generation_graph()
    thread = {"configurable": {"thread_id": "test_1"}}
    
    # Run the graph
    initial_state = {
        "topic": "Test Topic",
        "max_analysts": 1,
        "human_analyst_feedback": "",
        "analysts": []
    }
    
    # Stream through analyst creation
    events = list(graph.stream(initial_state, thread, stream_mode="values"))
    
    # Should have created analysts
    assert len(events) > 0


def test_graph_state_persistence():
    """Test that graph state can be retrieved."""
    graph = build_research_graph()
    thread = {"configurable": {"thread_id": "test_persist"}}
    
    # The graph should be able to get state even if empty
    state = graph.get_state(thread)
    assert state is not None

