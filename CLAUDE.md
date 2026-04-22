# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tasks

Current step-by-step task instructions are in [`tasks.md`](tasks.md).

## Role

Multimodule ML prototyping agent. Responsibilities:
1. Analyze technical specs and concept context — identify requirements, constraints, and key design decisions.
2. Build a minimal working PoC — validate the concept with the least code necessary. No premature abstractions or production scaffolding.

## Setup

```bash
pip install -r poc/requirements.txt
cp .env.example .env  # then fill in OPENROUTER_API_KEY
```

## Running the PoC

```bash
# Single image
python poc/run.py samples/critical/1.jpg

# Entire folder
python poc/run.py samples/critical/

# All samples
python poc/run.py samples/
```

Output is saved as `<name>_detected.jpg` alongside each source image. Raw JSON detections saved as `<name>_detected.json`. Both are gitignored.

## Git Workflow

- Every meaningful change gets its own commit with a descriptive message explaining what changed and why.
- Stage and commit different folders/modules separately with relevant, scoped commit messages.
- Never batch unrelated changes into a single commit.
- Push to `origin/master` after each logical unit of work.

## Architecture

The PoC is a three-module pipeline in `poc/`:

- **`detector.py`** — encodes the image (base64 or URL), sends it to `google/gemini-2.0-flash-001` via OpenRouter with a structured prompt, returns parsed JSON detections.
- **`visualizer.py`** — takes the detection list and draws colored bounding boxes on the image using Pillow.
- **`run.py`** — CLI glue: collects images from path/folder, calls detect + draw, prints summary. Skips `_detected` output files automatically.

### Detection schema

Each detection: `type` (`bin` | `garbage`), `bbox` ([x1%, y1%, x2%, y2%] normalized 0–100), `classification` (`empty` | `full` | `overfilled` | `invalid`), `confidence` (0–1), `notes`.

### Box colors

| Color | Meaning |
|-------|---------|
| Red | Valid bin (empty / full / overfilled) |
| Orange | Garbage on the ground |
| Purple | Invalid bin type |

### Classification rules (encoded in the prompt)

The prompt uses a 3-step decision tree:
1. **Shape check**: round/cylindrical body → `invalid`
2. **Storage check**: plastic-wrapped or indoor storage → `invalid`
3. **Fill level**: `empty` / `full` / `overfilled` based on visible garbage

See `poc/detector.py` `USER_PROMPT` for the exact wording — prompt engineering is the main tuning lever.

## Samples

See [`samples/README.md`](samples/README.md) for ground-truth class descriptions.
