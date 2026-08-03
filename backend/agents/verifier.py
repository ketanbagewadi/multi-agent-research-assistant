# backend/agents/verifier.py

from backend.tools import web_search, format_results_for_llm
from backend.llm import call_llm

# ---------------------------------------------------------
# Verifier Agent
# Job: take the Summarizer's output and fact-check it by
# doing a SECOND, independent search. Then ask the LLM to
# judge if the summary is well-supported or not.
# ---------------------------------------------------------

VERIFIER_SYSTEM_PROMPT = """You are a fact-checker.
You will be given a summary and a fresh set of independent search results.
Check if the summary's claims are supported by these new results.
Respond with EXACTLY one word first: "PASS" or "FAIL"
Then on a new line, give a 1-2 sentence reason.

Example:
PASS
The claims match the independent search results closely.
"""


def verifier_node(state: dict) -> dict:
    """
    Input:  state["summary"]       -> summary from Summarizer agent
            state["query"]         -> original user query
            state["retry_count"]   -> how many times we've retried (default 0)
    Output: state["verified"]      -> True/False
            state["retry_count"]   -> incremented if failed
            state["verify_reason"] -> LLM's reasoning (useful for debugging/logs)
    """

    query = state["query"]
    summary = state["summary"]
    retry_count = state.get("retry_count", 0)

    print("[verifier] Running independent fact-check search...")

    # Independent search — different from Searcher's original results,
    # so we're not just checking the summary against itself.
    check_results = web_search(f"verify facts: {query}", max_results=3)
    check_text = format_results_for_llm(check_results)

    prompt = f"""Summary to verify:
{summary}

Independent search results (for verification):
{check_text}

Does the summary's claims hold up against these independent results?"""

    verdict = call_llm(prompt, system=VERIFIER_SYSTEM_PROMPT)

    # Parse first line for PASS/FAIL
    first_line = verdict.strip().split("\n")[0].strip().upper()
    passed = "PASS" in first_line

    state["verified"] = passed
    state["verify_reason"] = verdict
    state["retry_count"] = retry_count if passed else retry_count + 1

    status = "✅ PASSED" if passed else f"❌ FAILED (retry {state['retry_count']})"
    print(f"[verifier] {status}")
    print(f"[verifier] Reason: {verdict[:150]}...")

    return state