from backend.mcp_client import call_mcp_tool
from backend.llm import call_llm

FACT_CHECK_SERVER = "backend.mcp_servers.fact_check_server"

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
    query = state["query"]
    summary = state["summary"]
    retry_count = state.get("retry_count", 0)

    print("[verifier] Calling MCP fact-check tool...")

    check_text = call_mcp_tool(
        module_name=FACT_CHECK_SERVER,
        tool_name="verify_search",
        arguments={"query": query, "max_results": 3}
    )

    prompt = f"""Summary to verify:
{summary}

Independent search results (for verification):
{check_text}

Does the summary's claims hold up against these independent results?"""

    verdict = call_llm(prompt, system=VERIFIER_SYSTEM_PROMPT)

    first_line = verdict.strip().split("\n")[0].strip().upper()
    passed = "PASS" in first_line

    state["verified"] = passed
    state["verify_reason"] = verdict
    state["retry_count"] = retry_count if passed else retry_count + 1

    status = "PASSED" if passed else f"FAILED (retry {state['retry_count']})"
    print(f"[verifier] {status}")

    return state
