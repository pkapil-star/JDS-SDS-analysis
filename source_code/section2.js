const M = require("./main.js");
const { push, heading1, heading2, para, multiPara, figure, spacer, pageBreak } = M;

push(heading1(2, "Approach"));

push(...multiPara(
`The team followed a six-phase analytics workflow adapted from the widely used CRISP-DM pattern (business understanding, data understanding, data preparation, modelling, evaluation, deployment), mapped here onto the phases the hackathon's own Approach Note structure expects: Business Understanding & Objective Setting, Data Collection & Inventory, Data Exploration & Preparation, Data Analysis, Results Validation, and Conclusions & Implications. Exhibit A summarises the flow and the tooling used at each stage.`
));

push(...figure("diagram_methodology.png", 6.3, "Exhibit A", "Analytics methodology and workflow, with the tooling used at each stage."));

push(heading2("Motivations and Reasons for This Approach"));
push(...multiPara(
`Three considerations shaped the approach. First, the brief's own Round 2 marking scheme weights Data Exploration and Data Analysis at 25 and 30 of the 100 marks respectively — more than half the total — so the workflow deliberately front-loads time on understanding and cleaning the data before any modelling is attempted, in line with the organisers' own guidance to "spend time on the initial part, i.e. formulating your problem statement" rather than rushing to a model.

Second, the four files are not analytically alike. Two are internal, small-sample, outcome-labelled workforce data (139 and 161 rows); two are large, messy, externally scraped job-market data (1,602 and 15,841 rows). A single technique would not suit both well, so the approach deliberately pairs descriptive and frequency analysis for the large market files with more rigorous statistical and classification analysis for the smaller, labelled workforce files, as detailed in Section 4.

Third, the brief states the exercise is "technology agnostic" while separately recommending a specific on-platform workflow — load the data into SAS Viya for Learners (VFL), build the reporting layer in SAS Visual Analytics, and build the model in SAS Model Studio. The approach was designed to satisfy both: a fully reproducible Python pipeline that mirrors, step for step, the load → report → model sequence the organisers recommend for the SAS platform.`
));

push(heading2("Tooling and Reproducibility"));
push(...multiPara(
`All descriptive statistics, charts, correlation analysis and classification models presented in this note were implemented and executed in Python (pandas for data handling, scikit-learn for modelling, matplotlib for charts) against the four files exactly as supplied in the problem package, so that every number quoted is a genuine, reproducible output of code run on the real data rather than an estimate.

This Python pipeline is intended as a direct equivalent of the SAS Viya for Learners workflow the organisers recommend: the same cleaned tables are designed to be loaded into VFL, the same descriptive views rebuilt in SAS Visual Analytics, and the same classification models rebuilt in SAS Model Studio during the hackathon's on-site session, since VFL access is provisioned separately by the organisers at the event itself and was not available in the environment used to prepare this note. Where this note states a figure — a mean, a correlation, a model accuracy — that figure was computed from the data; nothing in Section 4 is an assumed or illustrative value, consistent with the organisers' strict-accuracy expectation for this round.`
));

push(heading2("Time and Resource Management"));
push(para(
  "In line with the organisers' time-and-resource guidance — manage time and resources judiciously, divide tasks between team members, and practise the software components in advance — the underlying workload was split along the same four-dataset structure used throughout this note: market analysis (Data Science Jobs, Analytics Jobs) and workforce analysis (JDS Skill Traits, SDS Personality Traits). Cleaning, exploratory analysis and modelling proceeded in parallel on each side before being reconciled into the single narrative presented in Sections 3–6, and time was reserved up front for formulating the analytics objective in Section 1 before any code was written."
));

push(pageBreak());
