# multi-agent-research-assistant

A multi-agent AI system where specialized agents collaborate to research a topic end-to-end — search, summarize, verify, and write — with a self-correction retry loop and a live-streaming case-file UI.


```text
research-agent/
├── backend/
│   ├── main.py              # FastAPI app + SSE endpoint
│   ├── agents/
│   │   ├── searcher.py      # Executes targeted web queries
│   │   ├── summarizer.py    # Extracts key context from raw data
│   │   ├── verifier.py      # Cross-references facts & flags contradictions
│   │   └── writer.py        # Compiles the final structured markdown report
│   ├── graph.py              # LangGraph orchestration & state pipeline
│   ├── llm.py                 # Core routing model (Claude API / Local Ollama)
│   ├── tools.py               # Tavily search wrapper API integration
│   ├── db.py                   # SQLite configuration for session memory
│   └── requirements.txt     # Python project dependencies
├── frontend/
│   └── index.html            # Minimalist single-file UI (HTML + CSS + Vanilla JS)
└── README.md                # System documentation
```



## Requirements

- Python >= 3.10
- Free API keys: [Tavily](https://tavily.com) (search), and one LLM provider — [Anthropic](https://console.anthropic.com), [OpenAI](https://platform.openai.com), [Groq](https://console.groq.com), or a local [Ollama](https://ollama.com) install
- Full dependency list: `backend/requirements.txt`

## How It Works

```
User Query
   ↓
Searcher Agent    → web search via Tavily
   ↓
Summarizer Agent  → condenses findings into bullet points
   ↓
Verifier Agent    → independent re-search to fact-check the summary
   │
   ├── fails (retry < 2) → loops back to Searcher
   └── passes / retries exhausted ↓
Writer Agent      → composes the final report
   ↓
Streamed live to frontend via SSE, saved to SQLite
```

Built with **LangGraph** for agent orchestration, with conditional routing for the verify-and-retry loop.

## Directory Structure

| Folder / File          | Description                                              |
| ----------------------- | --------------------------------------------------------- |
| `backend/agents/`       | One file per agent — `searcher.py`, `summarizer.py`, `verifier.py`, `writer.py` |
| `backend/graph.py`      | LangGraph pipeline — wires agents together, defines retry logic |
| `backend/llm.py`        | Pluggable LLM layer — switches between Claude, OpenAI, Groq, or Ollama via `.env` |
| `backend/tools.py`      | Tavily search wrapper — the only file that calls the search API directly |
| `backend/db.py`         | SQLite setup — saves and retrieves past research reports |
| `backend/main.py`       | FastAPI app — `/run-agent` SSE streaming endpoint         |
| `frontend/index.html`   | Single-file UI (HTML/CSS/JS) — case-file themed, streams agent progress live |

## Tech Stack

| Layer            | Tool                                  |
| ------------------ | -------------------------------------- |
| Orchestration     | LangGraph                              |
| LLM               | Claude / OpenAI / Groq / Ollama (pluggable) |
| Web search        | Tavily API                             |
| Backend           | Python + FastAPI                       |
| Streaming         | Server-Sent Events (SSE)               |
| Database          | SQLite                                 |
| Frontend          | HTML + CSS + JS (single file, no framework) |

---

## Run Locally

1. Clone the repo:

   ```
   git clone https://github.com/ketanbagewadi/multi-agent-research-assistant.git
   cd multi-agent-research-assistant
   ```

2. Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate   # venv\Scripts\activate on Windows
   ```

3. Install dependencies:

   ```
   pip install -r backend/requirements.txt
   ```

4. Create a `.env` file in the project root:

   ```
   LLM_PROVIDER=ollama          # claude | openai | groq | ollama

   TAVILY_API_KEY=your_key
   ANTHROPIC_API_KEY=your_key
   OPENAI_API_KEY=your_key
   GROQ_API_KEY=your_key
   ```

5. (If using Ollama) pull a local model:

   ```
   ollama pull llama3.2
   ```

6. Run the backend:

   ```
   uvicorn backend.main:app --reload --port 8000
   ```

7. Open `frontend/index.html` directly in your browser.

---

## Switching LLM Providers

Change one line in `.env` — no code changes needed:

```
LLM_PROVIDER=claude    # or openai / groq / ollama
```

Every agent calls a single `call_llm()` function in `backend/llm.py`, which routes to the selected provider.

## API

**`GET /run-agent?query=<your question>`**
Streams live progress via SSE — one event per agent step (`searcher`, `summarizer`, `verifier`, `writer`), followed by a `final` event containing the completed report. Each completed report is also saved to `research_reports.db` (SQLite).

## Notes

- Retry loop caps at 2 attempts — if the Verifier still can't confirm the summary after 2 retries, the Writer produces a best-effort report anyway rather than failing silently.
- Tavily calls are isolated in `tools.py` — swapping to a different search provider (SerpAPI, Firecrawl, etc.) only requires editing that one file.

## Links

- GitHub: [ketanbagewadi/multi-agent-research-assistant](https://github.com/ketanbagewadi/multi-agent-research-assistant)
- Portfolio: [ketanbagewadi.github.io/ketan-portfolio](https://ketanbagewadi.github.io/ketan-portfolio/)
