"""
auth.py — Simple JWT authentication for the NovaTech admin panel.

Credentials and secrets are loaded from environment variables with
intentionally-weak defaults for the training lab context.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

# ---------------------------------------------------------------------------
# Configuration (intentionally embedded for the lab scenario)
# ---------------------------------------------------------------------------
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "NovaTech@RAG2024")
JWT_SECRET: str = os.getenv("JWT_SECRET", "novatech-internal-jwt-secret")

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 8


# ---------------------------------------------------------------------------
# Token functions
# ---------------------------------------------------------------------------

def create_token(username: str) -> str:
    """Create a signed JWT for the given username, valid for TOKEN_EXPIRE_HOURS."""
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": username,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    """
    Verify and decode a JWT.

    Returns the username (sub claim) on success, or None if the token is
    invalid, expired, or malformed.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        return username
    except JWTError:
        return None
