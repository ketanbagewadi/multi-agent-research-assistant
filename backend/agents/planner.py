from datetime import date
from backend.llm import call_llm

PLANNER_SYSTEM_PROMPT = """You are a research planner.
You will be told today's actual date — use it, don't guess a year yourself.
Break the user's question into 2-4 focused sub-questions — one per distinct entity/topic.
For anything time-sensitive (prices, current office-holders, current events),
explicitly include today's date or "today" in the sub-question to force fresh results.
Never invent or assume a year on your own.
Respond with ONLY a numbered list, one sub-question per line. No extra text."""


def planner_node(state: dict) -> dict:
    query = state["query"]
    today = date.today().strftime("%B %d, %Y")  # e.g. "August 04, 2026"

    print(f"[planner] Breaking down query (today = {today})...")

    prompt = f"""Today's date is {today}.
User's question: {query}"""

    response = call_llm(prompt, system=PLANNER_SYSTEM_PROMPT)

    sub_tasks = [
        line.split(".", 1)[-1].strip()
        for line in response.strip().split("\n")
        if line.strip()
    ]

    state["sub_tasks"] = sub_tasks
    print(f"[planner] ✅ {len(sub_tasks)} sub-tasks created: {sub_tasks}")

    return state