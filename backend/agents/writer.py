
# ---------------------------------------------------------
# Writer Agent
# Job: take the verified summary and turn it into a clean,
# well-formatted final report for the user.
# This is the LAST node in the pipeline.
# ---------------------------------------------------------

from backend.llm import call_llm

WRITER_SYSTEM_PROMPT = """You are a research report writer.
You will be given a verified summary of research findings.
Write a clear, well-structured final report with:
- A short intro (1-2 sentences)
- Organized sections or bullet points
- A brief conclusion
Keep it professional and easy to read. Preserve source citations like [1], [2].

IMPORTANT: Only use facts from the summary provided. Do NOT add your own
prior knowledge, especially for time-sensitive facts like current office-holders —
your training data may be outdated. If something isn't covered in the summary,
say it's unclear rather than guessing."""


def writer_node(state: dict) -> dict:
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