# tools

Build scripts that regenerate the project's derived files. Run from the repository root:

```bash
cd tools && npm install && cd ..   # once, for the Word renderer
bash tools/build_all.sh
```

| Source (edit this) | Generated (do not edit by hand) |
| --- | --- |
| `tools/build_templates.py` | `03_templates/*.csv` (codebook, extraction tables, screening form, exclusion codes, search log, seed set) |
| `04_scripts/search_blocks.py` | `02_protocol/search_strings_v0.1.md`, protocol Appendix A |
| `tools/src/protocol_src.md` | `02_protocol/Review_Protocol_v0.1.md` and `.docx` |
| `01_plan/Research_Plan_v1.1.md` | `01_plan/Research_Plan_v1.1.docx` |

`md2blocks.py` turns the project's markdown subset into blocks, `render2.js` writes the Word file, and `fix_pbdr.py`
puts paragraph-border elements in schema order. `build/` holds intermediate files and is not committed.

The live protocol doc (Claude Docs) is the working copy for prose edits. At each save point, edits made there are copied
back into `tools/src/protocol_src.md` and the build is rerun, so the committed files match the doc.
