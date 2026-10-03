# Project status – Arctic DEM microtopography

Last updated: 3 October 2026. **Stage S0 (protocol and setup) is complete; protocol v0.2 and plan v1.2 record the decisions made since. Next: Stage S1 (search development, recall testing, registration).**

This repository (https://github.com/Nalaquq/arctic-microtopography-map) is the canonical copy of every file; work
continues in Claude Code in VS Code on Fedora. A shareable Claude doc copy of the protocol, for collaborators to read and
comment on, is synced by hand at save points: https://claude.ai/artifact/BFGQ9aNK2kAMXM9bEwqDx1

## The project in two sentences

Paper 1 is a registered systematic map of how Arctic and subarctic studies compute terrain variables and delineate
microforms from elevation data at 5 m or finer, with a reporting audit. Paper 2, only if Paper 1's go/no-go gate
passes, is a practice-weighted benchmark of the LiDAR-to-terrain-variable chain on USDA SCINet, with procedural
tundra terrain, virtual laser scanning and public Arctic LiDAR.

## Decisions so far

| Date | Decision | Source |
| --- | --- | --- |
| 2026-10-02 | Not a Quinhagak or cloudberry paper; a methods benchmark of slope and terrain variables for LiDAR-derived Arctic elevation products | S. Gleason |
| 2026-10-02 | Run the benchmark on the USDA SCINet cluster | S. Gleason |
| 2026-10-02 | No new UAS-LiDAR or RTK field campaign; public datasets only | S. Gleason |
| 2026-10-03 | Start with the meta-review (systematic map) as Paper 1, with a go/no-go gate for the benchmark | S. Gleason |
| 2026-10-03 | Save progress in stages as versioned packages, updating the plan along the way | S. Gleason |
| 2026-10-03 | Review type: systematic map (CEE v5.1, ROSES, PRISMA-ScR), registered on OSF Registries (Environmental Evidence is out of scope, so PROCEED is not needed) | Protocol v0.2 |
| 2026-10-03 | Project home: GitHub repository Nalaquq/arctic-microtopography-map (public); work in Claude Code from the command line in VS Code on Fedora | S. Gleason |
| 2026-10-03 | S. Gleason screens every record; a student collaborator is the second reviewer for the 200-record and 20-full-text calibration, the 20% full-text check and the coding pilot | S. Gleason |
| 2026-10-03 | Paper 1 targets The Cryosphere as a research article; Permafrost and Periglacial Processes is the alternative | S. Gleason |

## Open questions for S. Gleason

1. The repository is public: keep it public (open-science record) or make it private until publication? Either way, choose licences before inviting reuse (for example CC BY 4.0 for documents and data, MIT for code).
2. The student collaborator's name, for the protocol's contributions statement, and when they can do the calibration samples.
3. Which licensed platforms can you search: Web of Science, Scopus, GeoRef (EBSCOhost or ProQuest), ProQuest Dissertations & Theses?
4. Who are three to five experts or data providers to ask for key studies?

## Next actions (Stage S1)

1. Confirm the 21 core seeds at full text (seed_set_v0.1.csv); move any that fail to the calibration set.
2. Ask the experts for key studies; add them to the validation set.
3. Run Web of Science, Scopus and GeoRef with strings v0.1 (02_protocol/search_strings_v0.1.md). Export full records with abstracts. Log each run in 03_templates/search_log_v0.1.csv.
4. Run `python3 04_scripts/openalex_harvest.py --count --mailto <email>`, then the full harvest.
5. Run `python3 04_scripts/recall_check.py --seeds 03_templates/seed_set_v0.1.csv <exports>`; revise strings on development seeds only; test validation seeds once.
6. Freeze strings and gate thresholds as protocol v1.0, complete the ROSES form and register. Save the S1 package.

## How to resume in a new session

Open the repository in VS Code on Fedora, start Claude Code in the terminal and say "resume from PROJECT_STATUS.md".
Claude Code reads CLAUDE.md for the working rules. Scripts need Python 3 only (standard library); check them with
`python3 04_scripts/test_scripts.py`. `bash tools/build_all.sh` regenerates every derived file (setup in README.md).

## Repository contents

| Path | What it is |
| --- | --- |
| README.md | What the project is, layout, Fedora setup, quick start |
| CLAUDE.md | Project context and working rules for Claude Code |
| PROJECT_STATUS.md | This file: stage, decisions, open questions, next actions |
| CHANGELOG.md | What changed at each save point |
| 01_plan/Research_Plan_v1.2.md (.docx) | Current research plan with change log; v1.0 and v1.1 in 01_plan/archive/ |
| 02_protocol/Review_Protocol_v0.2.md (.docx) | Systematic-map protocol, draft for registration; v0.1 in 02_protocol/archive/ |
| 02_protocol/search_strings_v0.1.md | Fully expanded strings for every platform |
| 02_protocol/llm_screening_prompt_v0.1.md | Frozen LLM second-screener prompt |
| 03_templates/codebook_v0.1.csv | 123 coding fields with definitions and allowed values |
| 03_templates/extract_*_v0.1.csv | Empty extraction tables: studies, elevation inputs, variables |
| 03_templates/screening_form_v0.1.csv, exclusion_codes_v0.1.csv | Screening log and codes E1–E9 |
| 03_templates/search_log_v0.1.csv | Formal search log with the planned searches |
| 03_templates/seed_set_v0.1.csv | 35 seed records: 21 core (14 development, 7 validation), 9 boundary, 5 expected exclusions |
| 04_scripts/ | search_blocks.py, recall_check.py, openalex_harvest.py, test_scripts.py |
| 05_scoping_v0.3/ | Dossier v0.3, Evidence Matrix v0.3 (202 records: the original 80 plus 122 added), Search Log v0.3, operator_pilot.py (frozen); the original v0.2 dossier and matrix in v0.2_originals/ |
| data/ | Working data from Stage S2 on; licensed raw exports are git-ignored (see data/README.md) |
| tools/ | Build scripts that regenerate templates, search strings and Word files (see tools/README.md) |

## Conventions

- Versions: protocol 0.x until registration at 1.0; plan 1.x; templates 0.x; scoping v0.3 is frozen.
- Names: `<Name>_v<version>.<ext>`; save points are Git tags (`S0`, `S1`, …); optional stage packages `Arctic_Microtopography_<stage>_<YYYY-MM-DD>.zip`.
- Raw database exports are never edited; derived files record the string version used.
- At every save point: update this file and CHANGELOG.md, bump versions, commit and tag the stage.

## Known limitations and items to verify

- The OpenAlex API refused requests (rate limit) from the drafting workspace, so openalex_harvest.py is tested offline only. Run `--count` first.
- Seven core seeds were judged from title or abstract only; confirm them at full text in S1.
- Dataset details marked "to confirm" in plan section 5.2 are checked in the Phase III inventory.
