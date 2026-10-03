#!/usr/bin/env bash
# Rebuild every generated file from its source, from the repository root:
#   bash tools/build_all.sh
# Needs Python 3 (standard library) and Node.js with the "docx" package (npm install, in tools/).
# Sources -> outputs:
#   tools/build_templates.py            -> 03_templates/*.csv (codebook, extraction tables, seed set, logs)
#   04_scripts/search_blocks.py         -> 02_protocol/search_strings_v0.1.md, protocol Appendix A
#   tools/src/protocol_src.md (+ above) -> 02_protocol/Review_Protocol_v$PROTO_VER.md -> .docx
#   01_plan/Research_Plan_v$PLAN_VER.md       -> 01_plan/Research_Plan_v$PLAN_VER.docx
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# Current versions: bump these when a document changes, and move the old files to archive/.
export PROTO_VER="0.2"
PLAN_VER="1.2"
cd "$ROOT/tools"
mkdir -p build

python3 build_templates.py
python3 build_search_md.py
python3 assemble.py

PROTO_META='{"doc_title":"Arctic microtopography systematic map - protocol v'"$PROTO_VER"'","doc_description":"Protocol for a systematic map of how terrain variables and microforms are computed from high-resolution elevation data in Arctic and subarctic landscapes","header_text":"Arctic microtopography systematic map - protocol v'"$PROTO_VER"' (draft for registration)","footer_text":"Protocol v'"$PROTO_VER"' | 3 October 2026 | Draft, not registered","titlepage":{"kicker":"SYSTEMATIC MAP PROTOCOL","subtitle":"Arctic DEM Microtopography project - Stage S1 draft","contents":true},"break_before":["References","Appendix A"]}'
PLAN_META='{"doc_title":"Arctic Tundra Microtopography Benchmark - Research Plan v'"$PLAN_VER"'","doc_description":"Integrated meta-review, benchmark study and article development plan","header_text":"Arctic tundra microtopography benchmark - working research plan v'"$PLAN_VER"'","footer_text":"Research Plan v'"$PLAN_VER"' | 3 October 2026","title_split":"(?<=:)\\s+","titlepage":{"kicker":"WORKING RESEARCH PLAN - VERSION '"$PLAN_VER"'","subtitle":"Companion files: Review Protocol v'"$PROTO_VER"' | State-of-Field Dossier v0.3 | Evidence Matrix v0.3 | Search Log v0.3 | templates and scripts in this repository","contents":true},"break_before":["References"]}'

python3 md2blocks.py "$ROOT/02_protocol/Review_Protocol_v$PROTO_VER.md" build/protocol.json "$PROTO_META"
node render2.js build/protocol.json "$ROOT/02_protocol/Review_Protocol_v$PROTO_VER.docx"
python3 fix_pbdr.py "$ROOT/02_protocol/Review_Protocol_v$PROTO_VER.docx"

python3 md2blocks.py "$ROOT/01_plan/Research_Plan_v$PLAN_VER.md" build/plan.json "$PLAN_META"
node render2.js build/plan.json "$ROOT/01_plan/Research_Plan_v$PLAN_VER.docx"
python3 fix_pbdr.py "$ROOT/01_plan/Research_Plan_v$PLAN_VER.docx"

python3 "$ROOT/04_scripts/test_scripts.py"
find "$ROOT" -name "__pycache__" -prune -exec rm -rf {} +
echo "build complete"
