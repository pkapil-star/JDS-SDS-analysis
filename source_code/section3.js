const M = require("./main.js");
const { push, R, heading1, heading2, heading3, para, multiPara, figure, dataTable, spacer, pageBreak } = M;

push(heading1(3, "Data Exploration"));

push(...multiPara(
`This section documents how the four supplied files were inspected, cleaned, transformed and reduced before any analysis was performed, following the brief's own sub-headings: data derivation, data modification, data deduction and reduction. Exhibit B shows, conceptually, how the four files relate to one another and to the two analytical products — market dashboards and workforce models — built from them in Section 4.`
));
push(...figure("diagram_data_map.png", 6.3, "Exhibit B", "Conceptual relationship across the four datasets: external market signals (blue) and internal talent signals (orange) converge into a single analytics layer."));

push(heading2("3.1  Data Inventory"));
push(para("The data dictionaries supplied in the Data Description Doc were used as the basis for inspection; observed row and column counts matched the documented approximations in every file (Table 1)."));
push(dataTable(
  ["File", "Rows × Cols", "Grain (one row =)", "Fields used in this note"],
  [
    ["Data Science Jobs", `${R.ds_jobs.n_rows} × 8`, "A company / job-title salary summary for 2024–25", "company_name, job_title, min_experience, avg/min/max_salary, num_of_jobs"],
    ["Analytics Jobs", `${R.an_jobs.n_rows.toLocaleString()} × 8`, "One job posting", "experience, job_desig, key_skills, location, salary (band)"],
    ["JDS Skill Traits", `${R.jds.n_rows} × 7`, "One junior data scientist", "5 skill scores (1–5 scale), salary_hike_high_or_low"],
    ["SDS Personality Traits", `${R.sds.n_rows} × 7`, "One senior, customer-facing data scientist", "5 Big-Five trait scores, success_classification_high_low"],
  ],
  [1.5, 0.9, 2.1, 2.9]
));
push(para("Table 1. Data inventory, as confirmed against the supplied files (row counts are exact; the Data Description Doc's own figures were rounded).", { italics: true, size: M.SZ_CAPTION, color: M.GRAY, align: "center", spacing: { before: 60, after: 240 } }));

push(heading2("3.2  Data Quality Assessment"));
push(para("The Problem Context Brief warns that the data \"may contain meaningless, misspelled or mistyped entries\" and \"may be present with outliers and other problems.\" The issues actually found on inspection are listed in Table 2; each was verified programmatically rather than assumed."));
push(dataTable(
  ["File", "Issue found", "Evidence", "Treatment"],
  [
    ["Analytics Jobs", "job_type almost entirely missing", `${R.an_jobs.pct_missing_job_type}% missing (only ${Object.values(R.an_jobs.job_type_counts_nonnull).reduce((a,b)=>a+b,0)} of ${R.an_jobs.n_rows.toLocaleString()} rows populated)`, "Excluded as a reliable analysis field; not used for segmentation"],
    ["Analytics Jobs", "job_type has no controlled vocabulary", "5 case variants of one word found: “Analytics”, “analytics”, “ANALYTICS”, “analytic”, “Analytic”", "Noted as a data-governance gap; not case-normalised for this note since the field is excluded above"],
    ["Analytics Jobs", "job_description missing", `${R.an_jobs.pct_missing_job_description}% missing`, "Not used for quantitative analysis in this note"],
    ["Analytics Jobs", "key_skills truncated at source", `${R.an_jobs.pct_key_skills_truncated_with_ellipsis}% of non-null values end in a literal “…”`, "Section 4 skill-frequency results are labelled directional, not exhaustive"],
    ["Analytics Jobs", "job_desig is near-unique free text", `${R.an_jobs.n_unique_designations.toLocaleString()} distinct values across ${R.an_jobs.n_rows.toLocaleString()} rows, including non-analytics spam-like entries (e.g. “Home Base Job/ Data Entry/online Work/part Time Work/freelancer work”)`, "Analysed by top-N frequency only (Section 4.1)"],
    ["Analytics Jobs", "location is free text, often multi-city", `${R.an_jobs.n_unique_locations_raw.toLocaleString()} distinct raw values`, "Reduced to a single primary_location per posting (Section 3.3)"],
    ["Analytics Jobs", "salary supplied as bands, not a figure", "6 ordered bands in INR lakh p.a. (0to3 … 25to50)", "Analysed as an ordered category, not interpolated to a point estimate"],
    ["Data Science Jobs", "salary fields stored as text", "avg_salary / min_salary / max_salary carry a trailing “L” (lakh) suffix, e.g. “7.8L”", "Parsed to numeric INR-lakh fields before analysis (Section 3.3)"],
    ["SDS Personality Traits", "documentation vs. data mismatch", "Data Description Doc states scores are “normalized”; observed range is approximately 17–68, not 0–1 or 0–100", "Treated as a standardised psychometric scale; the mismatch is flagged, not silently resolved"],
    ["JDS / SDS", "no missing values or duplicate IDs", "Verified by null-count and ID-uniqueness check on both files", "No imputation required"],
  ],
  [1.3, 1.7, 2.1, 1.3]
));
push(para("Table 2. Data quality issues identified during exploration, with the evidence and the treatment applied in this note.", { italics: true, size: M.SZ_CAPTION, color: M.GRAY, align: "center", spacing: { before: 60, after: 240 } }));

push(heading2("3.3  Data Derivation"));
push(para("New variables were derived where the supplied fields were not directly analysable:"));
push(dataTable(
  ["Derived field", "Source file", "Definition"],
  [
    ["avg_salary_num, min_salary_num, max_salary_num", "Data Science Jobs", "Numeric INR-lakh salary, parsed from the text fields by stripping the trailing “L”"],
    ["exp_min, exp_max, exp_mid", "Analytics Jobs", "Lower / upper / midpoint years of experience, parsed from free-text ranges such as “6-10 yrs”"],
    ["primary_location", "Analytics Jobs", "First city named in the (often multi-city) location field"],
    ["Tokenised key_skills", "Analytics Jobs", "Each posting's key_skills string split on commas into individual skill tokens for frequency analysis"],
  ],
  [2.1, 1.6, 2.7]
));
push(spacer(200));

push(heading2("3.4  Data Modification"));
push(...multiPara(
`Several source column headers carried stray whitespace or inconsistent casing that would silently break programmatic access — for example " extraversion" (leading space) and "success_ classification_ high_low" (internal spaces) in SDS Personality Traits, and "maths-stats_skills" (hyphenated) in JDS Skill Traits. All headers were trimmed and standardised to a consistent snake_case form before analysis.

Numeric fields were cast from text to proper numeric types (see 3.3), and the six Analytics Jobs salary bands were re-ordered into their natural low-to-high sequence (0to3, 3to6, 6to10, 10to15, 15to25, 25to50) for charting, since they are not stored in that order in the source file.`
));

push(heading2("3.5  Data Deduction and Reduction"));
push(...multiPara(
`For the two large market files, the analysis reduces 642 distinct companies to the top 12 by posting volume and the 10,097 distinct Analytics Jobs designations to the top 10–12 by frequency, so that the charts in Section 4 remain readable; full frequency detail is retained in Appendix B. For the two workforce files, all rows were retained — 139 and 161 are already small enough to analyse in full — and no reduction was applied beyond the five skill or trait columns already defined by the data dictionary.

One deduction follows directly from the quality assessment in 3.2: because job_type is populated for only a small minority of Analytics Jobs rows and carries no controlled vocabulary, this note does not use job_type to segment the analytics job market; job_desig (designation) and the tokenised key_skills field are used instead, since both are populated for effectively all rows.`
));

push(pageBreak());
