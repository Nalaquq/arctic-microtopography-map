# Arctic microtopography: systematic map and LiDAR benchmark

How do Arctic and subarctic studies compute slope, curvature, relative elevation and other terrain variables from
high-resolution elevation data, and how completely do they report it? This repository holds the systematic map that
answers that question (Paper 1, target journal The Cryosphere) and, if its go/no-go gate passes, the practice-weighted
benchmark of the LiDAR-to-terrain-variable chain that follows (Paper 2).

**Status:** Stage S0 complete; preparing Stage S1 (search development and recall testing). Protocol v0.2 is a draft
for registration on OSF. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for decisions, open questions and next actions.

**Canonical files:** this repository. The protocol is `02_protocol/Review_Protocol_v0.2.md` (built from
`tools/src/protocol_src.md`); the plan is `01_plan/Research_Plan_v1.2.md`. A shareable Claude doc copy of the protocol
exists for collaborators to read and comment on; it is synced by hand at save points.

## Layout

| Path | Contents |
| --- | --- |
| `CLAUDE.md` | Project context and working rules for Claude Code |
| `PROJECT_STATUS.md` | Current stage, decisions, open questions, next actions |
| `CHANGELOG.md` | What changed at each save point |
| `01_plan/` | Research plan (current version; older versions in `archive/`) |
| `02_protocol/` | Review protocol, search strings, LLM screening prompt (older versions in `archive/`) |
| `03_templates/` | Codebook, extraction tables, screening form, exclusion codes, search log, seed set |
| `04_scripts/` | `search_blocks.py`, `recall_check.py`, `openalex_harvest.py`, `test_scripts.py` |
| `05_scoping_v0.3/` | Frozen scoping deliverables: dossier, evidence matrix (202 records), exploratory search log |
| `data/` | Working data from Stage S2 on; licensed raw exports are never committed (see `data/README.md`) |
| `tools/` | Build scripts that regenerate templates, search strings and Word files (see `tools/README.md`) |

## Set up on Fedora

```bash
sudo dnf install -y git python3 nodejs npm
git clone https://github.com/Nalaquq/arctic-microtopography-map.git
cd arctic-microtopography-map
(cd tools && npm install)              # Word renderer dependency (docx)
python3 04_scripts/test_scripts.py     # offline tests, standard library only
bash tools/build_all.sh                # regenerate templates, strings and Word files
```

Open the folder in VS Code and start Claude Code in the integrated terminal. Claude Code reads `CLAUDE.md`
automatically; begin a session with "resume from PROJECT_STATUS.md".

## Quick start for Stage S1

```bash
python3 04_scripts/openalex_harvest.py --dry-run                         # show the OpenAlex sub-queries
python3 04_scripts/openalex_harvest.py --count --mailto you@example.org  # hit counts per block
python3 04_scripts/openalex_harvest.py --out data/openalex/openalex_S1.csv --mailto you@example.org
python3 04_scripts/recall_check.py --seeds 03_templates/seed_set_v0.1.csv data/raw_exports/* data/openalex/*.csv
```

## Save points

Each stage ends with a save point: `PROJECT_STATUS.md` and `CHANGELOG.md` are updated, document versions are bumped
(superseded files move to `archive/`), and the commit is tagged with the stage name (`S0`, `S1`, …).

## Licence and citation

The repository is public, but no licence has been chosen yet, so all rights are reserved. Choose licences (for example
CC BY 4.0 for documents and data, MIT for code) before inviting reuse; a citation file will be added with the data
release at Stage S7.
