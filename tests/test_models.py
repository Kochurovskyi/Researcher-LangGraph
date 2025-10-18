"""Unit tests for models."""
import pytest
from graph.models import Analyst, SearchQuery, Perspectives


def test_analyst_creation():
    """Test creating an Analyst instance."""
    analyst = Analyst(
        affiliation="University",
        name="Dr. Smith",
        role="Research Scientist",
        description="Expert in AI research"
    )
    assert analyst.name == "Dr. Smith"
    assert analyst.role == "Research Scientist"


def test_analyst_persona():
    """Test analyst persona property."""
    analyst = Analyst(
        affiliation="University",
        name="Dr. Smith",
        role="Research Scientist",
        description="Expert in AI research"
    )
    persona = analyst.persona
    assert "Dr. Smith" in persona
    assert "Research Scientist" in persona
    assert "University" in persona


def test_search_query():
    """Test SearchQuery model."""
    query = SearchQuery(search_query="test query")
    assert query.search_query == "test query"


def test_perspectives():
    """Test Perspectives model."""
    analyst = Analyst(
        affiliation="University",
        name="Dr. Smith",
        role="Research Scientist",
        description="Expert in AI research"
    )
    perspectives = Perspectives(analysts=[analyst])
    assert len(perspectives.analysts) == 1
    assert perspectives.analysts[0].name == "Dr. Smith"

