# -*- coding: utf-8 -*-
"""Render search_strings_v0.1.md and the protocol's Appendix A from search_blocks.py."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]  # repository root
sys.path.insert(0, str(ROOT / "04_scripts"))
import search_blocks as sb  # noqa: E402
import openalex_harvest as oh  # noqa: E402


def code(s):
    return "```\n" + s + "\n```"


def appendix_a(h="###", hh="####"):
    L = []
    L.append(f"{h} A.1 Concept blocks ({sb.VERSION})")
    L.append("Each block is one OR-group; the blocks are combined with AND. No date, language or document-type limits.")
    L.append(f"**Block A – Arctic, subarctic and permafrost context** ({len(sb.A)} terms)")
    L.append(code(sb.ors(sb.A)))
    L.append(f"**Block B – Elevation data** ({len(sb.B)} terms; the first {len(sb.B_HR)} are the high-resolution subset B_hr)")
    L.append(code(sb.ors(sb.B)))
    L.append(f"**Block C – Terrain variables and microtopography** ({len(sb.C)} terms; the first {len(sb.C_MICRO)} are the microform subset C_micro)")
    L.append(code(sb.ors(sb.C)))
    L.append(f"{h} A.2 Platform syntax")
    L.append(f"{hh} Web of Science Core Collection (Advanced Search)")
    L.append(code(sb.wos()))
    L.append("TS searches title, abstract, author keywords and Keywords Plus. Web of Science treats hyphens as spaces and needs at least three characters before a right-hand wildcard; there is no limit on Boolean operators in TS searches.")
    L.append(f"{hh} Scopus (Advanced document search)")
    L.append(code(sb.scopus()))
    L.append(f"{hh} GeoRef – EBSCOhost")
    L.append(code(sb.ebsco()))
    L.append(f"{hh} GeoRef or ProQuest Dissertations & Theses – ProQuest")
    L.append(code(sb.proquest()))
    L.append(f"{hh} OpenAlex (API; run with openalex_harvest.py)")
    L.append(code(sb.openalex()))
    L.append("OpenAlex needs upper-case AND/OR/NOT and at least three characters before a wildcard, and it stems search terms. Its documentation does not say whether wildcards work inside quoted phrases, so the script expands such phrases to explicit variants where stemming cannot recover the word, and otherwise drops the trailing wildcard. "
             f"With the v0.1 blocks it runs {len(oh.split_queries([sb.A, sb.B, sb.C]))} sub-queries. Expansions:")
    L.append(code("\n".join(f"{k} -> {' OR '.join(v)}" for k, v in sb.OA_EXPAND.items())))
    L.append(f"{hh} Google Scholar (Publish or Perish; first 300 results per query, by relevance)")
    L.append(code("\n".join(f"GS{i}: {q}" for i, q in enumerate(sb.GOOGLE_SCHOLAR, 1))))
    L.append(f"{hh} OSTI.gov")
    L.append(code(sb.OSTI))
    L.append(f"{h} A.3 Two-arm restriction (only if A AND B AND C exceeds 8,000 unique records)")
    L.append("Arm 1 keeps every elevation term but only microform vocabulary. Arm 2 keeps every terrain-variable term but only high-resolution elevation terms. Adopt only if the recall targets in 5.3 still hold.")
    L.append(code(sb.two_arm()))
    L.append(f"{h} A.4 Notes for Stage S1")
    L.append("- Confirm every core seed at full text before testing, and add experts' key studies to the validation set.")
    L.append("- Check whether EBSCOhost and ProQuest accept wildcards inside quoted phrases. If not, expand those phrases to explicit variants and log the change.")
    L.append("- Export full records with abstracts: Web of Science full record (tab-delimited, UTF-8), Scopus CSV with abstracts, EBSCOhost or ProQuest RIS.")
    L.append("- Log the exact string as run, the date, the platform and the hit count in search_log_v0.1.csv.")
    L.append("- Run recall_check.py on each export and on their union; diagnose every missed seed with --diagnose.")
    L.append(f"{h} A.5 Novelty search for gate criterion G4 (Stage S6)")
    L.append("Run in Web of Science and Scopus with no area block, so that benchmarks outside the Arctic are found. Screen for studies that benchmark the full chain against known truth.")
    L.append(code(sb.novelty()))
    return "\n\n".join(L)


def appendix_a_compact():
    n_sub = len(oh.split_queries([sb.A, sb.B, sb.C]))
    L = []
    L.append(f"### A.1 Concept blocks ({sb.VERSION})")
    L.append("Each block is one OR-group, and the three blocks are combined with AND. There are no date, language or document-type limits. Fully expanded strings for every platform are in search_strings_v0.1.md.")
    L.append(f"**Block A – Arctic, subarctic and permafrost context** ({len(sb.A)} terms)")
    L.append(code(sb.ors(sb.A)))
    L.append(f'**Block B – Elevation data** ({len(sb.B)} terms; the first {len(sb.B_HR)}, from `lidar` to `"high resolution topograph*"`, form the high-resolution subset B_hr)')
    L.append(code(sb.ors(sb.B)))
    L.append(f'**Block C – Terrain variables and microtopography** ({len(sb.C)} terms; the first {len(sb.C_MICRO)}, from `microtopograph*` to `"landform mapping"`, form the microform subset C_micro; the rest form C_generic)')
    L.append(code(sb.ors(sb.C)))
    L.append("### A.2 Platform syntax")
    L.append("| Platform | Fields | Combination |\n| --- | --- | --- |\n"
             "| Web of Science Core Collection | TS (title, abstract, author keywords, Keywords Plus) | TS=(A) AND TS=(B) AND TS=(C) |\n"
             "| Scopus | TITLE-ABS-KEY | TITLE-ABS-KEY(A) AND TITLE-ABS-KEY(B) AND TITLE-ABS-KEY(C) |\n"
             "| GeoRef (EBSCOhost) | TI, AB, SU | (TI (A) OR AB (A) OR SU (A)) AND the same for B and C |\n"
             "| GeoRef or PQDT (ProQuest) | noft (all fields except full text) | noft(A) AND noft(B) AND noft(C) |\n"
             f"| OpenAlex API | title_and_abstract.search | one filter per block; split into {n_sub} sub-queries by openalex_harvest.py |")
    L.append("Web of Science treats hyphens as spaces and needs at least three characters before a right-hand wildcard; it sets no limit on Boolean operators in TS searches. OpenAlex needs upper-case operators and stems terms. Because its documentation does not say whether wildcards work inside quoted phrases, the script expands such phrases to explicit variants where stemming cannot recover the word (listed in search_strings_v0.1.md).")
    L.append("**Google Scholar** (Publish or Perish; first 300 results per query, by relevance) and **OSTI.gov**:")
    L.append(code("\n".join(f"GS{i}: {q}" for i, q in enumerate(sb.GOOGLE_SCHOLAR, 1)) + "\nOSTI: " + sb.OSTI))
    L.append("### A.3 Two-arm restriction")
    L.append("Used only if A AND B AND C returns more than 8,000 unique records after deduplication. Arm 1 = A AND B AND C_micro. Arm 2 = A AND B_hr AND C_generic. It is adopted only if the recall targets in 5.3 still hold.")
    L.append("### A.4 Notes for Stage S1")
    L.append("- Confirm every core seed at full text before testing, and add experts' key studies to the validation set.\n"
             "- Check whether EBSCOhost and ProQuest accept wildcards inside quoted phrases; if not, expand the phrases and log the change.\n"
             "- Export full records with abstracts: Web of Science tab-delimited (UTF-8), Scopus CSV, EBSCOhost or ProQuest RIS.\n"
             "- Log the exact string as run, date, platform and hit count in search_log_v0.1.csv.\n"
             "- Run recall_check.py on each export and on their union, and diagnose each missed seed with --diagnose.")
    L.append("### A.5 Novelty search for gate criterion G4 (Stage S6)")
    L.append("Run in Web of Science and Scopus with no area block, so that benchmarks outside the Arctic are found: B_hr AND C_generic AND D, where D is:")
    L.append(code(sb.ors(sb.D)))
    return "\n\n".join(L)


if __name__ == "__main__":
    head = (f"# Search strings {sb.VERSION} – Arctic microtopography systematic map\n\n"
            "Development version for Stage S1 testing (3 October 2026). Final strings become v1.0 at registration. "
            "Generated from search_blocks.py, which the scripts also use, so every platform string comes from one source.\n\n")
    md = head + appendix_a(h="##", hh="###") + "\n"
    open(ROOT / "02_protocol" / "search_strings_v0.1.md", "w").write(md)
    (ROOT / "tools" / "build").mkdir(exist_ok=True)
    open(ROOT / "tools" / "build" / "appendix_a.md", "w").write(appendix_a_compact() + "\n")
    print(len(md), "chars written")
