# backend/mcp_servers/web_search_server.py

from mcp.server.fastmcp import FastMCP
from backend.tools import web_search, format_results_for_llm

# ---------------------------------------------------------
# MCP Server: exposes web_search as a standardized MCP tool.
# Agents connect to this as MCP clients instead of calling
# tools.py directly — this is what makes it "MCP integration"
# rather than a plain function call.
# ---------------------------------------------------------

mcp = FastMCP("web-search-server")


@mcp.tool()
def search(query: str, max_results: int = 5) -> str:
    """
    Search the web for a query and return formatted results.
    """
    print(f"[MCP:web-search] Tool called with query: '{query}'")
    results = web_search(query, max_results=max_results)
    return format_results_for_llm(results)


if __name__ == "__main__":
    mcp.run(transport="stdio")