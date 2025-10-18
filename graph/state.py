"""State definitions for the research agent graphs."""
from typing import List, Annotated
from typing_extensions import TypedDict
import operator
from langgraph.graph import MessagesState
from graph.models import Analyst


class GenerateAnalystsState(TypedDict):
    """State for the analyst generation graph."""
    topic: str                              # Research topic
    max_analysts: int                       # Number of analysts
    human_analyst_feedback: str             # Human feedback
    analysts: List[Analyst]                 # Analyst asking questions


class InterviewState(MessagesState):
    """State for the interview sub-graph."""
    max_num_turns: int                      # Number turns of conversation
    context: Annotated[list, operator.add]  # Source docs
    analyst: Analyst                        # Analyst asking questions
    interview: str                          # Interview transcript
    sections: list                          # Final key we duplicate in outer state for Send() API


class ResearchGraphState(TypedDict):
    """State for the main research graph."""
    topic: str                                      # Research topic
    max_analysts: int                               # Number of analysts
    human_analyst_feedback: str                     # Human feedback
    analysts: List[Analyst]                         # Analyst asking questions
    sections: Annotated[list, operator.add]         # Send() API key
    introduction: str                               # Introduction for the final report
    content: str                                    # Content for the final report
    conclusion: str                                 # Conclusion for the final report
    final_report: str                               # Final report

