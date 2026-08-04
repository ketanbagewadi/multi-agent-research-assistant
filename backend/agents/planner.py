# backend/agents/planner.py

from backend.llm import call_llm

PLANNER_SYSTEM_PROMPT = """You are a research planner.
Break the user's question into 2-4 focused sub-questions — one per distinct entity/topic asked about.
Each sub-question must explicitly include the word "current" or "2026" if asking about a present-day fact,
to bias search results toward up-to-date information instead of historical lists.
Respond with ONLY a numbered list, one sub-question per line. No extra text."""


def planner_node(state: dict) -> dict:
    query = state["query"]

    print("[planner] Breaking down query...")

    response = call_llm(query, system=PLANNER_SYSTEM_PROMPT)

    # Parse numbered list into a clean list of strings
    sub_tasks = [
        line.split(".", 1)[-1].strip()
        for line in response.strip().split("\n")
        if line.strip()
    ]

    state["sub_tasks"] = sub_tasks
    print(f"[planner] ✅ {len(sub_tasks)} sub-tasks created: {sub_tasks}")

    return state