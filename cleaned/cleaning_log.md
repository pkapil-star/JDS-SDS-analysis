# Data Cleaning Log

| File | Step | Detail |
|---|---|---|
| Analytics Jobs | raw rows | 15841 |
| Analytics Jobs | whitespace | stripped leading/trailing/double spaces in text columns (50 job_desig had them) |
| Analytics Jobs | job_type | standardised case/typos to 'Analytics'; 76% still missing (kept as NaN, not imputable) |
| Analytics Jobs | duplicates | dropped 1001 duplicate postings (all columns identical except s_no) |
| Analytics Jobs | experience | parsed into exp_min/max/mid_yrs; unparsed=0 |
| Analytics Jobs | salary | salary is a BAND (0to3, 3to6, 6to10, 10to15, 15to25, 25to50 LPA) -> sal_min/max/mid_lpa. Treat mid as approximate. |
| Analytics Jobs | location | unified Gurugram->Gurgaon etc; added primary_city, num_locations (234 distinct primary cities) |
| Analytics Jobs | key_skills | 1 missing -> 'Not specified' |
| Analytics Jobs | job_description | 3371 missing kept as NaN (free text, only used for text mining) |
| Analytics Jobs | spam flag | 121 fake/data-entry style postings flagged (is_spam_posting=1). EXCLUDE from EDA/salary analysis. |
| Analytics Jobs | final rows | 14840 (from 15841) |
| DataScience Jobs | raw rows | 1602 |
| DataScience Jobs | salary | '7.8L' strings -> numeric avg/min/max_salary_lpa |
| DataScience Jobs | consistency | min<=avg<=max violated in 0 rows |
| DataScience Jobs | reference_no | 276 rows share a reference_no but are DIFFERENT companies/roles -> not true duplicates, kept. Don't use reference_no as a key. |
| DataScience Jobs | exact duplicates | 0 (none) |
| DataScience Jobs | outliers | flagged only (not removed): num_of_jobs=164 (max 4200, TCS BA - real mass hiring), min_experience>=13 = 12, avg_salary=39. Use log / median in analysis. |
| DataScience Jobs | final rows | 1602 (from 1602) |
| JDS Skill Traits | raw rows | 139 |
| JDS Skill Traits | columns | renamed maths-stats_skills -> maths_stats_skills (hyphen breaks SAS/SQL) |
| JDS Skill Traits | id | 2 ids repeated with DIFFERENT scores -> flagged id_conflict=1, kept (id is not a key) |
| JDS Skill Traits | duplicates | dropped 21 rows with identical 5 scores + outcome but a different id (copy-paste duplicates) |
| JDS Skill Traits | range | all scores within 1-5: True; no missing values; many 5.0 values (ceiling effect) |
| JDS Skill Traits | target balance | {1: 60, 0: 58} |
| JDS Skill Traits | final rows | 118 (from 139) |
| SDS Personality Traits | raw rows | 161 |
| SDS Personality Traits | columns | fixed ' extraversion' (leading space) and 'success_ classification_ high_low' -> success_high_low |
| SDS Personality Traits | id | 9 ids repeated with DIFFERENT values -> flagged id_conflict=1, kept |
| SDS Personality Traits | exact duplicates | 0 (none) |
| SDS Personality Traits | outliers | IQR flags only (kept): {neuroticism=0, extraversion=0, openness_to_experience=0, agreeableness=5, conscientiousness=0} |
| SDS Personality Traits | scale | scores already normalised (range ~17-68); no rescaling needed for tree models; standardise for logistic regression |
| SDS Personality Traits | target balance | {1: 85, 0: 76} |
| SDS Personality Traits | final rows | 161 (from 161) |
