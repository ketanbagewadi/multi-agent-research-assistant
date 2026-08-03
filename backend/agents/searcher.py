# backend/agents/searcher.py

from backend.mcp_client import call_mcp_tool

SEARCH_SERVER = "backend.mcp_servers.web_search_server"

def searcher_node(state: dict) -> dict:
    """
    Input:  state["query"]           -> user's original question
    Output: state["search_results"]  -> raw text from MCP tool
            state["search_text"]     -> same (kept for compatibility with other agents)
    """

    query = state["query"]

    retry_count = state.get("retry_count", 0)
    if retry_count > 0:
        query = f"{query} (more reliable sources, retry {retry_count})"
        print(f"[searcher] 🔁 Retry #{retry_count} — refined query: '{query}'")

    print(f"[searcher] Calling MCP web-search tool for: '{query}'")

    # Calls the MCP server instead of tools.py directly
    search_text = call_mcp_tool(
        module_name=SEARCH_SERVER,
        tool_name="search",
        arguments={"query": query, "max_results": 5}
    )

    state["search_results"] = search_text   # kept as text now (MCP tool returns formatted string)
    state["search_text"] = search_text

    print(f"[searcher] ✅ Done via MCP.")

    return state