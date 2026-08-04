from backend.mcp_client import call_mcp_tool

SEARCH_SERVER = "backend.mcp_servers.web_search_server"

def searcher_node(state: dict) -> dict:
    sub_tasks = state.get("sub_tasks") or [state["query"]]
    retry_count = state.get("retry_count", 0)

    all_results = []
    for task in sub_tasks:
        query = task
        if retry_count > 0:
            query = f"{task} (more reliable sources, retry {retry_count})"

        print(f"[searcher] Calling MCP web-search tool for: '{query}'")

        result_text = call_mcp_tool(
            module_name=SEARCH_SERVER,
            tool_name="search",
            arguments={"query": query, "max_results": 3}
        )
        all_results.append(result_text)

    combined = "\n\n---\n\n".join(all_results)
    state["search_results"] = combined
    state["search_text"] = combined

    print(f"[searcher] ✅ Done via MCP ({len(sub_tasks)} sub-task searches).")

    return state