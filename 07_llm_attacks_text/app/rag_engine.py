"""
rag_engine.py — BM25-based document store for NovaTech SmartSearch (Challenge 3).

Documents are persisted as JSON at /data/documents.json.
Seed documents are loaded on first run if the file does not exist.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

# ---------------------------------------------------------------------------
# Storage path
# ---------------------------------------------------------------------------
DATA_PATH = os.getenv("RAG_DATA_PATH", "/data/documents.json")

# ---------------------------------------------------------------------------
# Seed documents — realistic company knowledge-base content
# ---------------------------------------------------------------------------
SEED_DOCUMENTS = [
    {
        "id": "doc-seed-001",
        "title": "NovaTech Product Guide v4.1",
        "source": "system",
        "added_by": "system",
        "added_at": "2024-09-01T00:00:00Z",
        "content": (
            "NovaTech Product Guide — Version 4.1\n\n"
            "NovaBot Pro — Enterprise AI Assistant\n"
            "NovaBot Pro is our flagship product designed for large organisations "
            "that need reliable, scalable AI tooling.\n\n"
            "Key features:\n"
            "• 99.9% uptime SLA with dedicated infrastructure\n"
            "• Custom fine-tuning on proprietary data\n"
            "• Dedicated REST API with webhook support\n"
            "• 24/7 priority support with 1-hour SLA\n"
            "• SOC 2 Type II certified deployment\n"
            "Price: $299 per seat per month (annual contract)\n\n"
            "NovaBot Lite — For Small Teams\n"
            "Ideal for teams of up to 10 users who need conversational AI "
            "without the overhead of enterprise tooling.\n\n"
            "Key features:\n"
            "• Up to 10 users included\n"
            "• Pre-built Q&A templates\n"
            "• Email support with 48-hour SLA\n"
            "• 14-day free trial, no credit card required\n"
            "Price: $79 per month flat rate\n\n"
            "NovaBot API — Developer Tier\n"
            "Pay-as-you-go access for developers and integrators.\n"
            "• $0.002 per 1,000 tokens\n"
            "• Full REST API access\n"
            "• Python, Node.js, and Go SDKs available\n"
            "• Webhook and streaming support\n"
            "• 99.5% uptime SLA"
        ),
    },
    {
        "id": "doc-seed-002",
        "title": "Information Security Playbook v3.0",
        "source": "system",
        "added_by": "system",
        "added_at": "2024-09-01T00:00:00Z",
        "content": (
            "NovaTech Information Security Playbook — Version 3.0\n\n"
            "1. Access Control Policy\n"
            "All employees must enable multi-factor authentication (MFA) on all "
            "company systems within 24 hours of account creation. Failure to "
            "comply results in account suspension.\n\n"
            "Password requirements:\n"
            "• Minimum 14 characters\n"
            "• Must include uppercase, lowercase, number, and symbol\n"
            "• Rotated every 90 days\n"
            "• No reuse of the last 12 passwords\n\n"
            "Principle of least privilege applies to all system and data access. "
            "Access requests must be approved by the employee's manager and the "
            "Security Operations team.\n\n"
            "2. Incident Response\n"
            "All security incidents must be reported to security@novatech.io "
            "immediately upon discovery. The Security Operations Centre (SOC) "
            "is staffed 24/7.\n\n"
            "Data breach notification:\n"
            "• Internal escalation: within 1 hour\n"
            "• Regulatory notification (GDPR Article 33): within 72 hours\n"
            "• Customer notification: within 5 business days if data affected\n\n"
            "3. Compliance\n"
            "NovaTech holds the following certifications:\n"
            "• SOC 2 Type II (renewed annually)\n"
            "• GDPR compliant (EU and UK)\n"
            "• ISO 27001 certification in progress (target: Q2 2025)\n"
            "• PCI-DSS Level 3 for payment processing"
        ),
    },
    {
        "id": "doc-seed-003",
        "title": "Employee Onboarding Guide 2024",
        "source": "system",
        "added_by": "system",
        "added_at": "2024-09-01T00:00:00Z",
        "content": (
            "Welcome to NovaTech — Employee Onboarding Guide 2024\n\n"
            "Our Values: Innovation · Integrity · Impact\n\n"
            "Week 1: Orientation\n"
            "• Day 1: IT setup, access provisioning, security training\n"
            "• Day 2: Team introductions and product deep-dive\n"
            "• Day 3–5: Shadow senior team members, read internal wikis\n\n"
            "30/60/90 Day Plan:\n"
            "• 30 days: Complete onboarding courses, deliver first small task\n"
            "• 60 days: Contribute independently to team projects\n"
            "• 90 days: Own a deliverable end-to-end\n\n"
            "Benefits:\n"
            "• Medical, dental, and vision insurance (100% employer-paid for employee)\n"
            "• 401(k) with 4% company match, vesting on day 1\n"
            "• Unlimited PTO (minimum 15 days per year strongly encouraged)\n"
            "• $2,000 annual learning and development budget\n"
            "• $500 home-office setup stipend\n"
            "• Remote-first culture — headquarters in San Francisco, optional co-working\n\n"
            "Key Contacts:\n"
            "• IT Helpdesk: it-help@novatech.io\n"
            "• HR team: people@novatech.io\n"
            "• Security: security@novatech.io\n"
            "• Office Manager: facilities@novatech.io"
        ),
    },
    {
        "id": "doc-seed-004",
        "title": "NovaTech Public API Developer Guide v2.3",
        "source": "system",
        "added_by": "system",
        "added_at": "2024-09-01T00:00:00Z",
        "content": (
            "NovaTech Public API Developer Guide — Version 2.3\n\n"
            "Base URL: https://api.novatech.io/v2\n\n"
            "Authentication:\n"
            "All API requests must include a Bearer token in the Authorization header:\n"
            "  Authorization: Bearer <your_api_key>\n\n"
            "API keys can be generated at: https://console.novatech.io/api-keys\n\n"
            "Rate Limits:\n"
            "• Developer (free): 100 requests/minute, 10,000 requests/day\n"
            "• Pro: 1,000 requests/minute, unlimited/day\n"
            "• Enterprise: custom limits, contact sales\n\n"
            "Core Endpoints:\n\n"
            "POST /v2/chat — Submit a conversational query\n"
            "Request body: {\"model\": \"novabot-pro\", \"messages\": [...], \"stream\": true}\n\n"
            "POST /v2/embeddings — Generate text embeddings\n"
            "Request body: {\"input\": \"text to embed\", \"model\": \"nova-embed-v1\"}\n\n"
            "GET /v2/models — List available models\n\n"
            "Error Codes:\n"
            "• 400 Bad Request — malformed JSON or missing required fields\n"
            "• 401 Unauthorized — missing or invalid API key\n"
            "• 429 Too Many Requests — rate limit exceeded\n"
            "• 500 Internal Server Error — contact support\n\n"
            "SDKs available: Python (pip install novatech), Node.js (npm install @novatech/sdk), Go"
        ),
    },
    {
        "id": "doc-seed-005",
        "title": "NovaTech Product Roadmap H1 2025",
        "source": "system",
        "added_by": "system",
        "added_at": "2024-09-01T00:00:00Z",
        "content": (
            "NovaTech Product Roadmap — H1 2025 (Internal — Confidential)\n\n"
            "Q1 2025 Priorities:\n"
            "• Launch NovaBot Pro v5.0 with multi-modal support (images + text)\n"
            "• Release nova-embed-v2 with 3x improved retrieval accuracy\n"
            "• Open beta of NovaBot Voice for customer service use cases\n"
            "• EU data residency option for GDPR-sensitive customers\n\n"
            "Q2 2025 Priorities:\n"
            "• General availability of NovaBot Voice\n"
            "• Launch NovaTech Marketplace for third-party integrations\n"
            "• Salesforce and HubSpot native integrations (GA)\n"
            "• ISO 27001 certification completion\n"
            "• Self-hosted deployment option for enterprise customers\n\n"
            "Engineering Focus:\n"
            "• Migrate inference infrastructure to H100 clusters\n"
            "• Reduce average response latency from 800ms to under 300ms\n"
            "• Achieve 99.99% uptime for Pro tier\n\n"
            "Go-to-Market:\n"
            "• Target: 500 new enterprise customers in H1\n"
            "• Expand sales team from 12 to 25 AEs\n"
            "• Launch partner program with 10 launch partners"
        ),
    },
]


# ---------------------------------------------------------------------------
# Internal state — in-memory index rebuilt on load / mutation
# ---------------------------------------------------------------------------
_documents: list[dict] = []
_bm25: Optional[BM25Okapi] = None


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer."""
    import re
    return re.findall(r"[a-z0-9]+", text.lower())


def _rebuild_index() -> None:
    global _bm25
    if not _documents:
        _bm25 = None
        return
    corpus = [_tokenize(d["title"] + " " + d["content"]) for d in _documents]
    _bm25 = BM25Okapi(corpus)


def _load() -> None:
    """Load documents from disk, seeding if the file does not exist."""
    global _documents
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        _documents = [dict(d, size_chars=len(d["content"])) for d in SEED_DOCUMENTS]
        _save()
    else:
        with open(DATA_PATH, "r", encoding="utf-8") as fh:
            _documents = json.load(fh)
    _rebuild_index()


def _save() -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as fh:
        json.dump(_documents, fh, indent=2, ensure_ascii=False)


# Initialise on import
_load()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def search(query: str, top_k: int = 3) -> list[Document]:
    """Return up to top_k Document objects ranked by BM25 relevance."""
    if _bm25 is None or not _documents:
        return []
    tokens = _tokenize(query)
    scores = _bm25.get_scores(tokens)
    # Pair (score, doc) and pick top_k with score > 0
    ranked = sorted(
        [(scores[i], _documents[i]) for i in range(len(_documents))],
        key=lambda x: x[0],
        reverse=True,
    )
    query_tokens = set(_tokenize(query))
    results = []
    for score, doc in ranked[:top_k]:
        title_tokens = set(_tokenize(doc["title"]))
        if score <= 0 and not (query_tokens & title_tokens):
            continue  # skip only if score=0 AND no title overlap
        results.append(
            Document(
                page_content=doc["content"],
                metadata={
                    "id": doc["id"],
                    "title": doc["title"],
                    "source": doc["source"],
                    "added_by": doc["added_by"],
                    "score": float(score),
                },
            )
        )
    return results


def list_docs() -> list[dict]:
    """Return all documents (without full content, for listing)."""
    return [
        {
            "id": d["id"],
            "title": d["title"],
            "source": d["source"],
            "added_by": d["added_by"],
            "added_at": d["added_at"],
            "size_chars": d.get("size_chars", len(d.get("content", ""))),
        }
        for d in _documents
    ]


def get_doc(doc_id: str) -> Optional[dict]:
    """Return a single document by ID, or None."""
    for d in _documents:
        if d["id"] == doc_id:
            return d
    return None


def add_doc(title: str, content: str, source: str = "upload", added_by: str = "admin") -> dict:
    """Add a new document and persist to disk. Returns the new doc record."""
    doc = {
        "id": f"doc-{uuid.uuid4().hex[:12]}",
        "title": title,
        "source": source,
        "added_by": added_by,
        "added_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "content": content,
        "size_chars": len(content),
    }
    _documents.append(doc)
    _rebuild_index()
    _save()
    return doc


def delete_doc(doc_id: str) -> bool:
    """Delete a document by ID. Returns True if found and deleted."""
    global _documents
    before = len(_documents)
    _documents = [d for d in _documents if d["id"] != doc_id]
    if len(_documents) < before:
        _rebuild_index()
        _save()
        return True
    return False
