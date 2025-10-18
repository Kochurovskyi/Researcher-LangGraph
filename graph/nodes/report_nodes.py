"""Node functions for report writing."""
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Send
from graph.state import ResearchGraphState
from graph.chains.llm import llm
from graph.chains.prompts import (
    REPORT_WRITER_INSTRUCTIONS,
    INTRO_CONCLUSION_INSTRUCTIONS
)
from graph.logging_config import logger


def initiate_all_interviews(state: ResearchGraphState):
    """Map step to run each interview sub-graph using Send API."""
    logger.info("Initiating all interviews")
    
    # Check if human feedback
    human_analyst_feedback = state.get('human_analyst_feedback')
    if human_analyst_feedback:
        logger.info("Human feedback provided, returning to create_analysts")
        return "create_analysts"
    
    # Kick off interviews in parallel via Send() API
    topic = state["topic"]
    logger.info(f"Starting {len(state['analysts'])} parallel interviews")
    return [
        Send("conduct_interview", {
            "analyst": analyst,
            "messages": [HumanMessage(content=f"So you said you were writing an article on {topic}?")]
        }) 
        for analyst in state["analysts"]
    ]


def write_report(state: ResearchGraphState):
    """Write the main report content."""
    logger.info("Writing main report")
    sections = state["sections"]
    topic = state["topic"]
    
    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    system_message = REPORT_WRITER_INSTRUCTIONS.format(topic=topic, context=formatted_str_sections)
    report = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Write a report based upon these memos.")
    ])
    
    logger.info(f"Main report written, length: {len(report.content)} characters")
    return {"content": report.content}


def write_introduction(state: ResearchGraphState):
    """Write the report introduction."""
    logger.info("Writing introduction")
    sections = state["sections"]
    topic = state["topic"]
    
    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Write introduction
    instructions = INTRO_CONCLUSION_INSTRUCTIONS.format(
        topic=topic, 
        formatted_str_sections=formatted_str_sections
    )
    intro = llm.invoke([
        instructions,
        HumanMessage(content="Write the report introduction")
    ])
    
    logger.info(f"Introduction written, length: {len(intro.content)} characters")
    return {"introduction": intro.content}


def write_conclusion(state: ResearchGraphState):
    """Write the report conclusion."""
    logger.info("Writing conclusion")
    sections = state["sections"]
    topic = state["topic"]
    
    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Write conclusion
    instructions = INTRO_CONCLUSION_INSTRUCTIONS.format(
        topic=topic, 
        formatted_str_sections=formatted_str_sections
    )
    conclusion = llm.invoke([
        instructions,
        HumanMessage(content="Write the report conclusion")
    ])
    
    logger.info(f"Conclusion written, length: {len(conclusion.content)} characters")
    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchGraphState):
    """Finalize and assemble the complete report."""
    logger.info("Finalizing report")
    content = state["content"]
    
    # Clean up content
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    
    # Split out sources if present
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None
    
    # Assemble final report
    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    
    logger.info(f"Report finalized, total length: {len(final_report)} characters")
    return {"final_report": final_report}

