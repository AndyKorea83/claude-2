"""
CLI entry point.

Usage:
  python run.py samples/critical/1.jpg          # single image
  python run.py samples/critical/               # all images in a folder
  python run.py samples/                        # all subfolders recursively
"""

import sys
import json
from pathlib import Path

from detector import detect
from visualizer import draw_detections

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


def process_image(image_path: Path) -> None:
    print(f"\n>> {image_path}")
    result = detect(str(image_path))

    detections = result.get("detections", [])
    scene = result.get("scene_notes", "")

    print(f"   Scene: {scene}")
    print(f"   Detections: {len(detections)}")
    for d in detections:
        conf = int(d.get("confidence", 0) * 100)
        cls = d.get("classification", "")
        notes = d.get("notes", "")
        tag = f"{d['type']}" + (f"/{cls}" if cls else "") + f" {conf}%"
        if notes:
            tag += f" — {notes}"
        print(f"     • {tag}")

    out = draw_detections(str(image_path), detections)
    print(f"   Saved: {out}")

    # Also dump raw JSON alongside output
    json_path = Path(out).with_suffix(".json")
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))


def collect_images(target: Path) -> list[Path]:
    if target.is_file():
        if target.suffix.lower() not in SUPPORTED or target.stem.endswith("_detected"):
            return []
        return [target]
    return sorted(
        p for p in target.rglob("*")
        if p.suffix.lower() in SUPPORTED and not p.stem.endswith("_detected")
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <image_or_folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    images = collect_images(target)

    if not images:
        print(f"No supported images found at: {target}")
        sys.exit(1)

    print(f"Processing {len(images)} image(s)...")
    for img in images:
        try:
            process_image(img)
        except Exception as e:
            print(f"   ERROR: {e}")


if __name__ == "__main__":
    main()
