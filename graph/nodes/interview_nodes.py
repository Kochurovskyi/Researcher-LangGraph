"""Node functions for conducting interviews."""
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, get_buffer_string
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WikipediaLoader
from graph.state import InterviewState
from graph.models import SearchQuery
from graph.chains.llm import llm
from graph.chains.prompts import (
    QUESTION_INSTRUCTIONS, 
    SEARCH_INSTRUCTIONS, 
    ANSWER_INSTRUCTIONS,
    SECTION_WRITER_INSTRUCTIONS
)
from graph.logging_config import logger
from config import WEB_SEARCH_MAX_RESULTS, WIKIPEDIA_MAX_DOCS


# Initialize search tools
tavily_search = TavilySearch(max_results=WEB_SEARCH_MAX_RESULTS)


def generate_question(state: InterviewState):
    """Generate a question for the interview."""
    logger.info("Generating interview question")
    analyst = state["analyst"]
    messages = state["messages"]
    
    # Generate question
    system_message = QUESTION_INSTRUCTIONS.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)
    
    logger.info(f"Generated question from {analyst.name}")
    return {"messages": [question]}


def search_web(state: InterviewState):
    """Retrieve docs from web search."""
    logger.info("Performing web search")
    structured_llm = llm.with_structured_output(SearchQuery)
    search_instructions_msg = SystemMessage(content=SEARCH_INSTRUCTIONS)
    search_query = structured_llm.invoke([search_instructions_msg] + state['messages'])
    
    logger.info(f"Web search query: {search_query.search_query}")
    search_docs = tavily_search.invoke(search_query.search_query)
    
    # Handle both string and dict responses from TavilySearch
    if isinstance(search_docs, str):
        formatted_search_docs = f'<Document source="web_search"/>\n{search_docs}\n</Document>'
    elif isinstance(search_docs, list) and len(search_docs) > 0 and isinstance(search_docs[0], dict):
        formatted_search_docs = "\n\n---\n\n".join([
            f'<Document href="{doc.get("url", "")}"/>\n{doc.get("content", doc)}\n</Document>' 
            for doc in search_docs
        ])
    else:
        formatted_search_docs = f'<Document source="web_search"/>\n{str(search_docs)}\n</Document>'
    
    logger.info(f"Web search completed, found {len(search_docs) if isinstance(search_docs, list) else 1} results")
    return {"context": [formatted_search_docs]}


def search_wikipedia(state: InterviewState):
    """Retrieve docs from wikipedia."""
    logger.info("Performing Wikipedia search")
    structured_llm = llm.with_structured_output(SearchQuery)
    search_instructions_msg = SystemMessage(content=SEARCH_INSTRUCTIONS)
    search_query = structured_llm.invoke([search_instructions_msg] + state['messages'])
    
    logger.info(f"Wikipedia search query: {search_query.search_query}")
    search_docs = WikipediaLoader(query=search_query.search_query, load_max_docs=WIKIPEDIA_MAX_DOCS).load()
    
    formatted_search_docs = "\n\n---\n\n".join([
        f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
        for doc in search_docs
    ])
    
    logger.info(f"Wikipedia search completed, found {len(search_docs)} documents")
    return {"context": [formatted_search_docs]}


def generate_answer(state: InterviewState):
    """Generate an answer to the analyst's question."""
    logger.info("Generating answer")
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]
    
    # Answer question
    system_message = ANSWER_INSTRUCTIONS.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_message)] + messages)
    
    # Name the message as coming from the expert
    answer.name = "expert"
    
    logger.info("Answer generated from expert")
    return {"messages": [answer]}


def save_interview(state: InterviewState):
    """Save the interview transcript."""
    logger.info("Saving interview transcript")
    messages = state["messages"]
    
    # Convert interview to a string
    interview = get_buffer_string(messages)
    
    logger.info(f"Interview saved, length: {len(interview)} characters")
    return {"interview": interview}


def write_section(state: InterviewState):
    """Write a report section based on the interview."""
    logger.info("Writing report section")
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]
    
    # Write section using the gathered source docs from interview
    system_message = SECTION_WRITER_INSTRUCTIONS.format(focus=analyst.description)
    section = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=f"Use this source to write your section: {context}")
    ])
    
    logger.info(f"Section written, length: {len(section.content)} characters")
    return {"sections": [section.content]}


def route_messages(state: InterviewState, name: str = "expert"):
    """Route between question and answer based on conversation state."""
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns', 2)
    
    # Check the number of expert answers
    num_responses = len([m for m in messages if isinstance(m, AIMessage) and m.name == name])
    
    # End if expert has answered more than the max turns
    if num_responses >= max_num_turns:
        logger.info(f"Max turns ({max_num_turns}) reached, saving interview")
        return 'save_interview'
    
    # Get the last question asked to check if it signals the end of discussion
    last_question = messages[-2]
    if "Thank you so much for your help" in last_question.content:
        logger.info("Interview concluded by analyst, saving")
        return 'save_interview'
    
    logger.info("Continuing interview")
    return "ask_question"

