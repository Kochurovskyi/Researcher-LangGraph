"""Main entry point for the research agent."""
from graph.graph import build_research_graph
from graph.logging_config import logger


def main():
    """Run the research agent."""
    # Build the complete research graph
    research_graph = build_research_graph()
    
    # Configuration
    max_analysts = 3
    topic = "Why people love so much cats in the Internet?"
    thread = {"configurable": {"thread_id": "1"}}
    
    # Start research
    logger.info(f"Starting research on: {topic}")
    logger.info(f"Max analysts: {max_analysts}")
    print(f"\nStarting research on: {topic}")
    print(f"Max analysts: {max_analysts}")
    print("-" * 80)
    
    # Run until first interruption (at human_feedback node)
    for event in research_graph.stream(
        {"topic": topic, "max_analysts": max_analysts}, 
        thread, 
        stream_mode="values"
    ):
        analysts = event.get('analysts', '')
        if analysts:
            print(f"\nAnalysts created: {len(analysts)}")
            for analyst in analysts:
                print(f"  - {analyst.name}: {analyst.role}")
    
    # Continue without feedback (in production, you'd handle this interactively)
    research_graph.update_state(
        thread, 
        {"human_analyst_feedback": None}, 
        as_node="human_feedback"
    )
    
    print("\nContinuing research...")
    for event in research_graph.stream(None, thread, stream_mode="updates"):
        node_name = next(iter(event.keys()))
        print(f"Executing: {node_name}")
    
    # Get final report
    final_state = research_graph.get_state(thread)
    final_report = final_state.values.get('final_report')
    
    if final_report:
        print("\n" + "=" * 80)
        print("FINAL REPORT")
        print("=" * 80)
        print(final_report)
        
        # Save report to file
        with open("research_report.md", "w", encoding="utf-8") as f:
            f.write(final_report)
        print("\nReport saved to: research_report.md")
        logger.info("Research completed successfully")


if __name__ == "__main__":
    main()
