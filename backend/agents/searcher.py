# backend/agents/searcher.py

from backend.tools import web_search, format_results_for_llm

# ---------------------------------------------------------
# Searcher Agent
# Job: take the user's query, search the web, store raw results
# in the shared AgentState so the next agent (Summarizer) can use it.
# ---------------------------------------------------------

def searcher_node(state: dict) -> dict:
    """
    Input:  state["query"]           -> user's original question
    Output: state["search_results"]  -> list of search result dicts
            state["search_text"]     -> formatted text version (for LLM prompts)
    """

    query = state["query"]

    # On retry (verifier failed), we slightly tweak the query
    # to get different/better results instead of repeating the same search.
    retry_count = state.get("retry_count", 0)
    if retry_count > 0:
        query = f"{query} (more reliable sources, retry {retry_count})"
        print(f"[searcher] 🔁 Retry #{retry_count} — refined query: '{query}'")

    print(f"[searcher] Starting search for: '{query}'")

    results = web_search(query, max_results=5)

    # Update shared state — this is what LangGraph passes to the next node
    state["search_results"] = results
    state["search_text"] = format_results_for_llm(results)

    print(f"[searcher] ✅ Done. Found {len(results)} results.")

    return state