"""
Training dataset search agent.

Usage:
    py datasets/search_agent.py --query "street trash bin overflow CCTV"
    py datasets/search_agent.py --query "waste detection" --out located_datasets.md
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")

HF_API = "https://huggingface.co/api/datasets"

SYSTEM_PROMPT = """You are a computer vision dataset research assistant.
Given a description of images or labels needed for ML training, return a JSON array of relevant public datasets.

Each item must have these fields:
{
  "name": "Dataset Name",
  "url": "direct download or landing page URL",
  "description": "1-2 sentence description of content",
  "size": "approximate image count or GB",
  "license": "license identifier (CC BY 4.0, MIT, custom, etc.)",
  "format": "annotation format (COCO, VOC, YOLO, etc.)",
  "relevance": "high | medium | low"
}

Include datasets from: Kaggle, Roboflow Universe, Papers With Code, GitHub, Zenodo, academic benchmarks.
Focus on datasets that are publicly downloadable.
Return ONLY a valid JSON array. No markdown, no explanation."""


def search_huggingface(query: str, limit: int = 15) -> list[dict]:
    try:
        resp = httpx.get(
            HF_API,
            params={"search": query, "limit": limit, "full": "true"},
            timeout=15,
        )
        resp.raise_for_status()
        results = []
        for ds in resp.json():
            ds_id = ds.get("id", "")
            card = ds.get("cardData") or {}
            results.append({
                "name": ds_id,
                "url": f"https://huggingface.co/datasets/{ds_id}",
                "description": (ds.get("description") or "")[:300].strip(),
                "size": str((card.get("size_categories") or ["?"])[0]),
                "license": card.get("license", "unknown"),
                "format": "HuggingFace",
                "relevance": "medium",
                "source": "HuggingFace Hub",
            })
        return results
    except Exception as e:
        print(f"  HuggingFace search failed: {e}", file=sys.stderr)
        return []


def search_llm(query: str) -> list[dict]:
    if not OPENROUTER_KEY:
        print("  No OPENROUTER_API_KEY — skipping LLM search", file=sys.stderr)
        return []
    try:
        resp = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={
                "model": "google/gemini-2.0-flash-001",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Find training datasets for: {query}"},
                ],
                "temperature": 0.2,
            },
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        datasets = json.loads(raw)
        for ds in datasets:
            ds.setdefault("source", "LLM (Gemini 2.0 Flash)")
        return datasets
    except Exception as e:
        print(f"  LLM search failed: {e}", file=sys.stderr)
        return []


RELEVANCE_ORDER = {"high": 0, "medium": 1, "low": 2}


def write_markdown(datasets: list[dict], query: str, out: Path) -> None:
    lines = [
        "# Located Datasets\n",
        f"**Query:** {query}  ",
        f"**Date:** {date.today()}  ",
        f"**Found:** {len(datasets)} datasets\n",
        "---\n",
    ]

    ranked = sorted(datasets, key=lambda x: RELEVANCE_ORDER.get(x.get("relevance", "low"), 2))

    for ds in ranked:
        lines += [
            f"## {ds['name']}",
            f"- **URL:** {ds['url']}",
            f"- **Relevance:** {ds.get('relevance', '?')}",
            f"- **License:** {ds.get('license', '?')}",
            f"- **Size:** {ds.get('size', '?')}",
            f"- **Format:** {ds.get('format', '?')}",
            f"- **Source:** {ds.get('source', '?')}",
            "",
            ds.get("description", "").strip(),
            "",
        ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved {len(datasets)} datasets -> {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Search for public ML training datasets")
    parser.add_argument("--query", required=True, help="Description of images or labels needed")
    parser.add_argument("--out", default="located_datasets.md", help="Output markdown file")
    args = parser.parse_args()

    print(f"Searching HuggingFace Hub for: {args.query!r}")
    hf_results = search_huggingface(args.query)
    print(f"  -> {len(hf_results)} results")

    print(f"Querying LLM for known datasets...")
    llm_results = search_llm(args.query)
    print(f"  -> {len(llm_results)} results")

    # Deduplicate by lowercase name
    seen: set[str] = set()
    all_datasets: list[dict] = []
    for ds in llm_results + hf_results:
        key = ds.get("name", "").lower().strip()
        if key and key not in seen:
            seen.add(key)
            all_datasets.append(ds)

    write_markdown(all_datasets, args.query, Path(args.out))


if __name__ == "__main__":
    main()
