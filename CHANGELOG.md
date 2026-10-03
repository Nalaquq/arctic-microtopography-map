# Changelog

Newest first. One entry per save point. Version numbers follow each file's own series
(protocol 0.x until registration at 1.0; plan 1.x; templates 0.x).

## Unreleased – preparing Stage S1 (3 October 2026)

- **Changed** protocol v0.1 → v0.2: registration on OSF only (Environmental Evidence is out of scope); the full list of
  included studies is released with the data; the second reviewer is a student collaborator. Amendments table updated.
- **Changed** plan v1.1 → v1.2: Paper 1 targets The Cryosphere as a research article (alternative: Permafrost and
  Periglacial Processes); second reviewer named; the GitHub repository is the canonical copy and work continues in
  Claude Code in VS Code on Fedora. Change log gains a version column.
- **Added** CLAUDE.md (project context and working rules) and Fedora set-up steps in README.md.
- **Moved** superseded documents to `01_plan/archive/` and `02_protocol/archive/`; `tools/build_all.sh` now takes the
  current versions from `PROTO_VER` and `PLAN_VER`.

## S0 package – 3 October 2026

Stage S0 (protocol and setup) of the systematic map.

- **Added** Review Protocol v0.1 (`02_protocol/Review_Protocol_v0.1.docx`, `.md`): systematic-map protocol aligned with
  CEE Guidelines v5.1, ROSES and PRISMA-ScR; eligibility (PCC), sources, three concept blocks, seed-set recall testing,
  AI-assisted screening with human verification, three-table coding, Reporting Completeness Index (13 items),
  synthesis plan, go/no-go gate G1–G5, stages S0–S7 with save points.
- **Added** search strings v0.1 (`02_protocol/search_strings_v0.1.md`) generated from `04_scripts/search_blocks.py`;
  LLM screening prompt v0.1.
- **Added** templates v0.1 (`03_templates/`): codebook (123 fields, sections A–J), extraction tables (studies,
  elevation_inputs, variables), screening form, exclusion codes E1–E9, formal search log with planned searches,
  seed set (21 core seeds split 14 development / 7 validation; 9 boundary; 5 expected exclusions).
- **Reviewed** the protocol with an independent read-through before release; changes made in v0.1 as a result:
  operational area rules (CAVM, 60°N, permafrost zones north of 50°N), exclusion codes reordered, recall targets
  restated with a once-only validation test, a routing table for human and LLM screening, stricter LLM validation
  (30 positives, lower 95% bound 0.85), no LLM at full text, RCI scored per input or variable with NA rules,
  gate criteria G1–G5 sharpened with an ordered decision rule and a separate novelty search, ASTIS added,
  citationchaser described correctly (Lens.org), and OpenAlex phrase wildcards expanded explicitly.
- **Added** scripts (`04_scripts/`): `recall_check.py` (seed recall from WoS/Scopus/RIS/BibTeX/OpenAlex exports, with
  per-block diagnosis of misses), `openalex_harvest.py` (OpenAlex arm with automatic URL-length splitting),
  `test_scripts.py` (offline tests; all pass).
- **Changed** Research Plan v1.0 → v1.1 (`01_plan/Research_Plan_v1.1.docx`, `.md`); see the plan's change log.
  Main changes: Quinhagak/cloudberry application removed; two-paper structure (systematic map, then benchmark);
  Gate A as a pre-specified go/no-go; scale-explicit estimands; synthetic tier with procedural tundra terrain and
  virtual laser scanning; public point clouds only; SCINet workflow; stage-based save points.
- **Carried forward** scoping deliverables v0.3 (`05_scoping_v0.3/`) unchanged.
- **Set up** the GitHub repository: README, `.gitignore` (licensed raw exports excluded), `data/` layout, and
  `tools/` build scripts made path-relative. Recorded two decisions in PROJECT_STATUS.md: the project lives on
  GitHub under the Nalaquq account, and S. Gleason screens with the protocol's single-reviewer fallback.

## Scoping v0.3 – 2 October 2026

- State-of-Field Dossier v0.3 (reviewer appraisal, refinement, evidence update; 31 pages).
- Evidence Matrix v0.3 (202 records; verification status per record).
- Search Log v0.3 (161 exploratory web-index searches; not the formal review log).
- `operator_pilot.py` (closed-form kernel properties and a small synthetic-hummock simulation).
