# Arctic microtopography: systematic map and LiDAR benchmark

How do Arctic and subarctic studies compute slope, curvature, relative elevation and other terrain variables from
high-resolution elevation data, and how completely do they report it? This repository holds the systematic map that
answers that question (Paper 1) and, if its go/no-go gate passes, the practice-weighted benchmark of the
LiDAR-to-terrain-variable chain that follows (Paper 2).

**Status:** Stage S0 complete (3 October 2026). Protocol v0.1 is a draft for registration; Stage S1 (search development
and recall testing) is next. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for decisions, open questions and next actions.

**Live protocol:** "Arctic microtopography systematic map: protocol" (Claude doc,
https://claude.ai/artifact/BFGQ9aNK2kAMXM9bEwqDx1). Private until shared by the owner.

## Layout

| Path | Contents |
| --- | --- |
| `PROJECT_STATUS.md` | Current stage, decisions, open questions, next actions |
| `CHANGELOG.md` | What changed at each save point |
| `01_plan/` | Research plan (v1.1 current; v1.0 kept for reference) |
| `02_protocol/` | Review protocol, search strings, LLM screening prompt |
| `03_templates/` | Codebook, extraction tables, screening form, exclusion codes, search log, seed set |
| `04_scripts/` | `search_blocks.py`, `recall_check.py`, `openalex_harvest.py`, `test_scripts.py` |
| `05_scoping_v0.3/` | Frozen scoping deliverables: dossier, evidence matrix (202 records), exploratory search log |
| `data/` | Working data from Stage S2 on; raw licensed exports are never committed (see `data/README.md`) |
| `tools/` | Build scripts that regenerate the templates, search strings and Word files (see `tools/README.md`) |

## Quick start

```bash
python3 04_scripts/test_scripts.py                       # offline tests
python3 04_scripts/openalex_harvest.py --dry-run         # show OpenAlex sub-queries
python3 04_scripts/openalex_harvest.py --count --mailto you@example.org
python3 04_scripts/recall_check.py --seeds 03_templates/seed_set_v0.1.csv data/raw_exports/*
```

The scripts use the Python 3 standard library only.

## Save points

Each stage ends with a save point: `PROJECT_STATUS.md` and `CHANGELOG.md` are updated, file versions are bumped, and
the commit is tagged with the stage name (`S0`, `S1`, …). To see the project as it was at a stage, check out its tag.

## Licence and citation

No licence has been chosen yet, so all rights are reserved while the repository is private. A licence and a citation
file will be added before the data and code are released with the map (Stage S7).
