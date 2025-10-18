"""Node functions for analyst generation."""
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import GenerateAnalystsState, ResearchGraphState
from graph.models import Perspectives
from graph.chains.llm import llm
from graph.chains.prompts import ANALYST_INSTRUCTIONS
from graph.logging_config import logger


def create_analysts(state: GenerateAnalystsState):
    """Create analysts based on topic and feedback."""
    logger.info("Creating analysts")
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')
    
    # Enforce structured output
    structured_llm = llm.with_structured_output(Perspectives)
    
    # System message
    system_message = ANALYST_INSTRUCTIONS.format(
        topic=topic, 
        human_analyst_feedback=human_analyst_feedback, 
        max_analysts=max_analysts
    )
    
    # Generate analysts
    analysts = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Generate the set of analysts.")
    ])
    
    logger.info(f"Created {len(analysts.analysts)} analysts")
    return {"analysts": analysts.analysts}


def create_analysts_for_research(state: ResearchGraphState):
    """Create analysts for the main research graph."""
    logger.info("Creating analysts for research")
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')
    
    # Enforce structured output
    structured_llm = llm.with_structured_output(Perspectives)
    
    # System message
    system_message = ANALYST_INSTRUCTIONS.format(
        topic=topic, 
        human_analyst_feedback=human_analyst_feedback, 
        max_analysts=max_analysts
    )
    
    # Generate analysts
    analysts = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Generate the set of analysts.")
    ])
    
    logger.info(f"Created {len(analysts.analysts)} analysts for research")
    return {"analysts": analysts.analysts}


def human_feedback(state: GenerateAnalystsState):
    """No-op node that should be interrupted on."""
    logger.info("Waiting for human feedback")
    pass


def human_feedback_research(state: ResearchGraphState):
    """No-op node that should be interrupted on for research graph."""
    logger.info("Waiting for human feedback on research")
    pass

