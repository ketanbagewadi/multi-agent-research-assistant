# backend/agents/writer.py

from backend.llm import call_llm

# ---------------------------------------------------------
# Writer Agent
# Job: take the verified summary and turn it into a clean,
# well-formatted final report for the user.
# This is the LAST node in the pipeline.
# ---------------------------------------------------------

WRITER_SYSTEM_PROMPT = """You are a research report writer.
You will be given a verified summary of research findings.
Write a clear, well-structured final report with:
- A short intro (1-2 sentences)
- Organized sections or bullet points
- A brief conclusion
Keep it professional and easy to read. Preserve source citations like [1], [2]."""


def writer_node(state: dict) -> dict:
    """
    Input:  state["summary"]        -> verified summary from Verifier stage
            state["query"]          -> original user query
    Output: state["final_report"]   -> polished final report text
    """

    query = state["query"]
    summary = state["summary"]

    print("[writer] Composing final report...")

    prompt = f"""Original research question: {query}

Verified summary:
{summary}

Write the final report."""

    final_report = call_llm(prompt, system=WRITER_SYSTEM_PROMPT)

    state["final_report"] = final_report

    print("[writer] ✅ Report complete.")

    return state