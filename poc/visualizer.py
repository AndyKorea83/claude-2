"""
Draws detection bounding boxes on images.

Color scheme:
  RED    — valid trash bins (empty / full / overfilled), label shows classification
  ORANGE — garbage on the ground
  PURPLE — invalid bin type
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# (R, G, B)
COLORS = {
    "bin_valid": (220, 38, 38),    # red
    "bin_invalid": (147, 51, 234), # purple
    "garbage": (249, 115, 22),     # orange
}

LABEL_BG_ALPHA = 180  # 0-255


def _color_for(detection: dict) -> tuple[int, int, int]:
    if detection["type"] == "garbage":
        return COLORS["garbage"]
    if detection.get("classification") == "invalid":
        return COLORS["bin_invalid"]
    return COLORS["bin_valid"]


def _label_for(detection: dict) -> str:
    conf = int(detection.get("confidence", 0) * 100)
    if detection["type"] == "garbage":
        return f"garbage {conf}%"
    cls = detection.get("classification", "bin").upper()
    return f"{cls} {conf}%"


def draw_detections(image_path: str, detections: list[dict], output_path: str | None = None) -> str:
    """
    Draws boxes on the image and saves result.
    Returns path to the output file.
    """
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    try:
        font = ImageFont.truetype("arial.ttf", size=max(14, h // 40))
        font_small = font
    except OSError:
        font = ImageFont.load_default()
        font_small = font

    border = max(2, min(w, h) // 200)

    for det in detections:
        bbox = det.get("bbox")
        if not bbox or len(bbox) != 4:
            continue

        x1_pct, y1_pct, x2_pct, y2_pct = bbox
        x1 = int(x1_pct / 100 * w)
        y1 = int(y1_pct / 100 * h)
        x2 = int(x2_pct / 100 * w)
        y2 = int(y2_pct / 100 * h)

        color = _color_for(det)
        label = _label_for(det)

        # Box
        draw.rectangle([x1, y1, x2, y2], outline=color + (255,), width=border)

        # Label background
        bbox_text = font_small.getbbox(label)
        tw = bbox_text[2] - bbox_text[0]
        th = bbox_text[3] - bbox_text[1]
        pad = 4
        lx1, ly1 = x1, max(0, y1 - th - pad * 2)
        lx2, ly2 = x1 + tw + pad * 2, y1
        draw.rectangle([lx1, ly1, lx2, ly2], fill=color + (LABEL_BG_ALPHA,))
        draw.text((lx1 + pad, ly1 + pad), label, fill=(255, 255, 255, 255), font=font_small)

    if output_path is None:
        p = Path(image_path)
        output_path = str(p.parent / f"{p.stem}_detected{p.suffix}")

    # Save as JPEG regardless of source format for consistent output
    out = Path(output_path).with_suffix(".jpg")
    img.save(str(out), "JPEG", quality=92)
    return str(out)
