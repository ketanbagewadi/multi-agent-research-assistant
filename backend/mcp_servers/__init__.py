python3
>>> from backend.agents.searcher import searcher_node
>>> state = {"query": "best vector databases for RAG 2026", "retry_count": 0}
>>> updated_state = searcher_node(state)
>>> print(updated_state["search_text"])