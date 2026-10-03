# -*- coding: utf-8 -*-
"""Fill placeholders in protocol_src.md and write the protocol markdown used for the docx and the live doc."""
import csv
from collections import OrderedDict

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]  # repository root
B = str(ROOT / "tools" / "build")
R = str(ROOT)
cb = list(csv.DictReader(open(f"{R}/03_templates/codebook_v0.1.csv", encoding="utf-8")))

# RCI table
DOM = {"R01": "Data", "R02": "Data", "R03": "Data", "R04": "Data", "R05": "DTM", "R06": "DTM", "R07": "DTM",
       "R08": "DTM", "R09": "Derivatives", "R10": "Derivatives", "R11": "Derivatives", "R12": "Derivatives", "R13": "Openness"}
rows = ["| Item | Domain | Credit for |", "| --- | --- | --- |"]
for r in cb:
    if r["section"] == "I" and r["rci_item"]:
        rid = r["rci_item"]
        label = r["label"][len(rid) + 1:]
        rows.append(f"| {rid} | {DOM[rid]} | {label} |")
rci_table = "\n".join(rows)

# Codebook overview
sec = OrderedDict()
for r in cb:
    k = (r["section"], r["section_name"], r["table"])
    sec.setdefault(k, []).append(r["field_name"])
KEY = {
    "A": "study_id, doi, year, publication_type, venue_field",
    "B": "application_domain, terrain_role, region, area_rule, latitude/longitude, permafrost_zone, microforms",
    "C": "source_type, product_name, acquisition_date, point density or GSD, vertical accuracy and metric",
    "D": "surface_type, dtm_builder, ground_filter, gridding_method, native and analysis cell size, hydro-conditioning",
    "E": "variable_family, algorithm (verbatim and coded) with its basis, software and version, window in cells and metres, support type, scales, pre-processing, use, scale rationale",
    "F": "microform_targets, delineation_method, inputs, validation, accuracy",
    "G": "accuracy assessed (elevation and variables), uncertainty propagation, vegetation bias, sensitivity tested and outcome",
    "H": "code and derived-data availability, source data identified",
    "I": "R01 to R13 scores; RCI total and domain means",
    "J": "uncertain fields, author query, notes",
}
rows = ["| Section | Table | Fields | Key fields |", "| --- | --- | --- | --- |"]
for (s, name, table), fields in sec.items():
    rows.append(f"| {s}. {name} | {table} | {len(fields)} | {KEY[s]} |")
overview = ("Three linked tables: studies (one row per study), elevation_inputs (one row per elevation product) and variables "
            "(one row per terrain variable per elevation input). "
            f"The codebook has {len(cb)} fields; every field has a definition, a type and, where closed, a list of allowed values.\n\n"
            + "\n".join(rows))

appendix_a = open(f"{B}/appendix_a.md").read().strip()
prompt = open(f"{R}/02_protocol/llm_screening_prompt_v0.1.md").read().strip()

src = open(ROOT / "tools" / "src" / "protocol_src.md").read()
md = (src.replace("{{RCI_TABLE}}", rci_table).replace("{{CODEBOOK_OVERVIEW}}", overview)
      .replace("{{APPENDIX_A}}", appendix_a).replace("{{LLM_PROMPT}}", "```\n" + prompt + "\n```"))
assert "{{" not in md
VER = __import__("os").environ.get("PROTO_VER", "0.2")
open(f"{R}/02_protocol/Review_Protocol_v{VER}.md", "w").write(md)
print(len(md), "chars;", md.count("\n## "), "level-2 sections")
