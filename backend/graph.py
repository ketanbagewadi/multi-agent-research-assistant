# backend/graph.py

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from backend.agents.planner import planner_node
from backend.agents.searcher import searcher_node
from backend.agents.summarizer import summarizer_node
from backend.agents.verifier import verifier_node
from backend.agents.writer import writer_node


class AgentState(TypedDict):
    query: str
    sub_tasks: Optional[list]
    search_results: Optional[list]
    search_text: Optional[str]
    summary: Optional[str]
    verified: Optional[bool]
    verify_reason: Optional[str]
    retry_count: int
    final_report: Optional[str]


MAX_RETRIES = 2

def route_after_verifier(state: AgentState) -> str:
    if state["verified"]:
        print("[graph] Verified — proceeding to Writer.")
        return "writer"

    if state["retry_count"] < MAX_RETRIES:
        print(f"[graph] Not verified — retrying (attempt {state['retry_count']}/{MAX_RETRIES}).")
        return "searcher"

    print("[graph] Retries exhausted — writing best-effort report anyway.")
    return "writer"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("searcher", searcher_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "summarizer")
    graph.add_edge("summarizer", "verifier")

    graph.add_conditional_edges(
        "verifier",
        route_after_verifier,
        {
            "writer": "writer",
            "searcher": "searcher"
        }
    )

    graph.add_edge("writer", END)

    return graph.compile()


research_graph = build_graph()