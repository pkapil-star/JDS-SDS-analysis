"""
SAS Hackathon - Data cleaning (Person 1)
Usage: python3 clean_data.py <input_dir> <output_dir>
Reads the 4 raw files, writes 4 cleaned CSVs + cleaning_log.md
"""
import sys, re
from pathlib import Path
import numpy as np
import pandas as pd

IN, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
log = []


def note(file, step, detail):
    log.append((file, step, detail))
    print(f"[{file}] {step}: {detail}")


def iqr_flag(s, k=1.5):
    q1, q3 = s.quantile([.25, .75])
    return (s < q1 - k * (q3 - q1)) | (s > q3 + k * (q3 - q1))


# ------------------------------------------------------------------ 1. ANALYTICS JOBS
f = "Analytics Jobs"
a = pd.read_csv(IN / "Analytics Jobs.csv")
n0 = len(a)
note(f, "raw rows", n0)

# whitespace
for c in ["job_description", "job_desig", "job_type", "key_skills", "location", "experience", "salary"]:
    a[c] = a[c].astype("string").str.strip()
a["job_desig"] = a["job_desig"].str.replace(r"\s+", " ", regex=True)
note(f, "whitespace", "stripped leading/trailing/double spaces in text columns (50 job_desig had them)")

# job_type: analytics / ANALYTICS / analytic / Analytic -> Analytics
a["job_type"] = a["job_type"].str.lower().str.replace("analytic$", "analytics", regex=True).str.title()
note(f, "job_type", "standardised case/typos to 'Analytics'; 76% still missing (kept as NaN, not imputable)")

# exact duplicates (everything except s_no)
d = a.drop(columns="s_no").duplicated().sum()
a = a.drop_duplicates(subset=[c for c in a.columns if c != "s_no"], keep="first").copy()
note(f, "duplicates", f"dropped {d} duplicate postings (all columns identical except s_no)")

# experience "6-10 yrs" -> numeric
ex = a["experience"].str.extract(r"(\d+)\s*-\s*(\d+)").astype(float)
a["exp_min_yrs"], a["exp_max_yrs"] = ex[0], ex[1]
a["exp_mid_yrs"] = (a.exp_min_yrs + a.exp_max_yrs) / 2
note(f, "experience", f"parsed into exp_min/max/mid_yrs; unparsed={a.exp_min_yrs.isna().sum()}")

# salary buckets "6to10" -> LPA numeric
sl = a["salary"].str.extract(r"(\d+)\s*to\s*(\d+)").astype(float)
a["sal_min_lpa"], a["sal_max_lpa"] = sl[0], sl[1]
a["sal_mid_lpa"] = (a.sal_min_lpa + a.sal_max_lpa) / 2
note(f, "salary", "salary is a BAND (0to3, 3to6, 6to10, 10to15, 15to25, 25to50 LPA) -> sal_min/max/mid_lpa. Treat mid as approximate.")

# location: unify spellings, first city + count of cities
LOC_MAP = {"Gurugram": "Gurgaon", "Bangalore": "Bengaluru", "Bengaluru/Bangalore": "Bengaluru",
           "Delhi/Ncr": "Delhi NCR", "Delhi Ncr": "Delhi NCR", "New Delhi": "Delhi", "Bombay": "Mumbai",
           "Navi Mumbai": "Mumbai", "Mumbai Suburbs": "Mumbai", "Thiruvananthapuram": "Trivandrum",
           "Cochin": "Kochi", "Madras": "Chennai", "Calcutta": "Kolkata", "Dubai/ Uae": "Dubai"}


def clean_loc_part(p):
    p = re.sub(r"\(.*?\)", "", p)          # drop "(Whitefield)" style locality
    p = re.sub(r"\+\d+", "", p)            # drop "+3" suffix
    p = re.sub(r"\s+", " ", p).strip().title()
    return LOC_MAP.get(p, p)


def fix_loc(s):
    s = re.sub(r"\(.*?\)", "", str(s))     # remove brackets first (they can contain commas)
    parts = [clean_loc_part(p) for p in s.split(",")]
    parts = [p for p in parts if p]
    seen = []
    for p in parts:
        if p not in seen:
            seen.append(p)
    return seen


locs = a["location"].map(fix_loc)
a["location_clean"] = locs.map(", ".join)
a["primary_city"] = locs.map(lambda x: x[0] if x else np.nan)
a["num_locations"] = locs.map(len)
note(f, "location", f"unified Gurugram->Gurgaon etc; added primary_city, num_locations ({a.primary_city.nunique()} distinct primary cities)")

# key_skills missing -> explicit label
miss = a["key_skills"].isna().sum()
a["key_skills"] = a["key_skills"].fillna("Not specified")
note(f, "key_skills", f"{miss} missing -> 'Not specified'")
note(f, "job_description", f"{a.job_description.isna().sum()} missing kept as NaN (free text, only used for text mining)")

# spam / non-analytics postings flag
spam_rx = r"data entry|home base|home based|work from home|part time|freelanc|online work|typing|copy paste"
a["is_spam_posting"] = a["job_desig"].str.contains(spam_rx, case=False, regex=True).astype(int)
note(f, "spam flag", f"{a.is_spam_posting.sum()} fake/data-entry style postings flagged (is_spam_posting=1). EXCLUDE from EDA/salary analysis.")

# role family (for EDA grouping)
def role(t):
    t = t.lower()
    for k, v in [("data scien", "Data Scientist"), ("machine learning|ml engineer|ai ", "ML/AI"),
                 ("data engineer|etl|big data|hadoop|spark", "Data Engineer"),
                 ("business analyst", "Business Analyst"), ("data analyst|analyst", "Analyst"),
                 ("seo|digital marketing|marketing", "Marketing"), ("product", "Product"),
                 ("manager|lead|head|director", "Management"), ("developer|engineer|consultant", "Tech/Consulting")]:
        if re.search(k, t):
            return v
    return "Other"


a["role_family"] = a["job_desig"].map(role)
a["job_desig"] = a["job_desig"].str.title()

a = a.reset_index(drop=True)
note(f, "final rows", f"{len(a)} (from {n0})")
a.to_csv(OUT / "Analytics_Jobs_clean.csv", index=False)

# ------------------------------------------------------------------ 2. DATA SCIENCE JOBS
f = "DataScience Jobs"
j = pd.read_csv(IN / "DataScience Jobs.csv")
n0 = len(j)
note(f, "raw rows", n0)
j["company_name"] = j["company_name"].str.strip()
j["job_title"] = j["job_title"].str.strip()

for c in ["avg_salary", "min_salary", "max_salary"]:
    j[c + "_lpa"] = j[c].str.replace("L", "", regex=False).astype(float)
    j = j.drop(columns=c)
note(f, "salary", "'7.8L' strings -> numeric avg/min/max_salary_lpa")

bad = ((j.min_salary_lpa > j.avg_salary_lpa) | (j.avg_salary_lpa > j.max_salary_lpa)).sum()
note(f, "consistency", f"min<=avg<=max violated in {bad} rows")

dup_ref = j.reference_no.duplicated(keep=False).sum()
note(f, "reference_no", f"{dup_ref} rows share a reference_no but are DIFFERENT companies/roles -> not true duplicates, kept. Don't use reference_no as a key.")
note(f, "exact duplicates", f"{j.drop(columns='reference_no').duplicated().sum()} (none)")

j["is_senior"] = j.job_title.str.startswith("Senior").astype(int)
j["role_family"] = j.job_title.str.replace("Senior ", "", regex=False)
j["salary_range_lpa"] = j.max_salary_lpa - j.min_salary_lpa
j["num_of_jobs_log"] = np.log1p(j.num_of_jobs)
j["outlier_num_of_jobs"] = iqr_flag(j.num_of_jobs).astype(int)
j["outlier_exp"] = (j.min_experience >= 13).astype(int)
j["outlier_salary"] = iqr_flag(j.avg_salary_lpa).astype(int)
note(f, "outliers", f"flagged only (not removed): num_of_jobs={j.outlier_num_of_jobs.sum()} (max 4200, TCS BA - real mass hiring), "
     f"min_experience>=13 = {j.outlier_exp.sum()}, avg_salary={j.outlier_salary.sum()}. Use log / median in analysis.")
note(f, "final rows", f"{len(j)} (from {n0})")
j.to_csv(OUT / "DataScience_Jobs_clean.csv", index=False)

# ------------------------------------------------------------------ 3. JDS SKILL TRAITS
f = "JDS Skill Traits"
s = pd.read_excel(IN / "JDS Skill Traits.xlsx")
n0 = len(s)
note(f, "raw rows", n0)
s.columns = [c.strip().replace("-", "_") for c in s.columns]
note(f, "columns", "renamed maths-stats_skills -> maths_stats_skills (hyphen breaks SAS/SQL)")
s["id_conflict"] = s.id.duplicated(keep=False).astype(int)
note(f, "id", f"{s.id.duplicated().sum()} ids repeated with DIFFERENT scores -> flagged id_conflict=1, kept (id is not a key)")
feat = [c for c in s.columns if c.endswith("_skills")]
d = s.duplicated(subset=feat + ["salary_hike_high_or_low"]).sum()
s = s.drop_duplicates(subset=feat + ["salary_hike_high_or_low"], keep="first").reset_index(drop=True)
note(f, "duplicates", f"dropped {d} rows with identical 5 scores + outcome but a different id (copy-paste duplicates)")
rng_ok = s[feat].apply(lambda c: c.between(1, 5)).all().all()
note(f, "range", f"all scores within 1-5: {rng_ok}; no missing values; many 5.0 values (ceiling effect)")
s["total_skill_score"] = s[feat].mean(axis=1).round(2)
note(f, "target balance", s.salary_hike_high_or_low.value_counts().to_dict())
note(f, "final rows", f"{len(s)} (from {n0})")
s.to_csv(OUT / "JDS_Skill_Traits_clean.csv", index=False)

# ------------------------------------------------------------------ 4. SDS PERSONALITY TRAITS
f = "SDS Personality Traits"
p = pd.read_excel(IN / "SDS Personality Traits.xlsx")
n0 = len(p)
note(f, "raw rows", n0)
p.columns = [re.sub(r"\s+", "", c) if c.strip().startswith("success") else c.strip() for c in p.columns]
p = p.rename(columns={"success_classification_high_low": "success_high_low"})
note(f, "columns", "fixed ' extraversion' (leading space) and 'success_ classification_ high_low' -> success_high_low")
p["id_conflict"] = p.id.duplicated(keep=False).astype(int)
note(f, "id", f"{p.id.duplicated().sum()} ids repeated with DIFFERENT values -> flagged id_conflict=1, kept")
traits = ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]
note(f, "exact duplicates", f"{p.drop(columns='id').duplicated().sum()} (none)")
for t in traits:
    p["outlier_" + t] = iqr_flag(p[t]).astype(int)
note(f, "outliers", f"IQR flags only (kept): {{{', '.join(f'{t}={p['outlier_'+t].sum()}' for t in traits)}}}")
note(f, "scale", "scores already normalised (range ~17-68); no rescaling needed for tree models; standardise for logistic regression")
note(f, "target balance", p.success_high_low.value_counts().to_dict())
note(f, "final rows", f"{len(p)} (from {n0})")
p.to_csv(OUT / "SDS_Personality_Traits_clean.csv", index=False)

# ------------------------------------------------------------------ LOG
with open(OUT / "cleaning_log.md", "w") as fh:
    fh.write("# Data Cleaning Log\n\n| File | Step | Detail |\n|---|---|---|\n")
    for r in log:
        fh.write(f"| {r[0]} | {r[1]} | {r[2]} |\n")
print("done")
