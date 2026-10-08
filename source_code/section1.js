const M = require("./main.js");
const {
  push, R, Table, TableRow, WidthType, convertInchesToTwip, AlignmentType,
  heading1, heading2, para, paraRuns, multiPara, cell, dataTable, spacer, pageBreak, ORANGE, NAVY,
} = M;

push(heading1(1, "Problem Definition / Analytics Objective"));

push(...multiPara(
`SAS, in partnership with Chandigarh University, has framed this hackathon around a single, open-ended context: the Indian data-science and analytics job market, together with two internal workforce datasets measuring the technical skills of junior data scientists and the personality traits of senior, customer-facing data scientists. The brief deliberately leaves the specific analytics objective to each participating team, asking only that the chosen problem allow for the testing of data-management and data-manipulation skills, a defensible approach in a business-analytics context, genuine statistical or data-mining work, and a clear, well-supported conclusion. This section sets out the objective this team has chosen to pursue, the reasoning behind it, and the boundaries placed on the analysis, so that the remainder of the note can be read against a single, explicit yardstick.

The four supplied files split naturally into two families. Data Science Jobs and Analytics Jobs describe what the external market is paying for and asking for, across roughly 1,600 and 15,800 postings respectively. JDS Skill Traits and SDS Personality Traits describe what an organisation already has internally: the measured technical-skill profile of 139 junior data scientists and the Big-Five personality profile of 161 senior, customer-facing data scientists, each linked to a real recorded outcome — a salary hike and an overall success classification. Read separately, each file supports only a narrow, single-dataset exercise. Read together, they support a workforce-planning question that most data organisations face in practice: which capabilities should be built, hired for and promoted on, and does the answer change as a data scientist moves from a junior, technical role into a senior, customer-facing one. This team has made that connecting question the centre of the analysis, rather than treating the four files as four unrelated mini-projects.`
));

push(new Table({
  width: { size: convertInchesToTwip(6.4), type: WidthType.DXA },
  columnWidths: [convertInchesToTwip(6.4)],
  rows: [new TableRow({ children: [cell(
    "Analytics Objective: To determine, from the supplied job-market and internal workforce data, which measurable technical skills most strongly predict early-career advancement for junior data scientists, and which personality traits most strongly predict success for senior, customer-facing data scientists — and to translate these findings, together with the external market's pay and skill signals, into concrete, data-backed recommendations for talent acquisition, learning and development, and junior-to-senior career pathing.",
    { bold: true, shade: "FBE6D6", size: 22, align: AlignmentType.JUSTIFIED })] })],
}));
push(spacer(200));

push(heading2("Business Questions Addressed"));
push(para("The objective above is operationalised through six specific questions, each answered with evidence in Sections 4 and 5:"));
push(dataTable(
  ["#", "Question", "Primary dataset(s)"],
  [
    ["Q1", "Which technical skills (big-data, maths/stats, coding, AI/ML, dashboarding) separate junior data scientists who received a high salary hike from those who did not?", "JDS Skill Traits"],
    ["Q2", "Which Big-Five personality traits separate senior data scientists classified as high success from those classified as low success?", "SDS Personality Traits"],
    ["Q3", "Can a simple, explainable model predict the hike / success outcome well enough to be useful as a screening or coaching aid, and which model performs best?", "JDS, SDS"],
    ["Q4", "How does the market compensate experience and seniority for data-science roles, and which job titles and companies account for most of the hiring?", "Data Science Jobs"],
    ["Q5", "Which skills, locations and pay bands dominate the broader analytics job market, and do they corroborate the internal skill-scoring rubric?", "Analytics Jobs"],
    ["Q6", "What do the internal and external signals imply, together, for how an organisation should recruit, train and promote data scientists?", "All four files"],
  ],
  [0.5, 4.5, 1.4]
));
push(spacer(220));

push(heading2("Scope"));
push(...multiPara(
`In scope: descriptive, diagnostic (correlation-based) and predictive (classification) analysis of the four supplied files exactly as provided; standard data cleaning, quality assessment and feature engineering as documented in Section 3; and recommendations addressed to the stakeholders named in Section 6.

Out of scope: any claim of causation — all four files are observational / cross-sectional, so this note reports association, not cause and effect; real-time or streaming analysis; production deployment of any model; linkage to a named company's actual HR system; and any attempt to re-identify individuals, since the Data Description Doc itself notes the data is public, self-reported or masked sample data that "may contain meaningless, misspelled or mistyped entries."`
));

push(heading2("Success Criterion for This Note"));
push(para("This objective is considered met if, by the end of the note, a reader can answer each of the six questions above with a specific, data-backed statement rather than a general impression, and can trace a direct line from a finding in Section 4 (Data Analysis) to a recommendation in Section 6 (Implications)."));

push(pageBreak());
