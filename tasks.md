# Tasks

Step-by-step task instructions for the current work in this repository.

---

## Task 1 — Dataset Preparation

**Goal:** Collect at least 1000 labeled images of street trash bins from public datasets, suitable for training/evaluating a bin fill-level and overflow detector. Store each dataset in its own subfolder under `datasets/` and document all sources in `datasets/README.md`.

### Target image criteria
- Outdoor street or courtyard scenes (CCTV-style angle preferred)
- Rectangular/wheeled dumpsters (the kind in `samples/empty`, `samples/full`, `samples/critical`)
- Various lighting, weather, and image quality conditions
- Exclude: indoor bins, underground bins, product catalog images (same rules as `invalid/` samples)

### Candidate datasets to find and evaluate
Search the following sources for relevant datasets:

| Source | Search terms |
|--------|-------------|
| [Roboflow Universe](https://universe.roboflow.com) | `trash bin detection`, `dumpster detection`, `garbage bin overflow`, `waste bin` |
| [Kaggle](https://kaggle.com) | `trash bin detection`, `garbage overflow`, `waste management CCTV` |
| [TACO](http://tacodataset.org) | Evaluate for street bin images with litter context |
| [Papers With Code](https://paperswithcode.com/datasets) | `waste detection`, `bin detection` |
| [Google Open Images](https://storage.googleapis.com/openimages/web/index.html) | Filter for `Waste container`, `Trash` labels |

### Substeps

1. **Search & evaluate** each source above. For each candidate dataset record:
   - Dataset name and public URL
   - License (CC0, CC-BY, MIT, or other — must allow use for ML training)
   - Total image count and labeled image count
   - Annotation format (YOLO, COCO JSON, Pascal VOC, etc.)
   - Relevance score — does it match our target criteria?

2. **Select datasets** totalling ≥ 1000 relevant images across all sources.

3. **Download** each selected dataset into its own folder:
   ```
   datasets/
     <dataset-slug>/        # e.g. roboflow-trash-bin-detection/
       images/
       labels/              # annotations in original format
       README.md            # auto-generated or provided metadata
   ```

4. **Create `datasets/README.md`** with a summary table:

   | Folder | Dataset name | Source URL | License | Images | Annotations | Notes |
   |--------|-------------|-----------|---------|--------|------------|-------|
   | ...    | ...         | ...       | ...     | ...    | ...        | ...   |

   Include total image count at the bottom.

5. **Commit** each dataset folder separately with a message like:
   `datasets: add <dataset-name> — N images, <annotation-format> annotations`

### Definition of done
- `datasets/` contains ≥ 1000 images across ≥ 2 datasets
- All datasets have original annotations preserved
- `datasets/README.md` is filled with complete metadata for each source
