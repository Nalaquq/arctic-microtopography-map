#!/usr/bin/env python3
"""Offline tests for recall_check.py and openalex_harvest.py. Run: python3 test_scripts.py"""
import csv
import io
import os
import sys
import tempfile
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recall_check as rc  # noqa: E402
import openalex_harvest as oh  # noqa: E402

SEEDS = os.path.join(HERE, "..", "03_templates", "seed_set_v0.1.csv")


def write(path, text, enc="utf-8"):
    with open(path, "w", encoding=enc, newline="") as fh:
        fh.write(text)


def test_normalisers():
    assert rc.norm_doi("https://doi.org/10.5194/TC-13-237-2019.") == "10.5194/tc-13-237-2019"
    assert rc.norm_doi("DOI: 10.1002/2013WR014283") == "10.1002/2013wr014283"
    assert rc.norm_doi("") == ""
    assert rc.norm_title("Brief communication: Rapid <i>ML</i>-based...") == "brief communication rapid ml based"


def test_readers_and_recall():
    seeds = list(csv.DictReader(open(SEEDS, encoding="utf-8-sig")))
    s = {r["seed_id"]: r for r in seeds}
    with tempfile.TemporaryDirectory() as d:
        # WoS tab-delimited, UTF-8 with BOM: DOI match for SEED-03, title-only match for SEED-26 (no DOI)
        wos = "PT\tAU\tTI\tPY\tDI\n"
        wos += f"J\tAbolt, C\t{s['SEED-03']['title']}\t2019\t{s['SEED-03']['doi'].upper()}\n"
        wos += f"J\tHubbard, S\t{s['SEED-26']['title']}\t2013\t\n"
        wos += "J\tX, Y\tAn unrelated paper on glaciers\t2020\t10.1000/xyz\n"
        write(os.path.join(d, "savedrecs.txt"), "﻿" + wos)
        # Scopus CSV: fuzzy title (punctuation and one-word change) for SEED-10, DOI for SEED-19
        t10 = s["SEED-10"]["title"].replace("Geomorphon", "geomorphons")
        sco = io.StringIO()
        w = csv.writer(sco)
        w.writerow(["Authors", "Title", "Year", "DOI"])
        w.writerow(["Wen A.", t10, "2025", ""])
        w.writerow(["Riihimaki H.", "TWI paper", "2021", "https://doi.org/" + s["SEED-19"]["doi"]])
        write(os.path.join(d, "scopus.csv"), sco.getvalue())
        # RIS: SEED-01 by DOI
        ris = f"TY  - JOUR\nTI  - Something\nPY  - 2014\nDO  - {s['SEED-01']['doi']}\nER  - \n"
        write(os.path.join(d, "georef.ris"), ris)
        # BibTeX: SEED-05 by DOI
        bib = "@article{dv23,\n  title = {Hillslope-channel transitions},\n  doi = {" + s["SEED-05"]["doi"] + "},\n  year = {2023},\n}\n"
        write(os.path.join(d, "x.bib"), bib)
        rep = os.path.join(d, "rep.csv")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc.main(["--seeds", SEEDS, "--report", rep] + [os.path.join(d, f) for f in ("savedrecs.txt", "scopus.csv", "georef.ris", "x.bib")])
        got = {r["seed_id"]: r for r in csv.DictReader(open(rep))}
        assert got["SEED-03"]["matched_by"] == "doi", got["SEED-03"]
        assert got["SEED-26"]["matched_by"] == "title", got["SEED-26"]
        assert got["SEED-10"]["matched_by"] == "fuzzy title", got["SEED-10"]
        assert got["SEED-19"]["matched_by"] == "doi"
        assert got["SEED-01"]["matched_by"] == "doi"
        assert got["SEED-05"]["matched_by"] == "doi"
        assert got["SEED-02"]["retrieved"] == "no"
        assert "core - all" in buf.getvalue()
        hits = sum(r["retrieved"] == "yes" for r in got.values())
        assert hits == 6, hits


def test_diagnose_terms():
    import search_blocks as sb
    txt = "We derived slope and TPI from a 0.5 m lidar DTM across ice-wedge polygons near Utqiagvik, Alaska."
    d = rc.diagnose(txt, sb.BLOCKS)
    assert d["A"] and d["B"] and d["C"], d
    d2 = rc.diagnose("Canopy height from airborne lidar in a temperate forest.", sb.BLOCKS)
    assert not d2["A"] and d2["B"] and not d2["C"], d2
    # hyphen/space equivalence and wildcard inside phrase
    assert rc.term_regex('"ice wedge*"').search("ice-wedges")
    assert rc.term_regex("kilpisj*").search("Kilpisjarvi")
    assert not rc.term_regex("TLS").search("bottles")


def test_openalex_queries():
    import search_blocks as sb
    qs = oh.split_queries([sb.A, sb.B, sb.C])
    assert len(qs) >= 2
    for q in qs:
        assert len(oh.build_url(q, cursor="X" * 40)) <= oh.URL_LIMIT
    # union of the split block equals the original block (distributive split)
    rebuilt = {k: set() for k in range(3)}
    for q in qs:
        for k in range(3):
            rebuilt[k].update(q[k])
    assert rebuilt[0] == set(sb.A) and rebuilt[1] == set(sb.B) and rebuilt[2] == set(sb.C)
    assert oh.oa_term('"ice wedge*"') == '"ice wedge"'
    assert oh.oa_term("palsa*") == "palsa*"
    assert oh.oa_terms('"low-cent*"') == ['"low-centered"', '"low-centred"', '"low-center"', '"low-centre"']
    # every phrase wildcard is either expanded explicitly or ends in a fragment that stemming can match
    import re as _re
    for t in sb.A + sb.B + sb.C:
        if t.startswith('"') and t.endswith('*"') and t not in sb.OA_EXPAND:
            last = t.strip('"').rstrip("*").split()[-1].split("-")[-1]
            assert _re.match(r"^[a-z]+$", last.lower()), t
            assert last.lower() in {"wedge", "latitude", "plateau", "boil", "hummock", "cloud", "model", "survey",
                                    "attribute", "variable", "parameter", "derivative", "feature", "metric",
                                    "gradient", "track", "polygon", "rim", "form"}, f"check stemming for {t}"
    url = oh.build_url(qs[0], mailto="a@b.org")
    assert "title_and_abstract.search:(" in url and "%20OR%20" in url and "mailto=a%40b.org" in url


def test_openalex_rows():
    inv = {"Ice": [0], "wedge": [1], "polygons": [2], "matter.": [3]}
    assert oh.reconstruct_abstract(inv) == "Ice wedge polygons matter."
    w = {"id": "https://openalex.org/W123", "doi": "https://doi.org/10.1/abc", "display_name": "T",
         "publication_year": 2020, "type": "article", "primary_location": {"source": {"display_name": "J"}},
         "authorships": [{"author": {"display_name": "A. Author"}}], "abstract_inverted_index": inv}
    r = oh.row_from_work(w)
    assert r["openalex_id"] == "W123" and r["doi"] == "10.1/abc" and r["venue"] == "J" and r["first_author"] == "A. Author"
    assert oh.row_from_work({"id": None, "primary_location": None})["venue"] == ""


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok ", name)
    print("all tests passed")
