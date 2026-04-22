"""
VLM-based trash bin detector.
Sends an image to Gemini 2.0 Flash via OpenRouter and returns structured detections.
"""

import os
import base64
import json
import re
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-001"

SYSTEM_PROMPT = """You are a computer vision system specialized in urban waste management.
You detect trash bins and ground litter in street/outdoor CCTV images.
Respond with valid JSON only. No markdown, no explanation outside the JSON."""

USER_PROMPT = """Analyze this image and detect all trash bins and any garbage lying on the ground.

Return this exact JSON structure:
{
  "detections": [
    {
      "type": "bin",
      "bbox": [x1, y1, x2, y2],
      "classification": "empty" | "full" | "overfilled" | "invalid",
      "confidence": <float 0.0-1.0>,
      "notes": "<optional short note>"
    },
    {
      "type": "garbage",
      "bbox": [x1, y1, x2, y2],
      "confidence": <float 0.0-1.0>,
      "notes": "<optional short note>"
    }
  ],
  "scene_notes": "<overall scene description>"
}

bbox coordinates are integers as percentage of image dimensions:
- x1, y1: top-left corner (0-100)
- x2, y2: bottom-right corner (0-100)

STEP 1 — Invalidity check (apply per bin, in this priority order):

  A) SHAPE: Is the bin body round, cylindrical, barrel-shaped, or drum-shaped (circular cross-section)?
     If you would describe it as "round bin", "barrel bin", "cylindrical bin", or "drum" — it is invalid.
     Examples: Molok-style underground containers, large barrel bins, any bin where the body is not a rectangular box.
     → If the body is NOT a rectangular/square box shape: classify as "invalid". Do not classify its fill level.

  B) PACKAGING: Is the bin wrapped in plastic shrink-wrap or packaging material?
     Plastic-wrapped bins are products awaiting deployment — invalid regardless of indoor/outdoor setting.
     → If YES: "invalid".

  C) INDOOR STORAGE: Is the scene clearly indoors (warehouse shelving, shop floor, enclosed building) with bins in storage?
     → If YES: "invalid".

  D) Otherwise: proceed to STEP 2.

STEP 2 — Fill level (rectangular/square-bodied bins in any outdoor setting):
- "empty": no garbage visible inside or on top; lid closed with nothing sticking out, or lid open with visibly empty interior
- "full": garbage visibly sticking out above the top rim OR lid physically cannot close due to contents
- "overfilled": garbage bags or loose trash on the GROUND immediately around the bin

For "garbage" type: only mark loose litter, bags, or waste lying on the GROUND outside any bin.
Do not mark garbage that is inside a bin as a separate garbage detection.

If no bins or garbage are found, return empty detections array."""


def _encode_image(path: str) -> tuple[str, str]:
    p = Path(path)
    ext = p.suffix.lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(ext, "image/jpeg")
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode(), mime


def detect(image_source: str) -> dict:
    """
    image_source: local file path or public URL.
    Returns dict with 'detections' list and 'scene_notes'.
    """
    if image_source.startswith("http://") or image_source.startswith("https://"):
        img_content = {"type": "image_url", "image_url": {"url": image_source}}
    else:
        b64, mime = _encode_image(image_source)
        img_content = {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [img_content, {"type": "text", "text": USER_PROMPT}]},
        ],
        "temperature": 0.1,
        "max_tokens": 1024,
    }

    resp = httpx.post(
        API_URL,
        json=payload,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        timeout=45,
    )
    resp.raise_for_status()

    raw = resp.json()["choices"][0]["message"]["content"].strip()
    clean = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.DOTALL).strip()
    return json.loads(clean)
