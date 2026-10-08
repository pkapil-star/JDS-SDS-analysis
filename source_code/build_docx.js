const fs = require("fs");
const path = require("path");
const sizeOf = (() => {
  // tiny PNG dimension reader (avoids extra deps)
  return function (file) {
    const buf = fs.readFileSync(file);
    // PNG: width/height at bytes 16-24
    const width = buf.readUInt32BE(16);
    const height = buf.readUInt32BE(20);
    return { width, height };
  };
})();

const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, PageBreak, Header, Footer, PageNumber, NumberFormat,
  TableOfContents, LevelFormat, convertInchesToTwip, VerticalAlign,
  TabStopType, TabStopPosition
} = require("docx");

const OUT_DIR = "/tmp/claude-0/-home-claude/31826d7e-fff7-520a-8812-a91292e0ab56/scratchpad/outputs";
const R = JSON.parse(fs.readFileSync(path.join(OUT_DIR, "results.json"), "utf8"));
const DEST = "/mnt/user-data/outputs/SAS_CU_Hackathon_Approach_Note.docx";

// ---------------------------------------------------------------------------
// Style constants
// ---------------------------------------------------------------------------
const FONT = "Times New Roman";
const NAVY = "1F3C57";
const BLUE = "2C5F8A";
const ORANGE = "B35C1E";
const GRAY = "595959";
const LIGHT_BLUE_SHADE = "DCE8F2";
const LIGHT_GRAY_SHADE = "F0F0F0";

const SZ_TITLE = 56;      // 28pt
const SZ_SUB = 30;        // 15pt
const SZ_H1 = 30;         // 15pt
const SZ_H2 = 26;         // 13pt
const SZ_H3 = 24;         // 12pt bold
const SZ_BODY = 24;       // 12pt
const SZ_SMALL = 20;      // 10pt
const SZ_CAPTION = 19;    // 9.5pt

// single spacing, modest space-after
const SPACING_BODY = { after: 160, line: 264, lineRule: "auto" };
const SPACING_TIGHT = { after: 80, line: 264, lineRule: "auto" };

function para(text, opts = {}) {
  const {
    bold = false, italics = false, size = SZ_BODY, color = "1A1A1A",
    align = AlignmentType.JUSTIFIED, spacing = SPACING_BODY, after, indent,
  } = opts;
  return new Paragraph({
    alignment: align,
    spacing: after !== undefined ? { ...spacing, after } : spacing,
    indent,
    children: [new TextRun({ text, bold, italics, size, font: FONT, color })],
  });
}

// paragraph with mixed runs: array of {text, bold, italics, color, size}
function paraRuns(runs, opts = {}) {
  const { align = AlignmentType.JUSTIFIED, spacing = SPACING_BODY } = opts;
  return new Paragraph({
    alignment: align,
    spacing,
    children: runs.map(r => new TextRun({
      text: r.text, bold: !!r.bold, italics: !!r.italics,
      size: r.size || SZ_BODY, font: FONT, color: r.color || "1A1A1A",
    })),
  });
}

function multiPara(text, opts = {}) {
  return text.split(/\n\n+/).map(t => para(t.trim(), opts));
}

function heading1(num, text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 180 },
    border: { bottom: { color: BLUE, space: 4, style: BorderStyle.SINGLE, size: 10 } },
    children: [new TextRun({ text: `${num}. ${text}`, bold: true, size: SZ_H1, font: FONT, color: NAVY })],
  });
}
function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 260, after: 140 },
    children: [new TextRun({ text, bold: true, size: SZ_H2, font: FONT, color: BLUE })],
  });
}
function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, italics: true, size: SZ_H3, font: FONT, color: "333333" })],
  });
}

function bulletPara(text, opts = {}) {
  return new Paragraph({
    numbering: { reference: "main-bullets", level: 0 },
    spacing: SPACING_TIGHT,
    children: [new TextRun({ text, size: SZ_BODY, font: FONT, ...opts })],
  });
}

function caption(text, label) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 240 },
    children: [new TextRun({ text: `${label}: ${text}`, italics: true, size: SZ_CAPTION, font: FONT, color: GRAY })],
  });
}

function imageParagraph(file, widthIn) {
  const full = path.join(OUT_DIR, file);
  const dim = sizeOf(full);
  const w = widthIn;
  const h = (dim.height / dim.width) * w;
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 160, after: 40 },
    children: [
      new ImageRun({
        type: "png",
        data: fs.readFileSync(full),
        transformation: { width: Math.round(w * 96), height: Math.round(h * 96) },
      }),
    ],
  });
}

function figure(file, widthIn, label, text) {
  return [imageParagraph(file, widthIn), caption(text, label)];
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ---------------- Tables ----------------
function cell(text, opts = {}) {
  const { bold = false, shade, width, align = AlignmentType.LEFT, color = "1A1A1A", size = SZ_SMALL, valign } = opts;
  return new TableCell({
    width: width ? { size: width, type: WidthType.DXA } : undefined,
    shading: shade ? { type: ShadingType.CLEAR, color: "auto", fill: shade } : undefined,
    verticalAlign: valign || VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      alignment: align,
      spacing: { after: 0, line: 240, lineRule: "auto" },
      children: [new TextRun({ text: String(text), bold, size, font: FONT, color })],
    })],
  });
}

function dataTable(headers, rows, widthsIn, opts = {}) {
  const totalTwip = convertInchesToTwip(widthsIn.reduce((a, b) => a + b, 0));
  const colWidths = widthsIn.map(w => convertInchesToTwip(w));
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => cell(h, { bold: true, shade: NAVY, color: "FFFFFF", width: colWidths[i], align: opts.headerAlign || AlignmentType.LEFT })),
  });
  const bodyRows = rows.map((r, ri) => new TableRow({
    children: r.map((v, i) => cell(v, {
      width: colWidths[i],
      shade: ri % 2 === 1 ? LIGHT_GRAY_SHADE : undefined,
      align: (opts.colAlign && opts.colAlign[i]) || AlignmentType.LEFT,
    })),
  }));
  return new Table({
    width: { size: totalTwip, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...bodyRows],
  });
}

function spacer(h = 160) {
  return new Paragraph({ spacing: { after: h }, children: [] });
}

module.exports = {
  fs, path, R, OUT_DIR, DEST,
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, PageBreak, Header, Footer, PageNumber, NumberFormat,
  TableOfContents, LevelFormat, convertInchesToTwip, VerticalAlign,
  TabStopType, TabStopPosition,
  FONT, NAVY, BLUE, ORANGE, GRAY, LIGHT_BLUE_SHADE, LIGHT_GRAY_SHADE,
  SZ_TITLE, SZ_SUB, SZ_H1, SZ_H2, SZ_H3, SZ_BODY, SZ_SMALL, SZ_CAPTION,
  SPACING_BODY, SPACING_TIGHT,
  para, paraRuns, multiPara, heading1, heading2, heading3, bulletPara,
  caption, imageParagraph, figure, pageBreak, cell, dataTable, spacer,
};
