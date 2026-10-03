// Generic renderer: {meta, blocks} JSON (from md2blocks.py) -> .docx, matching the dossier v0.3 look.
// Usage: node render2.js in.json out.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, PageBreak, Header, Footer, PageNumber, LevelFormat,
  TableLayoutType, VerticalAlign,
} = require("docx");

const [, , IN, OUT] = process.argv;
const { meta, blocks } = JSON.parse(fs.readFileSync(IN, "utf8"));
const BLUE = "1F4E79", GREY = "5A5A5A", HEAD_FILL = "D9EAF7", BOX_FILL = "EAF2F8", CODE_FILL = "F4F6F8";

// Math symbols are set in Cambria Math so every renderer finds a glyph (Arial lacks several of them).
const MATH = /([\u2202\u2207\u2217\u2211\u221A\u2208\u2248\u2264\u2265\u0302]+)/;
function mkRuns(runs, opts = {}) {
  const out = [];
  runs.forEach(r => {
    const base = { bold: !!r.b || !!opts.bold, italics: !!r.i || !!opts.italics,
      size: r.c ? Math.max((opts.size || 20) - 2, 14) : opts.size, color: opts.color };
    r.text.split(MATH).forEach(seg => {
      if (!seg) return;
      const isMath = MATH.test(seg) && seg.replace(MATH, "") === "";
      out.push(new TextRun({ ...base, text: seg, font: isMath ? "Cambria Math" : (r.c ? "Consolas" : "Arial") }));
    });
  });
  return out;
}

let numCount = 0;
const numbering = [{
  reference: "bullets",
  levels: [0, 1, 2].map(l => ({
    level: l, format: LevelFormat.BULLET, text: l === 0 ? "•" : (l === 1 ? "–" : "◦"),
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360 + 360 * l, hanging: 260 } } },
  })),
}];
blocks.forEach(b => {
  if (b.t === "numbered") {
    b._ref = "num" + (numCount++);
    numbering.push({ reference: b._ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 300 } } } }] });
  }
});

const thin = { style: BorderStyle.SINGLE, size: 4, color: "B7C9D9" };
const cellBorders = { top: thin, left: thin, bottom: thin, right: thin };

function mkTable(b) {
  const size = Math.round((b.font || 8) * 2);
  const w = b.widths;
  const hdr = new TableRow({ tableHeader: true, cantSplit: true, children: b.header.map((h, i) => new TableCell({
    width: { size: w[i], type: WidthType.DXA }, borders: cellBorders,
    shading: { type: ShadingType.CLEAR, color: "auto", fill: HEAD_FILL },
    margins: { top: 50, bottom: 50, left: 80, right: 80 }, verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: mkRuns(h, { bold: true, size, color: "1F2D3D" }) })],
  })) });
  const rows = b.rows.map((row, ri) => new TableRow({ cantSplit: true, children: row.map((c, i) => new TableCell({
    width: { size: w[i], type: WidthType.DXA }, borders: cellBorders,
    shading: ri % 2 === 1 ? { type: ShadingType.CLEAR, color: "auto", fill: "F7FAFC" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: mkRuns(c, { size }) })],
  })) }));
  return new Table({ width: { size: w.reduce((a, c) => a + c, 0), type: WidthType.DXA }, columnWidths: w,
    layout: TableLayoutType.FIXED, rows: [hdr, ...rows] });
}

function callout(runs, tone) {
  const color = tone === "amber" ? "C55A11" : BLUE;
  const fill = tone === "amber" ? "FFF4E5" : BOX_FILL;
  const bd = { style: BorderStyle.SINGLE, size: 8, color, space: 6 };
  return new Paragraph({ border: { top: bd, left: bd, bottom: bd, right: bd },
    shading: { type: ShadingType.CLEAR, color: "auto", fill }, spacing: { before: 160, after: 160 },
    indent: { left: 120, right: 120 }, children: mkRuns(runs, { size: 19 }) });
}

const children = [];
for (const b of blocks) {
  switch (b.t) {
    case "titlepage": {
      if (b.kicker) children.push(new Paragraph({ spacing: { before: 700, after: 240 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: b.kicker, bold: true, color: BLUE, size: 22, font: "Arial" })] }));
      b.title.forEach((t, i) => children.push(new Paragraph({ alignment: AlignmentType.CENTER,
        spacing: { after: i === b.title.length - 1 ? 240 : 80 },
        children: [new TextRun({ text: t, bold: true, size: i === 0 ? 38 : 30, font: "Arial", color: "111111" })] })));
      if (b.subtitle) children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
        children: [new TextRun({ text: b.subtitle, italics: true, size: 20, font: "Arial", color: GREY })] }));
      children.push(callout(b.lead, "blue"));
      if (b.note) children.push(new Paragraph({ spacing: { before: 120, after: 120 },
        children: [new TextRun({ text: b.note, size: 18, font: "Arial", color: GREY })] }));
      if (b.contents) {
        children.push(new Paragraph({ spacing: { before: 240, after: 80 },
          children: [new TextRun({ text: "Contents", bold: true, color: BLUE, size: 22, font: "Arial" })] }));
        blocks.filter(x => x.t === "h1").forEach(x => children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 },
          spacing: { after: 20 }, children: [new TextRun({ text: x.text, size: 19, font: "Arial" })] })));
      }
      children.push(new Paragraph({ children: [new PageBreak()] }));
      break;
    }
    case "h1": children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: b.text })] })); break;
    case "h2": children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: b.text })] })); break;
    case "h3": children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: b.text })] })); break;
    case "p": children.push(new Paragraph({ spacing: { after: 110 }, children: mkRuns(b.runs) })); break;
    case "bullets":
      b.items.forEach((it, k) => children.push(new Paragraph({ numbering: { reference: "bullets", level: (b.levels || [])[k] || 0 },
        spacing: { after: 50 }, children: mkRuns(it) })));
      children.push(new Paragraph({ spacing: { after: 40 }, children: [] }));
      break;
    case "numbered":
      b.items.forEach(it => children.push(new Paragraph({ numbering: { reference: b._ref, level: 0 }, spacing: { after: 60 }, children: mkRuns(it) })));
      children.push(new Paragraph({ spacing: { after: 40 }, children: [] }));
      break;
    case "callout": children.push(callout(b.runs, b.tone)); break;
    case "table": children.push(mkTable(b)); children.push(new Paragraph({ spacing: { after: 120 }, children: [] })); break;
    case "code":
      b.lines.forEach((ln, k) => children.push(new Paragraph({
        shading: { type: ShadingType.CLEAR, color: "auto", fill: CODE_FILL },
        spacing: { before: k === 0 ? 80 : 0, after: k === b.lines.length - 1 ? 140 : 0 }, indent: { left: 120, right: 120 },
        children: [new TextRun({ text: ln.length ? ln : " ", font: "Consolas", size: 15, color: "1F2D3D" })] })));
      break;
    case "ref": children.push(new Paragraph({ spacing: { after: 60 }, indent: { left: 360, hanging: 360 }, children: mkRuns(b.runs, { size: 17 }) })); break;
    case "pagebreak": children.push(new Paragraph({ children: [new PageBreak()] })); break;
    default: throw new Error("unknown block " + b.t);
  }
}

const small = { size: 16, color: "6E6E6E", font: "Arial" };
const doc = new Document({
  creator: meta.creator || "S. Gleason", title: meta.doc_title, description: meta.doc_description,
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, color: BLUE, font: "Arial" }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 0, keepNext: true } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 25, bold: true, color: BLUE, font: "Arial" }, paragraph: { spacing: { before: 220, after: 90 }, outlineLevel: 1, keepNext: true } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, color: "2E5C8A", font: "Arial" }, paragraph: { spacing: { before: 180, after: 60 }, outlineLevel: 2, keepNext: true } },
    ],
  },
  numbering: { config: numbering },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1000, left: 1080, right: 1080 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: meta.header_text, ...small })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: meta.footer_text + " | Page ", ...small }),
      new TextRun({ children: [PageNumber.CURRENT], ...small }), new TextRun({ text: " of ", ...small }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], ...small })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("wrote", OUT, buf.length); });
