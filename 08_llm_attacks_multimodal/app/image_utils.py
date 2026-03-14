"""
image_utils.py — Image validation, resizing, and base64 encoding for Module 08.

All image processing happens server-side before forwarding to Ollama.
LLaVA expects a list of base64-encoded image strings in the "images" field.
"""

import base64
import io
import os

from fastapi import HTTPException
from PIL import Image

MAX_IMAGE_MB = int(os.getenv("MAX_IMAGE_MB", "5"))
MAX_PIXELS = 1024  # resize to this max dimension before encoding
ALLOWED_FORMATS = {"JPEG", "PNG", "GIF", "WEBP"}


def validate_and_encode(raw: bytes, filename: str) -> str:
    """
    Validate that raw bytes are a real image, enforce size and format limits,
    resize if needed, then return a base64-encoded JPEG string.

    Raises HTTPException on validation failure.
    """
    size_mb = len(raw) / (1024 * 1024)
    if size_mb > MAX_IMAGE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"Image too large ({size_mb:.1f} MB). Maximum is {MAX_IMAGE_MB} MB.",
        )

    try:
        # Open and verify — PIL.verify() closes the handle, so re-open for processing
        buf = io.BytesIO(raw)
        img = Image.open(buf)
        img.load()  # force decode to catch corrupt images
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupt image file. Use JPEG, PNG, GIF, or WEBP.",
        )

    if img.format not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{img.format}'. Allowed: JPEG, PNG, GIF, WEBP.",
        )

    # Convert palette/RGBA modes to RGB for JPEG output
    if img.mode in ("P", "RGBA", "LA", "L"):
        img = img.convert("RGB")

    # Resize if larger than MAX_PIXELS on either dimension (preserve aspect ratio)
    w, h = img.size
    if w > MAX_PIXELS or h > MAX_PIXELS:
        img.thumbnail((MAX_PIXELS, MAX_PIXELS), Image.LANCZOS)

    out = io.BytesIO()
    img.save(out, format="JPEG", quality=85)
    return base64.b64encode(out.getvalue()).decode("utf-8")


def pil_to_b64(img: Image.Image) -> str:
    """Encode a PIL Image directly to base64 JPEG (helper for pre-generated images)."""
    if img.mode not in ("RGB",):
        img = img.convert("RGB")
    out = io.BytesIO()
    img.save(out, format="JPEG", quality=85)
    return base64.b64encode(out.getvalue()).decode("utf-8")
