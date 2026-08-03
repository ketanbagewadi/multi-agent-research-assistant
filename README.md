# multi-agent-research-assistant


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
