const M = require("./main.js");
const { push, R, heading1, heading2, para, multiPara, dataTable, spacer, pageBreak } = M;

// =====================================================================
// SECTION 5 — RESULTS AND CONCLUSIONS
// =====================================================================
push(heading1(5, "Results and Conclusions"));
push(para("Table 9 closes the loop opened in Section 1 by answering each business question directly, with the supporting figure quoted alongside."));

push(dataTable(
  ["#", "Finding"],
  [
    ["Q1", "Dashboarding/storytelling skill (r=0.55) and maths/statistics skill (r=0.52) are the strongest technical differentiators of a high salary hike among junior data scientists; raw big-data/infrastructure skill is the weakest (r=0.11)."],
    ["Q2", "Conscientiousness (r=0.68) and openness to experience (r=0.67) are the strongest differentiators of senior success; neuroticism shows no meaningful relationship (r=–0.01)."],
    ["Q3", "Yes — a five-feature logistic regression reaches 88.6% accuracy for the junior-hike outcome and 92.7% accuracy for the senior-success outcome on held-out data; a random-forest cross-check broadly agrees on which features matter most, supporting the result's direction despite the small sample sizes (n=139, n=161)."],
    ["Q4", "Experience is moderately correlated with pay (r=0.59); the “Senior” prefix alone is worth a 65% pay premium within the same job family; hiring is concentrated — the top 12 of 642 recruiting companies account for 39% of all postings."],
    ["Q5", "SQL, Python, machine learning and SAS are among the most-requested skills in the broader analytics market (itself broader than pure data-science roles); Bengaluru, Mumbai and Gurgaon together host 49% of postings."],
    ["Q6", "See Section 6 (Implications) below."],
  ],
  [0.6, 5.8]
));
push(spacer(200));

push(...multiPara(
`Read together, the market and workforce evidence support a single, coherent conclusion: technical breadth matters early in a data-science career, but it is quantitative depth and the ability to communicate findings — not infrastructure or "big data" skill in isolation — that most separates high performers at the junior level, while at the senior, customer-facing level the differentiator shifts almost entirely to disposition: how organised, goal-directed and open to new ideas a person is, rather than any additional technical credential measured in this dataset. This conclusion directly answers the analytics objective set out in Section 1 and is consistent across two independent modelling techniques (logistic regression and random forest) on both workforce files.`
));

push(heading2("Limitations"));
push(...multiPara(
`The workforce datasets are modest in size (139 and 161 rows); results should be read as indicative rather than as a production-grade predictive system. All four files are cross-sectional and observational, so this note reports association, not causation — the models identify which traits and skills move together with the outcomes, not that raising one would cause the other to change. The Data Description Doc states the data is public, self-reported or masked sample data, so individual records should not be treated as verified facts about real people. The Analytics Jobs key-skills field is truncated in 87.2% of rows (Section 3.2), so the market skill-frequency read in Section 4.1 is directional rather than exhaustive. Finally, the SDS "normalized score" documentation does not match the observed 17–68 range in the data (Section 3.2); this note treats the scores as a standardised psychometric scale rather than assuming a literal 0–1 normalisation, and that assumption should be confirmed with the data owner before the findings are used operationally.`
));
push(pageBreak());

// =====================================================================
// SECTION 6 — IMPLICATIONS
// =====================================================================
push(heading1(6, "Implications"));
push(para("The findings in Sections 4 and 5 translate into specific, actionable implications for the stakeholders who would actually use this analysis, summarised in Table 10 and expanded below."));

push(dataTable(
  ["Stakeholder", "Implication / recommendation"],
  [
    ["Talent acquisition / campus recruiting", "Screen junior candidates on quantitative/statistics proficiency and communication/storytelling ability at least as heavily as coding or big-data-tool exposure; this data does not support weighting raw big-data familiarity heavily at entry level."],
    ["Learning & development", "Early-career training budget is better spent on statistics depth and data-storytelling/dashboarding practice than on additional big-data infrastructure tooling, given the latter's weak (r=0.11) relationship to rewarded performance in this sample."],
    ["Succession planning / promotion to senior roles", "When identifying juniors for fast-tracking into senior, customer-facing roles, weight demonstrated conscientiousness (reliability, follow-through) and openness to new approaches alongside technical ability; these behavioural signals are more strongly associated with senior success in this data than any skill or trait examined."],
    ["Compensation & workforce planning", "Budget for a substantial step-change in pay on promotion to “Senior” level (the data shows a 65%+ premium within one job family); treat the concentration of hiring among a small number of large recruiters as both a benchmark and a competitive-hiring signal."],
    ["Students, educators and the broader community", "For students, the findings support investing in statistics and communication skills — not coding alone — as a defensible path to early salary growth; for institutions such as Chandigarh University, they support curricula that pair technical training with structured communication practice and the kind of conscientiousness-building (ownership, deadlines) this data associates with later career success."],
  ],
  [1.9, 4.5]
));
push(spacer(200));

push(heading2("Future Scope"));
push(para(
  "Outside this note's scope but worth flagging for a subsequent round: validating the key-skills frequency read once the Analytics Jobs field is available untruncated; replicating the modelling pipeline natively in SAS Model Studio for a direct comparison against the Python results reported here; and, if a longitudinal version of the JDS/SDS data becomes available, testing whether the junior-stage technical gate and the senior-stage behavioural gate identified in Section 4.4 are genuinely sequential within the same individuals — a within-person panel question the current cross-sectional data cannot answer."
));

push(pageBreak());
