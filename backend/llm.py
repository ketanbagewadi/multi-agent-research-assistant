# backend/llm.py

import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # claude | openai | groq | ollama


def call_llm(prompt: str, system: str = "") -> str:
    """
    Unified LLM call — switches provider based on .env LLM_PROVIDER.
    Every agent should call this function only — never call an SDK directly.
    """

    if PROVIDER == "claude":
        return _call_claude(prompt, system)
    elif PROVIDER == "openai":
        return _call_openai(prompt, system)
    elif PROVIDER == "groq":
        return _call_groq(prompt, system)
    elif PROVIDER == "ollama":
        return _call_ollama(prompt, system)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {PROVIDER}")


def _call_claude(prompt: str, system: str) -> str:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def _call_openai(prompt: str, system: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def _call_groq(prompt: str, system: str) -> str:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def _call_ollama(prompt: str, system: str) -> str:
    import ollama
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]