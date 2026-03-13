"""
rag_graph.py — LangGraph RAG pipeline for NovaTech SmartSearch (Challenge 3).

Graph nodes:
  route_query  →  retrieve (or skip)  →  format_context  →  END

Exposes:
  async def run_rag(query, history, system_prompt) -> tuple[list[str], list[dict]]
    Returns (retrieved_titles, ollama_messages_list)
"""

from typing import TypedDict, List

from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END

import rag_engine


# ---------------------------------------------------------------------------
# State schema
# ---------------------------------------------------------------------------

class RAGState(TypedDict):
    query: str
    history: List[dict]
    system_prompt: str
    documents: List[Document]
    retrieved_titles: List[str]
    context: str


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

# Keywords that suggest the user wants factual information from the knowledge base
_KNOWLEDGE_KEYWORDS = {
    "what", "how", "why", "when", "where", "who", "which",
    "tell me", "explain", "describe", "show", "list", "summarize",
    "find", "search", "look up", "about", "info", "information",
    "details", "guide", "policy", "feature", "price", "pricing",
    "plan", "product", "api", "endpoint", "security", "benefit",
    "roadmap", "onboarding", "handbook", "document", "report",
    "help", "support", "faq", "question",
}


def route_query(state: RAGState) -> RAGState:
    """Decide whether to retrieve documents or skip retrieval."""
    query_lower = state["query"].lower()
    should_retrieve = any(kw in query_lower for kw in _KNOWLEDGE_KEYWORDS)
    # Also retrieve if query is longer than a typical greeting
    if len(state["query"].split()) > 5:
        should_retrieve = True
    return {**state, "_should_retrieve": should_retrieve}  # type: ignore[misc]


def retrieve(state: RAGState) -> RAGState:
    """Retrieve top-k documents using BM25."""
    docs = rag_engine.search(state["query"], top_k=3)
    titles = [d.metadata["title"] for d in docs]
    return {**state, "documents": docs, "retrieved_titles": titles}


def skip_retrieve(state: RAGState) -> RAGState:
    """No-op — skip retrieval for simple conversational queries."""
    return {**state, "documents": [], "retrieved_titles": []}


def format_context(state: RAGState) -> RAGState:
    """Format retrieved documents into a context string for the LLM."""
    docs = state.get("documents", [])
    if not docs:
        return {**state, "context": ""}

    parts = []
    for i, doc in enumerate(docs, 1):
        title = doc.metadata.get("title", f"Document {i}")
        parts.append(f"--- RETRIEVED DOCUMENT {i}: {title} ---\n{doc.page_content}\n--- END DOCUMENT {i} ---")

    context = "\n\n".join(parts)
    return {**state, "context": context}


# ---------------------------------------------------------------------------
# Routing function (edge condition)
# ---------------------------------------------------------------------------

def _route_edge(state: RAGState):
    if state.get("_should_retrieve", True):  # type: ignore[typeddict-item]
        return "retrieve"
    return "skip_retrieve"


# ---------------------------------------------------------------------------
# Build graph
# ---------------------------------------------------------------------------

_builder = StateGraph(RAGState)

_builder.add_node("route_query", route_query)
_builder.add_node("retrieve", retrieve)
_builder.add_node("skip_retrieve", skip_retrieve)
_builder.add_node("format_context", format_context)

_builder.add_edge(START, "route_query")
_builder.add_conditional_edges("route_query", _route_edge, {
    "retrieve": "retrieve",
    "skip_retrieve": "skip_retrieve",
})
_builder.add_edge("retrieve", "format_context")
_builder.add_edge("skip_retrieve", "format_context")
_builder.add_edge("format_context", END)

_graph = _builder.compile()


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

async def run_rag(
    query: str,
    history: list[dict],
    system_prompt: str,
) -> tuple[list[str], list[dict]]:
    """
    Run the RAG pipeline for a query.

    Returns:
        (retrieved_titles, ollama_messages)
        - retrieved_titles: list of document titles that were retrieved
        - ollama_messages: list of {role, content} dicts ready for the Ollama API
    """
    initial_state: RAGState = {
        "query": query,
        "history": history,
        "system_prompt": system_prompt,
        "documents": [],
        "retrieved_titles": [],
        "context": "",
    }

    result = await _graph.ainvoke(initial_state)

    retrieved_titles: list[str] = result.get("retrieved_titles", [])
    context: str = result.get("context", "")

    # Build the full system prompt (with context appended if any)
    full_system = system_prompt
    if context:
        full_system = f"{system_prompt}\n\n{context}"

    # Build the Ollama messages list
    messages: list[dict] = [{"role": "system", "content": full_system}]
    for msg in history[-12:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": query})

    return retrieved_titles, messages
