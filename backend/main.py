# backend/main.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json

from backend.graph import research_graph
from backend.db import save_report, init_db

# ---------------------------------------------------------
# FastAPI app setup
# ---------------------------------------------------------

app = FastAPI(title="Multi-Agent Research Assistant")

# Allow frontend (running on a different port/file) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # for dev only — restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the SQLite table on startup (if it doesn't exist yet)
@app.on_event("startup")
def startup():
    init_db()
    print("[main] 🚀 Server started, DB ready.")


# ---------------------------------------------------------
# /run-agent endpoint — streams each agent step as it completes
# ---------------------------------------------------------

@app.get("/run-agent")
async def run_agent(query: str):
    """
    Streams live updates as the LangGraph pipeline runs.
    Frontend listens to this via EventSource (SSE).
    """

    def event_stream():
        initial_state = {"query": query, "retry_count": 0}

        # research_graph.stream() yields state after EACH node finishes
        # this is what makes live step-by-step updates possible
        for step in research_graph.stream(initial_state):
            node_name = list(step.keys())[0]       # e.g. "searcher", "summarizer"
            node_output = step[node_name]

            # Send a small status update to frontend
            update = {
                "node": node_name,
                "status": "done"
            }
            yield f"data: {json.dumps(update)}\n\n"

            # If this is the writer node (last step), send the final report too
            if node_name == "writer":
                final_report = node_output.get("final_report", "")
                save_report(query, final_report)   # persist to SQLite

                final_update = {
                    "node": "final",
                    "report": final_report
                }
                yield f"data: {json.dumps(final_update)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ---------------------------------------------------------
# Simple health check
# ---------------------------------------------------------

@app.get("/")
def health():
    return {"status": "running"}