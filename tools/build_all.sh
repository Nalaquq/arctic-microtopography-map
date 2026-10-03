#!/usr/bin/env bash
# Rebuild every generated file from its source, from the repository root:
#   bash tools/build_all.sh
# Needs Python 3 (standard library) and Node.js with the "docx" package (npm install, in tools/).
# Sources -> outputs:
#   tools/build_templates.py            -> 03_templates/*.csv (codebook, extraction tables, seed set, logs)
#   04_scripts/search_blocks.py         -> 02_protocol/search_strings_v0.1.md, protocol Appendix A
#   tools/src/protocol_src.md (+ above) -> 02_protocol/Review_Protocol_v0.1.md -> .docx
#   01_plan/Research_Plan_v1.1.md       -> 01_plan/Research_Plan_v1.1.docx
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/tools"
mkdir -p build

python3 build_templates.py
python3 build_search_md.py
python3 assemble.py

PROTO_META='{"doc_title":"Arctic microtopography systematic map - protocol v0.1","doc_description":"Protocol for a systematic map of how terrain variables and microforms are computed from high-resolution elevation data in Arctic and subarctic landscapes","header_text":"Arctic microtopography systematic map - protocol v0.1 (draft for registration)","footer_text":"Protocol v0.1 | 3 October 2026 | Draft, not registered","titlepage":{"kicker":"SYSTEMATIC MAP PROTOCOL","subtitle":"Arctic DEM Microtopography project - Stage S0","contents":true},"break_before":["References","Appendix A"]}'
PLAN_META='{"doc_title":"Arctic Tundra Microtopography Benchmark - Research Plan v1.1","doc_description":"Integrated meta-review, benchmark study and article development plan, version 1.1","header_text":"Arctic tundra microtopography benchmark - working research plan v1.1","footer_text":"Research Plan v1.1 | 3 October 2026 | Supersedes v1.0","title_split":"(?<=:)\\s+","titlepage":{"kicker":"WORKING RESEARCH PLAN - VERSION 1.1","subtitle":"Companion files: Review Protocol v0.1 | State-of-Field Dossier v0.3 | Evidence Matrix v0.3 | Search Log v0.3 | Stage S0 templates and scripts","contents":true},"break_before":["References"]}'

python3 md2blocks.py "$ROOT/02_protocol/Review_Protocol_v0.1.md" build/protocol.json "$PROTO_META"
node render2.js build/protocol.json "$ROOT/02_protocol/Review_Protocol_v0.1.docx"
python3 fix_pbdr.py "$ROOT/02_protocol/Review_Protocol_v0.1.docx"

python3 md2blocks.py "$ROOT/01_plan/Research_Plan_v1.1.md" build/plan.json "$PLAN_META"
node render2.js build/plan.json "$ROOT/01_plan/Research_Plan_v1.1.docx"
python3 fix_pbdr.py "$ROOT/01_plan/Research_Plan_v1.1.docx"

python3 "$ROOT/04_scripts/test_scripts.py"
find "$ROOT" -name "__pycache__" -prune -exec rm -rf {} +
echo "build complete"
