# CLAUDE.md – Arctic microtopography project

## What this project is

- **Paper 1:** a registered systematic map of how Arctic and subarctic studies compute terrain variables and delineate
  microforms from elevation data at 5 m or finer, with a reporting audit. Target journal: The Cryosphere (research
  article); alternative: Permafrost and Periglacial Processes.
- **Paper 2:** a practice-weighted benchmark of the LiDAR-to-terrain-variable chain on USDA SCINet, run only if Paper 1's
  go/no-go gate (protocol section 10) passes.
- Lead reviewer: S. Gleason. Second reviewer: a student collaborator.

## Start every session here

Read `PROJECT_STATUS.md` first: current stage, decisions, open questions and next actions. At every save point, update
it and `CHANGELOG.md`, bump document versions, commit, and tag the stage (`S1`, `S2`, …). Stages S0–S7 are defined in
protocol section 11.

## Sources and generated files

| To change | Edit this | Then run |
| --- | --- | --- |
| Protocol | `tools/src/protocol_src.md` (`{{…}}` placeholders are filled by `tools/assemble.py`) | `bash tools/build_all.sh` |
| Research plan | `01_plan/Research_Plan_v<ver>.md` | `bash tools/build_all.sh` |
| Search strings | `04_scripts/search_blocks.py` only | `bash tools/build_all.sh` |
| Codebook and templates | `tools/build_templates.py` | `bash tools/build_all.sh` |

Never edit generated files by hand: `02_protocol/Review_Protocol_v*.md` and `.docx`, `02_protocol/search_strings_*.md`,
`03_templates/*.csv`, `01_plan/*.docx`. To bump a version, change `PROTO_VER` or `PLAN_VER` in `tools/build_all.sh`, move
the superseded files to `archive/`, and add a row to the protocol's amendments table (section 12) or the plan's change log.

## Rules that protect the review

- After protocol v1.0 is registered, eligibility, search strings, gate thresholds (G1–G5) and recall targets change only
  through a dated amendment row, reported as a deviation.
- Do not look at or tune strings against validation seeds (`split = validation` in `03_templates/seed_set_v0.1.csv`);
  test them once, as protocol section 5.3 says.
- Raw exports from Web of Science, Scopus, GeoRef or PQDT go in `data/raw_exports/`, which is git-ignored. Never commit
  them; their licences forbid redistribution.
- Log every database search in `03_templates/search_log_v0.1.csv`: date, string version, platform, hit count, export file.
- Never add a reference from memory. Check the DOI, venue and year at the publisher or in a database first, and mark
  anything unverified "to confirm".
- AI screening follows protocol sections 6.3–6.4: the LLM may exclude only below the human stopping point and only after
  validation, and it is never used at full text. Record the model name, version, settings and dates.
- Screening decisions and coded data are research records: never overwrite a human decision; add rows or columns.

## Writing style

British spelling (metres, organise), plain words, sentences under about 25 words, numbers with units. The Cryosphere's
research articles are typically up to 12 journal pages with at most 80 references and a 150–250-word abstract, so the
full list of included studies belongs in the data release.

## Commands

```bash
python3 04_scripts/test_scripts.py                    # offline tests
bash tools/build_all.sh                               # rebuild generated files (run `npm install` in tools/ once)
python3 04_scripts/openalex_harvest.py --count --mailto <email>
python3 04_scripts/recall_check.py --seeds 03_templates/seed_set_v0.1.csv <exports>
```

## Environment

Fedora, VS Code and Claude Code on the command line. Scripts use the Python 3 standard library; Word rendering needs
Node.js and the `docx` package (`tools/package.json`). Heavy computation for Paper 2 runs on USDA SCINet.
