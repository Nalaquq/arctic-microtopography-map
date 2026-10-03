#!/usr/bin/env python3
"""Harvest the OpenAlex arm of the systematic-map search (Stage S1/S2).

Runs  title_and_abstract.search:(A) AND (B) AND (C)  with the concept blocks in search_blocks.py.
OpenAlex limits a request URL to about 4,000 characters, so the script splits the largest block
into sub-queries until every URL fits, then unions the results by OpenAlex ID. This is valid
because (A1 OR A2) AND B AND C = (A1 AND B AND C) OR (A2 AND B AND C).

OpenAlex notes (help.openalex.org/api/searching, read 3 Oct 2026): AND/OR/NOT must be upper case;
'*' wildcards need at least 3 characters before them; search is stemmed by default. Because the
docs do not say whether wildcards work inside quoted phrases, the script expands such phrases to
explicit variants where stemming cannot recover the word (search_blocks.OA_EXPAND, e.g. "low-cent*" ->
"low-centered" OR "low-centred" ...), and otherwise drops the trailing '*' and relies on stemming
(e.g., "ice wedge*" -> "ice wedge", which also matches "ice wedges").

Usage
  python3 openalex_harvest.py --dry-run                      # show sub-queries and URL lengths
  python3 openalex_harvest.py --count --mailto you@org       # hit counts only
  python3 openalex_harvest.py --out openalex_S1.csv --mailto you@org [--api-key KEY]
  python3 openalex_harvest.py --dois seed_dois.txt --out seed_abstracts.csv   # fetch given DOIs

Output CSV columns: openalex_id, doi, title, year, type, venue, first_author, abstract, subqueries.
Standard library only. Not yet run against the live API from the drafting workspace (requests were
rate-limited there); query building and abstract reconstruction are tested offline.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search_blocks as sb  # noqa: E402

BASE = "https://api.openalex.org/works"
URL_LIMIT = 3800  # stay under the ~4,000-character limit with room for paging parameters
SELECT = "id,doi,display_name,publication_year,type,primary_location,authorships,abstract_inverted_index"


def oa_terms(t):
    """OpenAlex form of one search term, as a list (a phrase wildcard may expand to several phrases)."""
    t = t.strip()
    if t in sb.OA_EXPAND:
        return list(sb.OA_EXPAND[t])
    if t.startswith('"') and t.endswith('"'):
        return ['"' + t.strip('"').rstrip("*") + '"']   # stemming covers plural endings
    return [t]


def oa_term(t):
    return " OR ".join(oa_terms(t))


def group(terms):
    return "(" + " OR ".join(x for t in terms for x in oa_terms(t)) + ")"


def filter_value(blocks):
    return ",".join("title_and_abstract.search:" + group(b) for b in blocks)


def build_url(blocks, cursor="*", per_page=200, mailto=None, count_only=False):
    params = {"filter": filter_value(blocks)}
    if count_only:
        params.update({"per-page": "1", "select": "id"})
    else:
        params.update({"per-page": str(per_page), "cursor": cursor, "select": SELECT})
    if mailto:
        params["mailto"] = mailto
    return BASE + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe=":,()*")


def split_queries(blocks, limit=URL_LIMIT):
    """Return a list of block-lists whose URLs all fit under the limit."""
    if len(build_url(blocks, cursor="X" * 40)) <= limit:
        return [blocks]
    i = max(range(len(blocks)), key=lambda k: len(" OR ".join(blocks[k])))
    if len(blocks[i]) < 2:
        raise ValueError("A single term is too long for the URL limit")
    half = len(blocks[i]) // 2
    left = blocks[:i] + [blocks[i][:half]] + blocks[i + 1:]
    right = blocks[:i] + [blocks[i][half:]] + blocks[i + 1:]
    return split_queries(left, limit) + split_queries(right, limit)


def reconstruct_abstract(inv):
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def get_json(url, api_key=None, tries=6):
    req = urllib.request.Request(url, headers={"User-Agent": "arctic-microtopo-map/0.1"})
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")
    for k in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and k < tries - 1:
                time.sleep(2 ** k)
                continue
            raise
        except urllib.error.URLError:
            if k < tries - 1:
                time.sleep(2 ** k)
                continue
            raise


def row_from_work(w):
    loc = w.get("primary_location") or {}
    src = (loc.get("source") or {}) if isinstance(loc, dict) else {}
    auth = w.get("authorships") or []
    first = ((auth[0].get("author") or {}).get("display_name", "")) if auth else ""
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    return {"openalex_id": (w.get("id") or "").rsplit("/", 1)[-1], "doi": doi, "title": w.get("display_name") or "",
            "year": w.get("publication_year") or "", "type": w.get("type") or "", "venue": src.get("display_name") or "",
            "first_author": first, "abstract": reconstruct_abstract(w.get("abstract_inverted_index"))}


def harvest(queries, mailto=None, api_key=None, max_records=50000, polite=0.2):
    out = {}
    for qi, blocks in enumerate(queries, 1):
        cursor, n = "*", 0
        while cursor:
            data = get_json(build_url(blocks, cursor=cursor, mailto=mailto), api_key)
            for w in data.get("results", []):
                r = row_from_work(w)
                if r["openalex_id"] in out:
                    out[r["openalex_id"]]["subqueries"] += f";{qi}"
                else:
                    r["subqueries"] = str(qi)
                    out[r["openalex_id"]] = r
                n += 1
            cursor = (data.get("meta") or {}).get("next_cursor")
            if n >= max_records:
                print(f"  sub-query {qi}: stopped at --max-records {max_records}", file=sys.stderr)
                break
            time.sleep(polite)
        print(f"  sub-query {qi}/{len(queries)}: {n} records", file=sys.stderr)
    return list(out.values())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="openalex_results.csv")
    ap.add_argument("--mailto", help="contact email for the OpenAlex polite pool")
    ap.add_argument("--api-key", help="OpenAlex API key, if you have one")
    ap.add_argument("--dry-run", action="store_true", help="print sub-queries and URL lengths only")
    ap.add_argument("--count", action="store_true", help="print hit counts per block and per sub-query")
    ap.add_argument("--dois", help="text file with one DOI per line: fetch these works instead of searching")
    ap.add_argument("--max-records", type=int, default=50000)
    a = ap.parse_args(argv)

    blocks = [sb.A, sb.B, sb.C]
    queries = split_queries(blocks)
    if a.dry_run:
        for i, q in enumerate(queries, 1):
            print(f"sub-query {i}: block sizes {[len(b) for b in q]}, URL length {len(build_url(q, cursor='X'*40))}")
        return 0
    if a.dois:
        dois = [d.strip() for d in open(a.dois) if d.strip()]
        rows = []
        for i in range(0, len(dois), 50):
            chunk = "|".join("https://doi.org/" + d.replace("https://doi.org/", "") for d in dois[i:i + 50])
            url = BASE + "?" + urllib.parse.urlencode({"filter": f"doi:{chunk}", "per-page": "50", "select": SELECT},
                                                      quote_via=urllib.parse.quote, safe=":,/|")
            if a.mailto:
                url += "&mailto=" + urllib.parse.quote(a.mailto)
            rows += [row_from_work(w) for w in get_json(url, a.api_key).get("results", [])]
        for r in rows:
            r["subqueries"] = "doi-lookup"
    elif a.count:
        for name, b in zip("ABC", blocks):
            for part in split_queries([b]):
                c = get_json(build_url(part, mailto=a.mailto, count_only=True), a.api_key)["meta"]["count"]
                print(f"block {name} part ({len(part[0])} terms): {c}")
        total = 0
        for i, q in enumerate(queries, 1):
            c = get_json(build_url(q, mailto=a.mailto, count_only=True), a.api_key)["meta"]["count"]
            total += c
            print(f"A AND B AND C, sub-query {i}: {c}")
        print(f"sum of sub-queries (before removing overlaps): {total}")
        return 0
    else:
        rows = harvest(queries, a.mailto, a.api_key, a.max_records)
    cols = ["openalex_id", "doi", "title", "year", "type", "venue", "first_author", "abstract", "subqueries"]
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} unique records to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
