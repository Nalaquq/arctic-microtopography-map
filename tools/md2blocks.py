# -*- coding: utf-8 -*-
"""Convert the project's markdown subset to the block JSON consumed by render2.js.

Supported: '# title', '##'/'###'/'####' headings (-> h1/h2/h3), paragraphs, '- ' bullets (two-space
indent = level 1), '1. ' numbered lists, pipe tables, fenced code blocks, '> ' callouts, inline
**bold**, *italic* and `code`. Paragraphs under a 'References' heading become hanging-indent refs.
Usage: python3 md2blocks.py in.md out.json '<json meta>'
"""
import json
import re
import sys

INLINE = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|(?<![\w*])\*[^*\s][^*]*?(?<!\s)\*(?![\w*]))")


def runs(text):
    out = []
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append({"text": text[pos:m.start()]})
        tok = m.group(0)
        if tok.startswith("`"):
            out.append({"text": tok[1:-1], "c": True})
        elif tok.startswith("**"):
            out.append({"text": tok[2:-2], "b": True})
        else:
            out.append({"text": tok[1:-1], "i": True})
        pos = m.end()
    if pos < len(text):
        out.append({"text": text[pos:]})
    for r in out:
        r["text"] = r["text"].replace("\\*", "*")
    return out or [{"text": ""}]


def table_widths(header, rows, total=10080, min_w=900):
    n = len(header)
    weights = []
    for j in range(n):
        cells = [header[j]] + [r[j] if j < len(r) else "" for r in rows]
        longest = max(len(c) for c in cells)
        avg = sum(len(c) for c in cells) / len(cells)
        weights.append(min(max(avg * 1.2, longest * 0.35, 6), 70) + 6)
    raw = [w / sum(weights) * total for w in weights]
    # never narrower than the longest unbreakable word in the column (about 95 DXA per 8-pt character)
    floor = []
    for j in range(n):
        cells = [header[j]] + [r[j] if j < len(r) else "" for r in rows]
        longest_word = max((len(wd) for c in cells for wd in re.split(r"[\s/]+", re.sub(r"[*`]", "", c)) if wd), default=4)
        floor.append(max(min_w, min(longest_word * 95 + 200, 3200)))
    raw = [max(f, r) for f, r in zip(floor, raw)]
    scale = total / sum(raw)
    ws = [int(round(r * scale)) for r in raw]
    ws[-1] += total - sum(ws)
    return ws


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def convert(md, meta):
    lines = md.splitlines()
    blocks = []
    i = 0
    section = ""
    para = []

    def flush():
        nonlocal para
        if para:
            text = " ".join(s.strip() for s in para)
            if section.lower().startswith("references"):
                blocks.append({"t": "ref", "runs": runs(text)})
            else:
                blocks.append({"t": "p", "runs": runs(text)})
            para = []

    title_done = False
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            flush()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append({"t": "code", "lines": code})
            i += 1
            continue
        if not s:
            flush()
            i += 1
            continue
        if s.startswith("# ") and not title_done:
            flush()
            title = s[2:].strip()
            parts = [p.strip().rstrip(":") for p in re.split(meta.get("title_split", r"(?<=\?)\s+"), title)]
            i += 1
            lead = []
            while i < len(lines) and not lines[i].strip():
                i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                lead.append(lines[i].strip())
                i += 1
            blocks.append({"t": "titlepage", "title": parts, "lead": runs(" ".join(lead)), **meta.get("titlepage", {})})
            title_done = True
            continue
        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m:
            flush()
            level = len(m.group(1)) - 1
            text = m.group(2).strip()
            if level == 1:
                section = text
                if meta.get("break_before", []) and any(text.startswith(x) for x in meta["break_before"]):
                    blocks.append({"t": "pagebreak"})
            blocks.append({"t": f"h{level}", "text": text})
            i += 1
            continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            header, body = rows[0], [r for r in rows[1:] if not all(re.match(r"^:?-{3,}:?$", c) for c in r)]
            widths = meta.get("widths", {}).get(header[0] + "|" + header[-1]) or table_widths(header, body)
            blocks.append({"t": "table", "header": [runs(h) for h in header], "rows": [[runs(c) for c in r] for r in body],
                           "widths": widths, "font": meta.get("table_font", 8)})
            continue
        if s.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append({"t": "callout", "runs": runs(" ".join(quote)), "tone": "blue"})
            continue
        bm = re.match(r"^(\s*)[-*]\s+(.*)$", ln)
        if bm and not s.startswith("**"):
            flush()
            items, levels = [], []
            while i < len(lines):
                bm = re.match(r"^(\s*)[-*]\s+(.*)$", lines[i])
                if not bm or lines[i].strip().startswith("**"):
                    break
                items.append(runs(bm.group(2)))
                levels.append(1 if len(bm.group(1)) >= 2 else 0)
                i += 1
            blocks.append({"t": "bullets", "items": items, "levels": levels})
            continue
        nm = re.match(r"^\d+\.\s+(.*)$", s)
        if nm:
            flush()
            items = []
            while i < len(lines):
                nm = re.match(r"^\d+\.\s+(.*)$", lines[i].strip())
                if not nm:
                    break
                items.append(runs(nm.group(1)))
                i += 1
            blocks.append({"t": "numbered", "items": items})
            continue
        para.append(s)
        i += 1
    flush()
    return blocks


if __name__ == "__main__":
    src, dst, meta = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    bl = convert(open(src, encoding="utf-8").read(), meta)
    json.dump({"meta": meta, "blocks": bl}, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
    print(len(bl), "blocks ->", dst)
