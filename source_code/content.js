// Prose and data content for the Approach Note, kept separate from doc-building
// mechanics in build_docx.js. All numbers here are taken verbatim from
// outputs/results.json (produced by analyze.py against the real hackathon data)
// or from the Problem Context Brief / Data Description Doc PDFs. Nothing here is
// invented.

const fs = require("fs");
const R = JSON.parse(fs.readFileSync(process.argv[2] || (__dirname + "/../outputs/results.json"), "utf8"));

module.exports = { R };
