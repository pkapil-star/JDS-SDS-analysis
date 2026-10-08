const M = require("./main.js");
const { push, R, heading1, heading2, heading3, para, multiPara, figure, dataTable, spacer, pageBreak, SZ_CAPTION, GRAY } = M;

push(heading1(4, "Data Analysis"));
push(para("This section moves from description to diagnosis to prediction: first characterising the market and workforce data as observed (4.1), then testing which variables are statistically associated with the recorded outcomes (4.2), then fitting and validating classification models (4.3), and finally reading the two halves of the data together (4.4)."));

// -------------------------------------------------------------------
push(heading2("4.1  Descriptive Analytics — The Job Market"));
push(heading3("Data Science Jobs"));
push(...multiPara(
`Across ${R.ds_jobs.n_rows} company / title records summarising ${R.ds_jobs.total_postings_sum_num_of_jobs.toLocaleString()} individual postings from ${R.ds_jobs.n_companies} companies, the average offered salary is ${R.ds_jobs.avg_salary_lakh_mean} lakh p.a. (median ${R.ds_jobs.avg_salary_lakh_median} lakh), with a typical minimum-experience requirement of ${R.ds_jobs.min_experience_median} years (mean ${R.ds_jobs.min_experience_mean}). Minimum experience is moderately, positively correlated with average salary (r = ${R.ds_jobs.corr_experience_avgsalary}), confirming the expected link between seniority and pay. The number of postings per record is weakly negatively correlated with average salary (r = ${R.ds_jobs.corr_numjobs_avgsalary}): higher-paying, more senior roles tend to be posted less frequently than entry-level roles, consistent with a typical organisational pyramid.`
));
push(...figure("ds_experience_vs_salary.png", 5.6, "Figure 1", "Minimum experience required vs. average offered salary, Data Science Jobs (each point is one company/title record; line is a linear fit)."));

push(...multiPara(
`Hiring is concentrated: the twelve largest recruiters alone account for 39% of all postings summed across the dataset (36,387 of ${R.ds_jobs.total_postings_sum_num_of_jobs.toLocaleString()}), and all twelve are large IT-services or consulting firms (Figure 2). Pay varies sharply by title (Figure 3): the highest-paid title, Senior Data Scientist, averages ${R.ds_jobs.avg_salary_by_title_lakh["Senior Data Scientist"]} lakh p.a. — almost four times the ${R.ds_jobs.avg_salary_by_title_lakh["Data Analyst"]} lakh average for the entry-level Data Analyst title — and the "Senior" prefix alone carries a substantial premium within the same job family (Data Scientist ${R.ds_jobs.avg_salary_by_title_lakh["Data Scientist"]} lakh vs. Senior Data Scientist ${R.ds_jobs.avg_salary_by_title_lakh["Senior Data Scientist"]} lakh, a 65% uplift).`
));
push(...figure("ds_top_companies.png", 5.6, "Figure 2", "Top 12 companies by total Data Science job postings (sum of num_of_jobs)."));
push(...figure("ds_salary_by_title.png", 5.6, "Figure 3", "Average offered salary by Data Science job title."));

push(heading3("Analytics Jobs"));
push(...multiPara(
`The Analytics Jobs file is both larger and broader than Data Science Jobs: its ${R.an_jobs.n_rows.toLocaleString()} postings have a mean experience requirement of ${R.an_jobs.exp_mid_mean} years (higher than Data Science Jobs' 2.8-year mean), and its top designations and key skills (Figures 4–6) show it spans digital marketing, SEO, finance and general business-analyst roles alongside data-science-specific ones — so it is read in this note as the broader Indian analytics/IT-services job market, not a dataset exclusively about data-science roles.`
));
push(...figure("an_salary_bands.png", 5.6, "Figure 4", "Distribution of postings across salary bands (INR lakh p.a.)."));
push(...multiPara(
`The largest single band is 10–15 lakh (${R.an_jobs.salary_bucket_counts["10to15"].toLocaleString()} postings, ${(100*R.an_jobs.salary_bucket_counts["10to15"]/R.an_jobs.n_rows).toFixed(1)}%), followed by 15–25 lakh (${(100*R.an_jobs.salary_bucket_counts["15to25"]/R.an_jobs.n_rows).toFixed(1)}%); the premium 25–50 lakh band is the smallest (${(100*R.an_jobs.salary_bucket_counts["25to50"]/R.an_jobs.n_rows).toFixed(1)}%), again consistent with fewer senior openings than mid-level ones.`
));
push(...figure("an_top_designations.png", 5.6, "Figure 5", "Top 12 job designations by posting count. Note the mix of analytics-specific and broader IT/marketing titles."));
push(...figure("an_top_locations.png", 5.6, "Figure 6", "Top 12 hiring locations (first city listed per posting)."));
push(...multiPara(
`Hiring is geographically concentrated: Bengaluru alone accounts for ${(100*R.an_jobs.top_primary_locations["Bengaluru"]/R.an_jobs.n_rows).toFixed(1)}% of postings, and the top three cities (Bengaluru, Mumbai, Gurgaon) together account for 49%.`
));
push(...figure("an_top_skills.png", 5.6, "Figure 7", "Top 15 key skills requested (within the visible, non-truncated portion of the key_skills field; see Section 3.2 on the 87.2% truncation rate)."));
push(...multiPara(
`SQL, Python, machine learning and SAS all appear among the most-requested skills, alongside non-technical categories such as finance, digital marketing and project management — reinforcing that this file reflects a broad job board rather than a data-science-only sample, and directly relevant to a SAS-sponsored hackathon, SAS itself is the ninth most frequent skill mention among the visible, non-truncated skill text (715 mentions).`
));
push(pageBreak());

// -------------------------------------------------------------------
push(heading2("4.2  Diagnostic Analytics — What Separates High and Low Outcomes"));
push(heading3("JDS Skill Traits: drivers of a high salary hike"));
push(...multiPara(
`${R.jds.pct_high_hike}% of the ${R.jds.n_rows} junior data scientists in this file received a high salary hike. Correlating each of the five skill scores with the hike outcome (Table 3) shows dashboarding-and-storytelling skill as the strongest single correlate (r = ${R.jds.corr_with_target.dashboard_and_storytelling_skills}), closely followed by maths/statistics skill (r = ${R.jds.corr_with_target["maths-stats_skills"]}); big-data skill is, by a wide margin, the weakest (r = ${R.jds.corr_with_target.big_data_skills}).`
));
push(dataTable(
  ["Skill", "Corr. with high hike (r)", "Mean — low hike (0)", "Mean — high hike (1)", "Difference"],
  (() => {
    const order = ["dashboard_and_storytelling_skills","maths-stats_skills","coding_skills","ai_and_ml_skills","big_data_skills"];
    const label = { dashboard_and_storytelling_skills: "Dashboard & storytelling", "maths-stats_skills": "Maths / statistics", coding_skills: "Coding", ai_and_ml_skills: "AI & ML", big_data_skills: "Big data" };
    return order.map(k => [label[k], R.jds.corr_with_target[k].toFixed(3), R.jds.skill_means_by_class[k]["0"].toFixed(2), R.jds.skill_means_by_class[k]["1"].toFixed(2),
      "+" + (R.jds.skill_means_by_class[k]["1"] - R.jds.skill_means_by_class[k]["0"]).toFixed(2)]);
  })(),
  [1.9, 1.5, 1.4, 1.4, 1.1]
));
push(para("Table 3. JDS skill scores (1–5 scale) by salary-hike outcome, ordered by correlation strength.", { italics: true, size: SZ_CAPTION, color: GRAY, align: "center", spacing: { before: 60, after: 200 } }));
push(...figure("jds_corr_heatmap.png", 5.0, "Figure 8", "Correlation matrix, JDS Skill Traits."));
push(...figure("jds_skills_by_class.png", 5.6, "Figure 9", "JDS skill profile by salary-hike outcome. The largest gaps are in dashboarding/storytelling and maths/statistics skill; the smallest is in big-data skill."));

push(heading3("SDS Personality Traits: drivers of senior success"));
push(...multiPara(
`${R.sds.pct_high_success}% of the ${R.sds.n_rows} senior, customer-facing data scientists in this file are classified as high success. Here the pattern is sharper: conscientiousness is the strongest correlate (r = ${R.sds.corr_with_target.conscientiousness}), followed closely by openness to experience (r = ${R.sds.corr_with_target.openness_to_experience}); neuroticism shows essentially no relationship to success (r = ${R.sds.corr_with_target.neuroticism}).`
));
push(dataTable(
  ["Trait", "Corr. with high success (r)", "Mean — low success (0)", "Mean — high success (1)", "Difference"],
  (() => {
    const order = ["conscientiousness","openness_to_experience","extraversion","agreeableness","neuroticism"];
    const label = { conscientiousness: "Conscientiousness", openness_to_experience: "Openness to experience", extraversion: "Extraversion", agreeableness: "Agreeableness", neuroticism: "Neuroticism" };
    return order.map(k => [label[k], R.sds.corr_with_target[k].toFixed(3), R.sds.trait_means_by_class[k]["0"].toFixed(1), R.sds.trait_means_by_class[k]["1"].toFixed(1),
      (R.sds.trait_means_by_class[k]["1"] - R.sds.trait_means_by_class[k]["0"] >= 0 ? "+" : "") + (R.sds.trait_means_by_class[k]["1"] - R.sds.trait_means_by_class[k]["0"]).toFixed(1)]);
  })(),
  [2.0, 1.6, 1.3, 1.3, 1.1]
));
push(para("Table 4. SDS Big-Five trait scores by success outcome, ordered by correlation strength.", { italics: true, size: SZ_CAPTION, color: GRAY, align: "center", spacing: { before: 60, after: 200 } }));
push(...figure("sds_corr_heatmap.png", 5.0, "Figure 10", "Correlation matrix, SDS Personality Traits."));
push(...figure("sds_traits_by_class.png", 5.6, "Figure 11", "SDS Big-Five trait profile by success outcome. Conscientiousness shows the largest gap; neuroticism shows almost none."));
push(...figure("sds_boxplot.png", 5.6, "Figure 12", "Distribution of each Big-Five trait score across all 161 senior data scientists, independent of outcome."));
push(pageBreak());

// -------------------------------------------------------------------
push(heading2("4.3  Predictive Analytics — Classification Models"));
push(...multiPara(
`To test whether the outcomes can be predicted from the skill or trait scores (Business Question Q3), a logistic regression and a random-forest classifier were fitted to each of the two workforce files, using a stratified 75/25 train-test split (random_state fixed for reproducibility) and standardised features for the logistic model. Logistic regression is used as the primary model because its standardised coefficients are directly comparable as relative driver strength; the random forest serves as a non-linear cross-check on which features matter. Given the modest sample sizes (${R.jds.n_rows} and ${R.sds.n_rows} rows), both models are read as indicative of direction and relative importance, not as production-grade predictors — this limitation is restated in Section 5.`
));

push(heading3("JDS Skill Traits — predicting a high salary hike"));
push(dataTable(
  ["Metric", "Logistic Regression", "Random Forest"],
  [
    ["Test-set size", String(R.jds.logreg.test_size), String(R.jds.logreg.test_size)],
    ["Accuracy", R.jds.logreg.accuracy.toFixed(3), R.jds.rf.accuracy.toFixed(3)],
    ["Precision", R.jds.logreg.precision.toFixed(3), "—"],
    ["Recall", R.jds.logreg.recall.toFixed(3), "—"],
    ["F1 score", R.jds.logreg.f1.toFixed(3), "—"],
  ],
  [2.2, 2.0, 2.0]
));
push(para(`Table 5. JDS classification performance on the held-out test set (n=${R.jds.logreg.test_size}). The logistic-regression confusion matrix is [[${R.jds.logreg.confusion_matrix[0].join(", ")}], [${R.jds.logreg.confusion_matrix[1].join(", ")}]] (rows = actual low/high hike, columns = predicted low/high), i.e. ${R.jds.logreg.confusion_matrix[0][0]+R.jds.logreg.confusion_matrix[1][1]} of ${R.jds.logreg.test_size} test cases correctly classified.`, { italics: true, size: SZ_CAPTION, color: GRAY, align: "center", spacing: { before: 60, after: 200 } }));

push(dataTable(
  ["Skill", "Logistic coefficient (standardised)", "Random-forest importance"],
  (() => {
    const order = ["maths-stats_skills","dashboard_and_storytelling_skills","ai_and_ml_skills","big_data_skills","coding_skills"];
    const label = { dashboard_and_storytelling_skills: "Dashboard & storytelling", "maths-stats_skills": "Maths / statistics", coding_skills: "Coding", ai_and_ml_skills: "AI & ML", big_data_skills: "Big data" };
    return order.map(k => [label[k], R.jds.logreg.coefficients_standardized[k].toFixed(3), R.jds.rf.feature_importance[k].toFixed(3)]);
  })(),
  [2.2, 2.4, 1.8]
));
push(para("Table 6. JDS feature-level drivers from both models, ordered by logistic coefficient. Maths/statistics and dashboarding/storytelling rank highest on both models; big-data ranks lowest on the random forest.", { italics: true, size: SZ_CAPTION, color: GRAY, align: "center", spacing: { before: 60, after: 240 } }));

push(heading3("SDS Personality Traits — predicting senior success"));
push(dataTable(
  ["Metric", "Logistic Regression", "Random Forest"],
  [
    ["Test-set size", String(R.sds.logreg.test_size), String(R.sds.logreg.test_size)],
    ["Accuracy", R.sds.logreg.accuracy.toFixed(3), R.sds.rf.accuracy.toFixed(3)],
    ["Precision", R.sds.logreg.precision.toFixed(3), "—"],
    ["Recall", R.sds.logreg.recall.toFixed(3), "—"],
    ["F1 score", R.sds.logreg.f1.toFixed(3), "—"],
  ],
  [2.2, 2.0, 2.0]
));
push(para(`Table 7. SDS classification performance on the held-out test set (n=${R.sds.logreg.test_size}). Confusion matrix [[${R.sds.logreg.confusion_matrix[0].join(", ")}], [${R.sds.logreg.confusion_matrix[1].join(", ")}]], i.e. ${R.sds.logreg.confusion_matrix[0][0]+R.sds.logreg.confusion_matrix[1][1]} of ${R.sds.logreg.test_size} test cases correctly classified.`, { italics: true, size: SZ_CAPTION, color: GRAY, align: "center", spacing: { before: 60, after: 200 } }));

push(dataTable(
  ["Trait", "Logistic coefficient (standardised)", "Random-forest importance"],
  (() => {
    const order = ["conscientiousness","openness_to_experience","extraversion","neuroticism","agreeableness"];
    const label = { conscientiousness: "Conscientiousness", openness_to_experience: "Openness to experience", extraversion: "Extraversion", agreeableness: "Agreeableness", neuroticism: "Neuroticism" };
    return order.map(k => [label[k], R.sds.logreg.coefficients_standardized[k].toFixed(3), R.sds.rf.feature_importance[k].toFixed(3)]);
  })(),
  [2.2, 2.4, 1.8]
));
push(para("Table 8. SDS feature-level drivers from both models. Conscientiousness and openness rank highest on both models and agree with the correlation analysis in Table 4.", { italics: true, size: SZ_CAPTION, color: GRAY, align: "center", spacing: { before: 60, after: 160 } }));
push(...multiPara(
`One result needs a caution flag rather than a face-value reading: despite a near-zero bivariate correlation with success (r = ${R.sds.corr_with_target.neuroticism}), neuroticism carries a small positive standardised coefficient in the multivariate logistic model (${R.sds.logreg.coefficients_standardized.neuroticism}). Given its negligible univariate relationship and the lowest random-forest importance of all five traits (${R.sds.rf.feature_importance.neuroticism}), this is read as a statistical suppression effect arising from neuroticism's correlation with the other traits, not as evidence that neuroticism independently drives success. This note treats conscientiousness and openness — which agree across the correlation analysis and both models — as the reliable drivers, and reports the neuroticism coefficient as a modelling artefact rather than a finding to act on.`
));
push(spacer(160));

// -------------------------------------------------------------------
push(heading2("4.4  Cross-Dataset Synthesis"));
push(...multiPara(
`Read together, the four files tell a connected story. The two technical competencies that most separate higher- and lower-rewarded junior data scientists internally — quantitative/statistics skill and dashboarding-and-storytelling skill — map directly onto skills the external market actively pays for: Python, SQL, machine learning and "data analysis" / "business analysis" all rank among the most-requested skills in the Analytics Jobs file (Figure 7), and SAS itself appears 715 times. This cross-check suggests the internal JDS skill-scoring rubric is reasonably well aligned with what the market rewards, rather than measuring something idiosyncratic to one employer.

On the compensation side, the roughly fourfold gap between the average Data Analyst and Senior Data Scientist salaries in the Data Science Jobs file (Figure 3) quantifies why the junior-to-senior transition matters financially. The SDS findings (Tables 4 and 8) indicate that this transition is predicted far more by conscientiousness and openness to experience than by any additional technical credential measured in this data. Together, the two workforce files describe two distinct, sequential gates on the path from junior to senior data scientist: a technical gate, passed through quantitative depth and communication skill, and a behavioural gate, passed through conscientiousness and openness — not through further accumulation of technical tooling.`
));

push(pageBreak());
