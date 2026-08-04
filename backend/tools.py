import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# ---------------------------------------------------------
# Tavily client setup
# This is the ONLY place Tavily is called directly.
# If you switch to SerpAPI/Firecrawl later, only this file changes.
# ---------------------------------------------------------
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches the web using Tavily and returns clean results.

    Args:
        query: the search query string
        max_results: how many results to fetch (keep low to save free-tier quota)

    Returns:
        list of dicts like:
        [
            {"title": "...", "url": "...", "content": "..."},
            ...
        ]
    """

    print(f"[tools.py] 🔍 Searching Tavily for: '{query}'")  # debug log — shows when search runs

    try:
        response = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth="basic"  # "basic" = faster/cheaper, "advanced" = deeper but uses more quota
        )

        # Tavily returns a dict with a "results" key — we extract only what we need
        results = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")
            }
            for r in response.get("results", [])
        ]

        print(f"[tools.py] ✅ Got {len(results)} results")  # confirms search succeeded
        return results

    except Exception as e:
        # If Tavily fails (bad key, no internet, quota exceeded) — don't crash the whole pipeline
        print(f"[tools.py] ❌ Search failed: {e}")
        return []


def format_results_for_llm(results: list[dict]) -> str:
    """
    Converts search results into a clean text block
    so it can be pasted directly into an LLM prompt.
    """

    if not results:
        return "No search results found."

    formatted = ""
    for i, r in enumerate(results, start=1):
        formatted += f"[{i}] {r['title']}\n{r['content']}\nSource: {r['url']}\n\n"

    return formatted