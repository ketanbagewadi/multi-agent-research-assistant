# backend/mcp_servers/fact_check_server.py

from mcp.server.fastmcp import FastMCP
from backend.tools import web_search, format_results_for_llm

mcp = FastMCP("fact-check-server")


@mcp.tool()
def verify_search(query: str, max_results: int = 3) -> str:
    """
    Independent search used specifically for fact-checking claims.
    """
    print(f"[MCP:fact-check] Tool called with query: '{query}'")
    results = web_search(f"verify facts: {query}", max_results=max_results)
    return format_results_for_llm(results)


if __name__ == "__main__":
    mcp.run(transport="stdio")