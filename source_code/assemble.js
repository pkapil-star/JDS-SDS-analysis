const M = require("./main.js");
require("./section1.js");
require("./section2.js");
require("./section3.js");
require("./section4.js");
require("./section56.js");
require("./appendix.js");

const {
  children, Document, Packer, Paragraph, TextRun, Header, Footer, PageNumber,
  AlignmentType, convertInchesToTwip, FONT, GRAY, NAVY, DEST, fs,
} = M;

const header = new Header({
  children: [new Paragraph({
    alignment: AlignmentType.RIGHT,
    border: { bottom: { color: "BFBFBF", space: 4, style: "single", size: 4 } },
    children: [new TextRun({
      text: "SAS CU Hackathon — Approach Note (Round 2)",
      size: 16, font: FONT, color: GRAY, italics: true,
    })],
  })],
});

const footer = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    border: { top: { color: "BFBFBF", space: 4, style: "single", size: 4 } },
    children: [
      new TextRun({ text: "Page ", size: 16, font: FONT, color: GRAY }),
      new TextRun({ children: [PageNumber.CURRENT], size: 16, font: FONT, color: GRAY }),
      new TextRun({ text: " of ", size: 16, font: FONT, color: GRAY }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, font: FONT, color: GRAY }),
    ],
  })],
});

const emptyHeader = new Header({ children: [new Paragraph({ children: [] })] });
const emptyFooter = new Footer({ children: [new Paragraph({ children: [] })] });

const doc = new Document({
  creator: "Prepared with Claude (Cowork)",
  title: "Decoding the Data-Science Talent Pipeline — Approach Note",
  description: "SAS CU Hackathon Round 2 Approach Note",
  styles: {
    default: {
      document: { run: { font: FONT, size: 24 } },
    },
  },
  sections: [{
    properties: {
      page: {
        margin: {
          top: convertInchesToTwip(1), bottom: convertInchesToTwip(1),
          left: convertInchesToTwip(1), right: convertInchesToTwip(1),
        },
      },
      titlePage: true,
    },
    headers: { default: header, first: emptyHeader },
    footers: { default: footer, first: emptyFooter },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(DEST, buf);
  console.log("Wrote", DEST, buf.length, "bytes. Paragraphs/elements:", children.length);
});
