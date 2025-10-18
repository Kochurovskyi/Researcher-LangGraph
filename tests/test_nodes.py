"""Unit tests for node functions."""
import pytest
from unittest.mock import Mock, patch
from graph.state import GenerateAnalystsState, InterviewState
from graph.models import Analyst
from graph.nodes.analyst_nodes import create_analysts


@pytest.fixture
def sample_analyst():
    """Create a sample analyst for testing."""
    return Analyst(
        affiliation="University",
        name="Dr. Smith",
        role="Research Scientist",
        description="Expert in AI research"
    )


@pytest.fixture
def sample_analyst_state():
    """Create a sample GenerateAnalystsState for testing."""
    return GenerateAnalystsState(
        topic="AI Research",
        max_analysts=3,
        human_analyst_feedback="",
        analysts=[]
    )


def test_analyst_state_structure(sample_analyst_state):
    """Test GenerateAnalystsState structure."""
    assert sample_analyst_state["topic"] == "AI Research"
    assert sample_analyst_state["max_analysts"] == 3
    assert isinstance(sample_analyst_state["analysts"], list)

