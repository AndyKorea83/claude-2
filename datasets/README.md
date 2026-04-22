# Datasets

Labeled image datasets for trash bin detection and fill-level classification.

## Summary

| Folder | Dataset | Source | License | Images | Annotations | Notes |
|--------|---------|--------|---------|--------|-------------|-------|
| `open-images-waste-container/` | Open Images v7 — Waste container | [Google Open Images](https://storage.googleapis.com/openimages/web/index.html) | CC BY 4.0 | 1019 | COCO-compatible (bounding boxes) | "Waste container" class; mixed outdoor/indoor |
| `taco/` | TACO — Trash Annotations in Context | [tacodataset.org](http://tacodataset.org) / [GitHub](https://github.com/pedropro/TACO) | CC BY 4.0 | 239 | COCO JSON (segmentation + bbox) | 60 litter categories; partial Flickr availability |

**Total: 1258 images across 2 datasets**

Run `py datasets/search_agent.py --query "..."` to discover additional datasets. See `located_datasets.md` (gitignored, generated on demand) for the full search results.

---

## Dataset Details

### open-images-waste-container

- **Full name**: Open Images v7 — Waste container class
- **Source**: Google Open Images Dataset v7
- **URL**: https://storage.googleapis.com/openimages/web/index.html
- **License**: CC BY 4.0
- **Annotation format**: COCO JSON (`annotations_coco.json`)
- **Classes**: `Waste container`
- **Splits downloaded**: `validation` (19) + `train` (1000)
- **Contents**:
  ```
  images/           JPEG images
  annotations_coco.json   Bounding box annotations
  stats.json        Download summary
  download.py       Reproduction script
  ```

### taco

- **Full name**: TACO — Trash Annotations in Context
- **Source**: http://tacodataset.org
- **GitHub**: https://github.com/pedropro/TACO
- **License**: CC BY 4.0
- **Annotation format**: COCO JSON (instance segmentation + bounding boxes)
- **Classes**: 60 litter categories (bottles, bags, cups, etc.) — bins appear as context
- **Contents**:
  ```
  images/           JPEG images downloaded from Flickr
  annotations/      COCO JSON annotation files
  stats.json        Download summary
  download.py       Reproduction script
  ```

---

## Reproducing Downloads

```bash
# Open Images
cd datasets/open-images-waste-container
py download.py

# TACO
cd datasets/taco
py download.py
```

Both scripts require: `pip install fiftyone requests tqdm`
