"""
Download Open Images v7 "Waste container" images using fiftyone.
"""
import json
import shutil
from pathlib import Path

import fiftyone as fo
import fiftyone.zoo as foz

OUT_DIR = Path(__file__).parent
IMAGES_DIR = OUT_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

total = 0
splits = {}

for split, max_s in [("validation", None), ("train", 1000)]:
    kwargs = dict(
        split=split,
        label_types=["detections"],
        classes=["Waste container"],
        dataset_name=f"oi-waste-{split}",
        overwrite=True,
    )
    if max_s:
        kwargs["max_samples"] = max_s

    print(f"Downloading {split} split...")
    ds = foz.load_zoo_dataset("open-images-v7", **kwargs)
    n = len(ds)
    print(f"  {split}: {n} samples")

    copied = 0
    for sample in ds:
        src = Path(sample.filepath)
        dst = IMAGES_DIR / src.name
        if src.exists() and not dst.exists():
            shutil.copy(src, dst)
            copied += 1
    print(f"  Copied {copied} new images")
    splits[split] = n
    total += n

print(f"\nTotal images: {total}")

stats = {
    "total_images": total,
    "classes": ["Waste container"],
    "splits": splits,
}
(OUT_DIR / "stats.json").write_text(json.dumps(stats, indent=2))
print("Done.")
