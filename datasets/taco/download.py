"""
Download TACO (Trash Annotations in Context) dataset.
Images are downloaded from Flickr via the official TACO download script.
"""
import subprocess
import sys
import json
import shutil
from pathlib import Path

OUT_DIR = Path(__file__).parent
REPO_DIR = OUT_DIR / "_taco_repo"

# Clone TACO repo
if not REPO_DIR.exists():
    print("Cloning TACO repository...")
    subprocess.run(
        ["git", "clone", "--depth=1", "https://github.com/pedropro/TACO.git", str(REPO_DIR)],
        check=True,
    )
else:
    print("TACO repo already cloned.")

# Install TACO requirements
req_file = REPO_DIR / "requirements.txt"
if req_file.exists():
    print("Installing TACO requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file), "-q"], check=True)

# Run the official download script from the repo ROOT (reads ./data/annotations.json)
print("Downloading TACO images from Flickr (1500 images, may take a while)...")
subprocess.run(
    [sys.executable, "download.py"],
    cwd=str(REPO_DIR),  # must run from repo root
    check=False,
)

# Copy results to standard layout
images_dst = OUT_DIR / "images"
annotations_dst = OUT_DIR / "annotations"
images_dst.mkdir(exist_ok=True)
annotations_dst.mkdir(exist_ok=True)

data_dir = REPO_DIR / "data"

# Copy annotation JSON files
for ann in data_dir.glob("*.json"):
    shutil.copy(ann, annotations_dst / ann.name)
    print(f"Copied annotation: {ann.name}")

# Copy all downloaded images (nested in batch folders)
img_count = 0
for img in data_dir.rglob("*.jpg"):
    dest = images_dst / img.name
    if not dest.exists():
        shutil.copy(img, dest)
        img_count += 1

print(f"\nDone. Copied {img_count} images to {images_dst}")
stats = {"total_images": img_count, "annotation_format": "COCO", "license": "CC BY 4.0"}
(OUT_DIR / "stats.json").write_text(json.dumps(stats, indent=2))
