# backend/agents/summarizer.py

from backend.llm import call_llm

# ---------------------------------------------------------
# Summarizer Agent
# Job: take the raw search results text (from Searcher agent)
# and condense it into a clean, structured summary using the LLM.
# ---------------------------------------------------------

SUMMARIZER_SYSTEM_PROMPT = """You are a research summarizer.
You will be given raw search results with sources.
Your job: extract only the key facts, remove repetition and marketing fluff,
and organize them into short, clear bullet points.
Always keep track of which source each fact came from (use [1], [2], etc).
Do not add information that isn't in the search results."""


def summarizer_node(state: dict) -> dict:
    """
    Input:  state["search_text"]  -> formatted search results from Searcher
    Output: state["summary"]       -> clean bullet-point summary
    """

    search_text = state["search_text"]
    query = state["query"]

    print("[summarizer] Starting summarization...")

    prompt = f"""User's research question: {query}

Search results:
{search_text}

Summarize the key facts as bullet points, citing sources like [1], [2]."""

    summary = call_llm(prompt, system=SUMMARIZER_SYSTEM_PROMPT)

    state["summary"] = summary

    print("[summarizer] ✅ Done.")
    print(f"[summarizer] Summary preview:\n{summary[:200]}...")  # first 200 chars for a quick sanity check

    return state