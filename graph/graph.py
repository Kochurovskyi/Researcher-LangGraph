"""Graph construction for the research agent."""
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from graph.state import GenerateAnalystsState, InterviewState, ResearchGraphState
from graph.nodes.analyst_nodes import (
    create_analysts,
    human_feedback,
    create_analysts_for_research,
    human_feedback_research
)
from graph.nodes.interview_nodes import (
    generate_question,
    search_web,
    search_wikipedia,
    generate_answer,
    save_interview,
    write_section,
    route_messages
)
from graph.nodes.report_nodes import (
    initiate_all_interviews,
    write_report,
    write_introduction,
    write_conclusion,
    finalize_report
)
from graph.routers import should_continue_analyst_generation
from graph.logging_config import logger
from config import MAX_INTERVIEW_TURNS


def build_analyst_generation_graph():
    """Build the analyst generation graph."""
    logger.info("Building analyst generation graph")
    
    # Add nodes and edges
    builder = StateGraph(GenerateAnalystsState)
    builder.add_node("create_analysts", create_analysts)
    builder.add_node("human_feedback", human_feedback)
    
    # Flow
    builder.add_edge(START, "create_analysts")
    builder.add_edge("create_analysts", "human_feedback")
    builder.add_conditional_edges(
        "human_feedback", 
        should_continue_analyst_generation, 
        ["create_analysts", END]
    )
    
    # Compile
    memory = MemorySaver()
    graph = builder.compile(interrupt_before=['human_feedback'], checkpointer=memory)
    
    # Save visualization
    try:
        png_data = graph.get_graph(xray=1).draw_mermaid_png()
        with open("analyst_graph.png", "wb") as f:
            f.write(png_data)
        logger.info("Analyst graph visualization saved to analyst_graph.png")
    except Exception as e:
        logger.warning(f"Could not save graph visualization: {e}")
    
    return graph


def build_interview_graph():
    """Build the interview sub-graph."""
    logger.info("Building interview graph")
    
    # Add nodes
    interview_builder = StateGraph(InterviewState)
    interview_builder.add_node("ask_question", generate_question)
    interview_builder.add_node("search_web", search_web)
    interview_builder.add_node("search_wikipedia", search_wikipedia)
    interview_builder.add_node("answer_question", generate_answer)
    interview_builder.add_node("save_interview", save_interview)
    interview_builder.add_node("write_section", write_section)
    
    # Flow
    interview_builder.add_edge(START, "ask_question")
    interview_builder.add_edge("ask_question", "search_web")
    interview_builder.add_edge("ask_question", "search_wikipedia")
    interview_builder.add_edge("search_web", "answer_question")
    interview_builder.add_edge("search_wikipedia", "answer_question")
    interview_builder.add_conditional_edges(
        "answer_question", 
        route_messages,
        ['ask_question', 'save_interview']
    )
    interview_builder.add_edge("save_interview", "write_section")
    interview_builder.add_edge("write_section", END)
    
    # Compile
    memory = MemorySaver()
    interview_graph = interview_builder.compile(checkpointer=memory).with_config(
        run_name="Conduct Interviews"
    )
    
    # Save visualization
    try:
        png_data = interview_graph.get_graph(xray=1).draw_mermaid_png()
        with open("interview_graph.png", "wb") as f:
            f.write(png_data)
        logger.info("Interview graph visualization saved to interview_graph.png")
    except Exception as e:
        logger.warning(f"Could not save graph visualization: {e}")
    
    return interview_graph


def build_research_graph():
    """Build the complete research graph."""
    logger.info("Building research graph")
    
    # Get the interview sub-graph
    interview_graph = build_interview_graph()
    
    # Add nodes and edges
    builder = StateGraph(ResearchGraphState)
    builder.add_node("create_analysts", create_analysts_for_research)
    builder.add_node("human_feedback", human_feedback_research)
    builder.add_node("conduct_interview", interview_graph)
    builder.add_node("write_report", write_report)
    builder.add_node("write_introduction", write_introduction)
    builder.add_node("write_conclusion", write_conclusion)
    builder.add_node("finalize_report", finalize_report)
    
    # Logic
    builder.add_edge(START, "create_analysts")
    builder.add_edge("create_analysts", "human_feedback")
    builder.add_conditional_edges(
        "human_feedback", 
        initiate_all_interviews, 
        ["create_analysts", "conduct_interview"]
    )
    builder.add_edge("conduct_interview", "write_report")
    builder.add_edge("conduct_interview", "write_introduction")
    builder.add_edge("conduct_interview", "write_conclusion")
    builder.add_edge(
        ["write_conclusion", "write_report", "write_introduction"], 
        "finalize_report"
    )
    builder.add_edge("finalize_report", END)
    
    # Compile
    memory = MemorySaver()
    graph = builder.compile(interrupt_before=['human_feedback'], checkpointer=memory)
    
    # Save visualization
    try:
        png_data = graph.get_graph(xray=1).draw_mermaid_png()
        with open("research_graph.png", "wb") as f:
            f.write(png_data)
        logger.info("Research graph visualization saved to research_graph.png")
    except Exception as e:
        logger.warning(f"Could not save graph visualization: {e}")
    
    return graph

