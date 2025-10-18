"""Router functions for conditional edges."""
from langgraph.graph import END
from graph.state import GenerateAnalystsState, ResearchGraphState
from graph.logging_config import logger


def should_continue_analyst_generation(state: GenerateAnalystsState):
    """Determine next node after analyst generation."""
    human_analyst_feedback = state.get('human_analyst_feedback', None)
    
    if human_analyst_feedback:
        logger.info("Human feedback provided, regenerating analysts")
        return "create_analysts"
    
    logger.info("No feedback, completing analyst generation")
    return END


def should_continue_research(state: ResearchGraphState):
    """Determine if research should continue or restart analyst creation."""
    human_analyst_feedback = state.get('human_analyst_feedback')
    
    if human_analyst_feedback:
        logger.info("Human feedback provided, returning to analyst creation")
        return "create_analysts"
    
    logger.info("Proceeding with interviews")
    return "conduct_interview"

