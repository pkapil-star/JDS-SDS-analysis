const L = require("./build_docx.js");
const {
  fs, path, R, Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ImageRun, PageBreak, Header, Footer,
  PageNumber, NumberFormat, convertInchesToTwip, VerticalAlign, LevelFormat,
  FONT, NAVY, BLUE, ORANGE, GRAY, LIGHT_GRAY_SHADE,
  SZ_TITLE, SZ_SUB, SZ_BODY, SZ_SMALL, SZ_CAPTION,
  para, paraRuns, multiPara, heading1, heading2, heading3, bulletPara,
  caption, imageParagraph, figure, pageBreak, cell, dataTable, spacer, DEST,
} = L;

const children = [];
const push = (...items) => items.forEach(i => Array.isArray(i) ? children.push(...i) : children.push(i));

// =====================================================================
// TITLE PAGE
// =====================================================================
push(
  new Paragraph({ spacing: { after: 600 }, children: [] }),
  new Paragraph({ spacing: { after: 600 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({ text: "APPROACH NOTE", bold: true, size: 26, font: FONT, color: ORANGE })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 280 },
    children: [new TextRun({ text: "SAS × Chandigarh University Hackathon — Round 2 Submission", italics: true, size: SZ_SUB, font: FONT, color: GRAY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new TextRun({ text: "Decoding the Data-Science Talent Pipeline", bold: true, size: SZ_TITLE, font: FONT, color: NAVY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 600 },
    children: [new TextRun({ text: "Linking Market Demand, Technical Skills and Personality Traits to Career Outcomes in Data Science",
      size: SZ_SUB, font: FONT, color: BLUE })],
  }),
  new Paragraph({ spacing: { after: 800 }, children: [], border: { bottom: { color: "BFBFBF", space: 1, style: "single", size: 6 } } }),
);

const titleRows = [
  ["Team name", "Greyhat"],
  ["Institution", "Chandigarh University (SAS CU Hackathon)"],
  ["Round", "Round 2 — Approach Note"],
  ["Draft prepared on", "07 October 2026"],
  ["Primary analysis tool", "Python (pandas, scikit-learn, matplotlib)"],
  ["Platform for on-site replication", "SAS Viya for Learners — SAS Visual Analytics & SAS Model Studio"],
];
push(new Table({
  width: { size: convertInchesToTwip(6.4), type: WidthType.DXA },
  columnWidths: [convertInchesToTwip(2.3), convertInchesToTwip(4.1)],
  rows: titleRows.map(([k, v], i) => new TableRow({
    children: [
      cell(k, { bold: true, width: convertInchesToTwip(2.3), size: SZ_SMALL }),
      cell(v, { width: convertInchesToTwip(4.1), size: SZ_SMALL, color: v.startsWith("[") ? ORANGE : "1A1A1A" }),
    ],
  })),
}));
push(
  new Paragraph({ spacing: { before: 500 }, children: [] }),
  para("All figures, tables and charts in this note were computed from the four data files supplied in the hackathon package; none are placeholders.",
    { italics: true, size: SZ_SMALL, color: GRAY, align: AlignmentType.CENTER, spacing: { after: 0 } }),
  pageBreak(),
);

// =====================================================================
// SCOPE NOTE (not part of the 20-25 page body)
// =====================================================================
push(
  new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ text: "Note on Scope, Data Source and Methodology", bold: true, size: 26, font: FONT, color: NAVY })],
  }),
  ...multiPara(
`This note is built entirely from the four data files supplied in the official hackathon package — Data Science Jobs, Analytics Jobs, JDS Skill Traits and SDS Personality Traits — together with the accompanying Data Description Doc and Problem Context Brief. No external data has been merged in, and the analytics objective in Section 1 was formulated by this team, since the brief deliberately leaves problem identification open ("everything depends on your problem identification or analytics objective").

Every statistic, chart, correlation and model result presented in Sections 1–6 and in the Appendix was produced by running Python code (pandas, scikit-learn, matplotlib) directly against the supplied files. Nothing is estimated, assumed or illustrative; where a number could not be computed from the data, or where a result should be read with caution, this note says so explicitly rather than presenting it as fact, in line with the organisers' own instruction to label unverified material as "proposed", "expected" or "to be validated".

The Problem Context Brief recommends a specific on-platform workflow — load the data into SAS Viya for Learners (VFL), build the reporting layer in SAS Visual Analytics and the model in SAS Model Studio — while also stating the exercise is technology-agnostic. The Python pipeline documented here was designed as a direct, reproducible equivalent of that workflow, intended to be rebuilt on the SAS platform during the hackathon's on-site session, since VFL access is provisioned separately by the organisers at the event and was not available while this note was prepared.

This note follows the structure, formatting and length guidance given on the Problem Context Brief's "Approach Note: Important for Round 2" slide: Word format; Times New Roman, 12 point, single spacing; and a target of 20–25 pages excluding the Appendix. The Appendix (data dictionaries, full statistical tables and a glossary) is additional material and is not counted toward that range.`,
    { spacing: { after: 160 } }
  ),
  pageBreak(),
);

// =====================================================================
// TABLE OF CONTENTS (static — mirrors the brief's required headings)
// =====================================================================
push(
  new Paragraph({
    spacing: { after: 240 },
    children: [new TextRun({ text: "Table of Contents", bold: true, size: 30, font: FONT, color: NAVY })],
  })
);
const toc = [
  ["1.", "Problem Definition / Analytics Objective"],
  ["2.", "Approach"],
  ["3.", "Data Exploration"],
  ["4.", "Data Analysis"],
  ["5.", "Results and Conclusions"],
  ["6.", "Implications"],
  ["", "Appendix A — Data Dictionaries"],
  ["", "Appendix B — Supplementary Statistical Tables"],
  ["", "Appendix C — Glossary of Terms"],
  ["", "Appendix D — Evaluation Rubric Alignment"],
];
toc.forEach(([n, t]) => {
  push(new Paragraph({
    spacing: { after: 110 },
    tabStops: [{ type: "right", position: convertInchesToTwip(6.4) }],
    children: [new TextRun({ text: `${n ? n + "  " : "      "}${t}`, size: SZ_BODY, font: FONT, color: "1A1A1A" })],
  }));
});
push(pageBreak());

module.exports = {
  children, push, fs, path, R, Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ImageRun, PageBreak, Header, Footer,
  PageNumber, NumberFormat, convertInchesToTwip, VerticalAlign, LevelFormat,
  FONT, NAVY, BLUE, ORANGE, GRAY, LIGHT_GRAY_SHADE,
  SZ_TITLE, SZ_SUB, SZ_BODY, SZ_SMALL, SZ_CAPTION,
  para, paraRuns, multiPara, heading1, heading2, heading3, bulletPara,
  caption, imageParagraph, figure, pageBreak, cell, dataTable, spacer, DEST,
};
