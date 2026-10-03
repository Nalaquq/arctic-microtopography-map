#!/usr/bin/env python3
"""Recall check for the Arctic microtopography systematic map (Stage S1).

Reads one or more database exports and reports which seed records they retrieved.
Supported exports: Web of Science tab-delimited (.txt), Scopus or other CSV, RIS (.ris), BibTeX (.bib),
and the CSV written by openalex_harvest.py. Records are matched to seeds by DOI first, then by
normalised title (exact, then fuzzy >= 0.92 with the year within +/- 1 when both years are known).

Usage
  python3 recall_check.py --seeds ../03_templates/seed_set_v0.1.csv exports/*.txt exports/*.csv
  python3 recall_check.py --seeds seed_set_v0.1.csv --report recall_S1-WOS-01.csv savedrecs.txt
  python3 recall_check.py --seeds seed_set_v0.1.csv --diagnose seed_abstracts.csv exports/*

--diagnose takes a CSV with columns doi,title,abstract for the seeds (for example, an
openalex_harvest.py --dois run). For every missed seed it reports which concept block (A, B or C)
has no matching term in the title or abstract, which tells you which block to widen.

Standard library only. Tested offline on synthetic exports (see test_recall_check.py).
"""
import argparse
import csv
import difflib
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.I)


def norm_doi(s):
    if not s:
        return ""
    m = DOI_RE.search(s.strip())
    if not m:
        return ""
    d = m.group(0).lower().rstrip(".,;)]}>\"'")
    return d


def norm_title(s):
    s = (s or "").lower()
    s = re.sub(r"<[^>]+>", " ", s)          # strip markup such as <i>
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def year_of(s):
    m = re.search(r"(19|20)\d{2}", s or "")
    return int(m.group(0)) if m else None


# ----------------------------------------------------------------------------- readers
def _open_text(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-16", "latin-1"):
        try:
            txt = raw.decode(enc)
            if enc == "utf-16" and "\x00" in txt:
                continue
            return txt
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def read_ris(txt):
    recs, cur = [], {}
    for line in txt.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  - ?(.*)$", line)
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "ER":
            recs.append(cur)
            cur = {}
            continue
        if tag in ("TI", "T1") and "title" not in cur:
            cur["title"] = val
        elif tag == "DO":
            cur["doi"] = val
        elif tag in ("PY", "Y1", "DA") and "year" not in cur:
            cur["year"] = val
        elif tag in ("UR", "L2", "N1") and "doi" not in cur and DOI_RE.search(val):
            cur["doi"] = val
    if cur:
        recs.append(cur)
    return recs


def read_bib(txt):
    recs = []
    for entry in re.split(r"\n\s*@", "\n" + txt)[1:]:
        def field(name):
            m = re.search(name + r"\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", entry, re.I | re.S)
            return m.group(1).replace("{", "").replace("}", "") if m else ""
        recs.append({"title": field("title"), "doi": field("doi"), "year": field("year")})
    return recs


def read_delimited(txt):
    first = txt.splitlines()[0] if txt else ""
    delim = "\t" if first.count("\t") > first.count(",") else ","
    rdr = csv.DictReader(io.StringIO(txt), delimiter=delim)
    keys = {k.lower().strip(): k for k in (rdr.fieldnames or []) if k}

    def pick(*names):
        for n in names:
            if n in keys:
                return keys[n]
        return None
    k_doi = pick("doi", "di", "do")                      # Scopus/OpenAlex 'doi', WoS 'DI'
    k_title = pick("title", "ti", "article title", "document title", "display_name")
    k_year = pick("year", "py", "publication_year", "publication year")
    recs = []
    for row in rdr:
        recs.append({"doi": row.get(k_doi, "") if k_doi else "",
                     "title": row.get(k_title, "") if k_title else "",
                     "year": row.get(k_year, "") if k_year else ""})
    return recs


def read_any(path):
    txt = _open_text(path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".ris" or re.search(r"^TY  - ", txt, re.M):
        return read_ris(txt)
    if ext == ".bib" or txt.lstrip().startswith("@"):
        return read_bib(txt)
    return read_delimited(txt)


# ----------------------------------------------------------------------------- matching
def build_index(records):
    by_doi, by_title = {}, {}
    for r in records:
        d = norm_doi(r.get("doi", ""))
        t = norm_title(r.get("title", ""))
        if d:
            by_doi.setdefault(d, r)
        if t:
            by_title.setdefault(t, r)
    return by_doi, by_title


def match_seed(seed, by_doi, by_title, titles_list):
    d = norm_doi(seed.get("doi", ""))
    if d and d in by_doi:
        return "doi"
    t = norm_title(seed.get("title", ""))
    if not t:
        return ""
    if t in by_title:
        return "title"
    sy = year_of(seed.get("year", ""))
    for cand in difflib.get_close_matches(t, titles_list, n=3, cutoff=0.92):
        cy = year_of(by_title[cand].get("year", ""))
        if sy is None or cy is None or abs(sy - cy) <= 1:
            return "fuzzy title"
    return ""


def unique_count(records):
    seen = set()
    for r in records:
        key = norm_doi(r.get("doi", "")) or norm_title(r.get("title", ""))
        if key:
            seen.add(key)
    return len(seen)


# ----------------------------------------------------------------------------- diagnosis
def term_regex(term):
    t = term.strip()
    phrase = t.startswith('"') and t.endswith('"')
    t = t.strip('"')
    parts = re.split(r"[\s\-]+", t)
    rx = []
    for p in parts:
        p_esc = re.escape(p).replace(r"\*", r"\w*").replace(r"\?", r"\w")
        rx.append(p_esc)
    body = r"[\s\-]+".join(rx) if phrase or len(parts) > 1 else rx[0]
    return re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])", re.I)


def diagnose(text, blocks):
    out = {}
    for name, terms in blocks.items():
        hits = [t for t in terms if term_regex(t).search(text)]
        out[name] = hits
    return out


# ----------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exports", nargs="*", help="export files (WoS .txt, CSV, RIS, BibTeX, OpenAlex CSV)")
    ap.add_argument("--seeds", required=True, help="seed_set CSV")
    ap.add_argument("--report", help="write a per-seed CSV report here")
    ap.add_argument("--diagnose", help="CSV with doi,title,abstract for seeds; explains misses by block")
    a = ap.parse_args(argv)

    seeds = list(csv.DictReader(open(a.seeds, encoding="utf-8-sig")))
    all_recs, per_file = [], {}
    for p in a.exports:
        recs = read_any(p)
        per_file[p] = recs
        all_recs.extend(recs)
    by_doi, by_title = build_index(all_recs)
    titles_list = list(by_title.keys())
    file_idx = {p: build_index(r) for p, r in per_file.items()}

    print(f"Exports: {len(a.exports)} file(s); {len(all_recs)} records; ~{unique_count(all_recs)} unique by DOI/title\n")
    results = []
    for s in seeds:
        how = match_seed(s, by_doi, by_title, titles_list)
        where = [os.path.basename(p) for p, (bd, bt) in file_idx.items()
                 if match_seed(s, bd, bt, list(bt.keys()))]
        results.append(dict(seed_id=s["seed_id"], record_id=s.get("record_id", ""), role=s.get("seed_role", ""),
                            split=s.get("split", ""), retrieved="yes" if how else "no", matched_by=how,
                            files=";".join(where), title=s.get("title", "")[:90]))

    def rate(sel):
        sel = list(sel)
        hit = sum(r["retrieved"] == "yes" for r in sel)
        return hit, len(sel), (100.0 * hit / len(sel)) if sel else float("nan")

    core = [r for r in results if r["role"].startswith("core")]
    print("Recall")
    for label, sel in (("core - all", core),
                       ("core - development", [r for r in core if r["split"] == "development"]),
                       ("core - validation", [r for r in core if r["split"] == "validation"]),
                       ("boundary", [r for r in results if r["role"].startswith("boundary")])):
        h, n, pct = rate(sel)
        print(f"  {label:<22} {h:>3}/{n:<3} {pct:5.1f}%")
    print("\nTargets (protocol 5.3): development 100%; validation >= 6/7; core overall >= 19/21.\n")
    for r in results:
        if r["role"].startswith("core") or r["role"].startswith("boundary"):
            flag = "  " if r["retrieved"] == "yes" else "!!"
            print(f"{flag} {r['seed_id']} {r['split']:<11} {r['retrieved']:<3} {r['matched_by']:<11} {r['title']}")

    if a.report:
        with open(a.report, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
            w.writeheader()
            w.writerows(results)
        print(f"\nReport written to {a.report}")

    if a.diagnose:
        import search_blocks as sb  # same blocks as the protocol
        rows = list(csv.DictReader(open(a.diagnose, encoding="utf-8-sig")))
        idx_doi = {norm_doi(r.get("doi", "")): r for r in rows if norm_doi(r.get("doi", ""))}
        idx_t = {norm_title(r.get("title", "")): r for r in rows if r.get("title")}
        print("\nDiagnosis of missed seeds (blocks with no matching term in title + abstract):")
        for r in results:
            if r["retrieved"] == "yes" or not (r["role"].startswith("core") or r["role"].startswith("boundary")):
                continue
            s = next(x for x in seeds if x["seed_id"] == r["seed_id"])
            src = idx_doi.get(norm_doi(s.get("doi", ""))) or idx_t.get(norm_title(s.get("title", "")))
            if not src:
                print(f"  {r['seed_id']}: no abstract supplied")
                continue
            d = diagnose(f"{src.get('title', '')} {src.get('abstract', '')}", sb.BLOCKS)
            missing = [b for b, hits in d.items() if not hits]
            print(f"  {r['seed_id']}: missing blocks {missing or 'none (check indexing or export limits)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
