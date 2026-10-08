const M = require("./main.js");
const { push, R, heading1, heading2, para, multiPara, dataTable, spacer, pageBreak, NAVY, FONT } = M;

function appendixHeading(letter, title) {
  push(new M.Paragraph({
    heading: M.HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 180 },
    border: { bottom: { color: M.BLUE, space: 4, style: "single", size: 10 } },
    children: [new M.TextRun({ text: `Appendix ${letter} — ${title}`, bold: true, size: 30, font: FONT, color: NAVY })],
  }));
}

push(new M.Paragraph({
  alignment: "center",
  spacing: { before: 2000, after: 2000 },
  children: [new M.TextRun({ text: "APPENDIX", bold: true, size: 40, font: FONT, color: NAVY })],
}));
push(para("The following pages are supplementary material — full data dictionaries, additional statistical detail and a glossary — and are not counted toward the 20–25 page target given for the main body of this Approach Note.", { align: "center", italics: true, color: M.GRAY, size: M.SZ_SMALL }));
push(pageBreak());

// ---------------------------------------------------------------------
appendixHeading("A", "Data Dictionaries");
push(para("Reproduced from the organisers' Data Description Doc, supplied with the hackathon package."));

push(heading2("Data Science Jobs"));
push(dataTable(["Column", "Description"], [
  ["reference_no", "Row identification number or ID"],
  ["company_name", "Name of the recruiting company"],
  ["job_title", "Title of the job"],
  ["min_experience", "Minimum required experience"],
  ["avg_salary", "Average salary offered across the job postings for the company"],
  ["min_salary", "Minimum salary offered across the job postings for the company"],
  ["max_salary", "Maximum salary offered across the job postings for the company"],
  ["num_of_jobs", "Number of postings by the company"],
], [1.6, 4.8]));
push(spacer(160));

push(heading2("Analytics Jobs"));
push(dataTable(["Column", "Description"], [
  ["s_no", "Row identification number or ID"],
  ["experience", "Years of experience required for the job"],
  ["job_description", "Typical description of the job"],
  ["job_desig", "Designation or position of the job role"],
  ["job_type", "Type or classification of the job"],
  ["key_skills", "Key skills required for the job"],
  ["location", "Geo location of the job requirement"],
  ["salary", "Salary offered (banded)"],
], [1.6, 4.8]));
push(spacer(160));

push(heading2("JDS Skill Traits (Junior Data Scientists)"));
push(dataTable(["Column", "Description"], [
  ["id", "Row identification number or ID"],
  ["big_data_skills", "Average score on data skills, 1–5 scale, from tests, training and feedback"],
  ["maths-stats_skills", "Average score on quantitative, maths and statistics skills, 1–5 scale"],
  ["coding_skills", "Average score on coding skills (SAS, Python, SQL, etc.), 1–5 scale"],
  ["ai_and_ml_skills", "Average score on AI and machine-learning concepts, 1–5 scale"],
  ["dashboard_and_storytelling_skills", "Average score on visualisation, reporting and storytelling, 1–5 scale"],
  ["salary_hike_high_or_low", "Binary outcome for performance-based salary hike: 1 = high, 0 = low"],
], [2.2, 4.2]));
push(spacer(160));

push(heading2("SDS Personality Traits (Senior Data Scientists)"));
push(para("Based on the Big-Five Personality Model (Five-Factor Model) and the Eysenck Personality Questionnaire (EPQ)."));
push(dataTable(["Column", "Description"], [
  ["id", "Row identification number or ID"],
  ["neuroticism", "Tendency to experience negative emotions (anxiety, anger, self-doubt). Higher = more neurotic."],
  ["extraversion", "Spectrum from outgoing/assertive to reserved/solitary. Higher = more extraverted."],
  ["openness_to_experience", "Creativity, curiosity, willingness to embrace new ideas. Higher = more open."],
  ["agreeableness", "Compassion, cooperation, trust, empathy. Higher = more agreeable."],
  ["conscientiousness", "Organisation, responsibility, goal-directedness. Higher = more conscientious."],
  ["success_classification_high_low", "High / low classification of overall success within the organisation"],
], [2.2, 4.2]));
push(pageBreak());

// ---------------------------------------------------------------------
appendixHeading("B", "Supplementary Statistical Tables");

push(heading2("B.1  Data Science Jobs — Top Job Titles by Frequency"));
push(dataTable(["Job title", "Count"],
  Object.entries(R.ds_jobs.top_job_titles).map(([k, v]) => [k, String(v)]),
  [4.8, 1.6]));
push(spacer(160));

push(heading2("B.2  Analytics Jobs — Top Designations by Frequency"));
push(dataTable(["Designation", "Count"],
  Object.entries(R.an_jobs.top_designations).map(([k, v]) => [k, String(v)]),
  [4.8, 1.6]));
push(spacer(160));

push(heading2("B.3  JDS Skill Traits — Descriptive Statistics (1–5 scale)"));
push(dataTable(["Skill", "Mean"],
  Object.entries(R.jds.skill_means_overall).map(([k, v]) => [k, v.toFixed(2)]),
  [4.8, 1.6]));
push(spacer(160));

push(heading2("B.4  SDS Personality Traits — Descriptive Statistics"));
push(dataTable(["Trait", "Mean"],
  Object.entries(R.sds.trait_means_overall).map(([k, v]) => [k, v.toFixed(1)]),
  [4.8, 1.6]));
push(spacer(160));

push(heading2("B.5  Model Configuration Notes"));
push(para("Both classifiers (scikit-learn LogisticRegression, max_iter=1000; RandomForestClassifier, n_estimators=300, max_depth=4) were trained on a stratified 75/25 train-test split with random_state=42 for reproducibility. Logistic-regression inputs were standardised (zero mean, unit variance) before fitting; the random forest used raw feature values, since tree-based models do not require feature scaling. Both models used the five skill or trait columns defined in the data dictionary as the only inputs — no additional engineered features were added to the workforce models, to keep the result directly interpretable against the original rubric."));
push(pageBreak());

// ---------------------------------------------------------------------
appendixHeading("C", "Glossary of Terms");
push(dataTable(["Term", "Meaning"], [
  ["JDS", "Junior Data Scientist(s) — the population in the JDS Skill Traits file"],
  ["SDS", "Senior Data Scientist(s) — the population in the SDS Personality Traits file"],
  ["VFL", "SAS Viya for Learners — SAS's free analytics platform for students and educators"],
  ["Lakh", "Indian numbering unit equal to 100,000; salary figures in the Data Science Jobs file are expressed in INR lakh per annum"],
  ["Big-Five / OCEAN model", "A widely used personality framework with five dimensions — Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism — used in the SDS Personality Traits file"],
  ["EDA", "Exploratory Data Analysis — descriptive, visual inspection of data before formal modelling"],
  ["CRISP-DM", "Cross-Industry Standard Process for Data Mining, the methodology this note's workflow is adapted from"],
  ["Logistic regression", "A statistical classification model estimating the probability of a binary outcome from one or more predictors"],
  ["Random forest", "An ensemble of decision trees used here as a non-linear cross-check on feature importance"],
  ["Standardised coefficient", "A logistic-regression coefficient computed on standardised (zero-mean, unit-variance) inputs, making coefficients comparable across features measured on different scales"],
], [2.0, 4.4]));
push(pageBreak());

// ---------------------------------------------------------------------
appendixHeading("D", "Evaluation Rubric Alignment");
push(para("Marking scheme and section headings reproduced from the organisers' Problem Context Brief (slide “Approach Note: Round 2 Considerations”, Total 100 marks)."));
push(dataTable(
  ["Rubric heading", "Marks", "Addressed in"],
  [
    ["Problem definition or Analytics Objective", "10", "Section 1"],
    ["Approach Description", "15", "Section 2"],
    ["Data Exploration (manipulation, derivation, consolidation, preparation)", "25", "Section 3"],
    ["Data Analysis", "30", "Section 4"],
    ["Results and Conclusions", "10", "Section 5"],
    ["Implications", "10", "Section 6"],
    ["Total", "100", "—"],
  ],
  [4.0, 0.9, 1.5]
));
push(spacer(140));
push(para(
  "Note on an inconsistency in the source brief: the Problem Context Brief states both that Round 2 selects the “top 8 teams” (slide “Approach Note: Round 2 Considerations”) and that Round 3 presentations are “for the 10 teams chosen in Round 2” (slide “Presentation — Round 3”). This note does not assume either figure is correct and flags it for confirmation with the organisers rather than silently resolving it.",
  { italics: true, size: M.SZ_SMALL, color: M.GRAY }
));
