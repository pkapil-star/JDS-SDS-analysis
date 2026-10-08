"""
Build cleaned/index.html: a self-contained web page that shows the cleaned datasets.
Usage: python build_dashboard.py            (run from anywhere; paths are relative to this file)
Reads the 4 cleaned CSVs + cleaning_log.md (+ raw files for before/after examples),
embeds aggregates and table rows as JSON into dashboard_template.html.
"""
import json, re
from collections import Counter
from datetime import date
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "Grayhat" / "SAS Data Problem Statement and Instructions Hackathon"


def rows(df):
    df = df.astype(object).where(df.notna(), None)
    out = []
    for r in df.values.tolist():
        out.append([round(v, 3) if isinstance(v, float) else v for v in r])
    return out


def pairs(s, n=None):
    s = s.head(n) if n else s
    return [[str(k), round(float(v), 3)] for k, v in s.items()]


# ------------------------------------------------------------------ cleaning log
log = {}
for line in (HERE / "cleaning_log.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|$", line)
    if m and m.group(1) not in ("File", "---"):
        log.setdefault(m.group(1), []).append((m.group(2), m.group(3)))


def steps(name):
    out, counts = [], {}
    for step, detail in log.get(name, []):
        if step in ("raw rows", "final rows"):
            counts[step] = int(re.match(r"\d+", detail).group())
            continue
        kind = "transform"
        if step in ("duplicates",) and not detail.startswith("dropped 0"):
            kind = "drop"
        elif step in ("spam flag", "outliers", "id", "reference_no"):
            kind = "flag"
        elif step in ("consistency", "range", "target balance", "scale", "exact duplicates"):
            kind = "check"
        out.append({"kind": kind, "step": step, "detail": detail})
    return out, counts.get("raw rows"), counts.get("final rows")


datasets = []

# ------------------------------------------------------------------ 1. Analytics Jobs
a = pd.read_csv(HERE / "Analytics_Jobs_clean.csv")
v = a[a.is_spam_posting == 0]
st, raw_n, fin_n = steps("Analytics Jobs")

band = (a.groupby("salary").agg(n=("salary", "size"), lo=("sal_min_lpa", "first"), hi=("sal_max_lpa", "first"))
        .sort_values("lo"))
skills = Counter()
for ks in v.key_skills[v.key_skills != "Not specified"]:
    for k in str(ks).split(","):
        k = k.strip()
        if k and not k.endswith("..."):
            skills[k.lower()] += 1
exp_bins = pd.cut(v.exp_mid_yrs, [-0.1, 2, 5, 8, 12, 100], labels=["0-2 yrs", "2-5 yrs", "5-8 yrs", "8-12 yrs", "12+ yrs"])
miss = (a.isna().mean() * 100).round(1)
loc_ex = a[a.location != a.location_clean].drop_duplicates("location").head(6)
a_ex = [
    {"title": "Location normalised", "headers": ["location (raw)", "location_clean", "primary_city", "num_locations"],
     "rows": rows(loc_ex[["location", "location_clean", "primary_city", "num_locations"]])},
    {"title": "Experience & salary bands parsed to numbers",
     "headers": ["experience (raw)", "exp_min_yrs", "exp_max_yrs", "salary (raw)", "sal_min_lpa", "sal_max_lpa", "sal_mid_lpa"],
     "rows": rows(a.drop_duplicates(["experience", "salary"]).head(6)[
         ["experience", "exp_min_yrs", "exp_max_yrs", "salary", "sal_min_lpa", "sal_max_lpa", "sal_mid_lpa"]])},
    {"title": "Postings flagged as spam (is_spam_posting = 1)", "headers": ["job_desig", "salary", "primary_city"],
     "rows": rows(a[a.is_spam_posting == 1].head(6)[["job_desig", "salary", "primary_city"]])},
]
tcols = ["s_no", "job_desig", "role_family", "experience", "exp_mid_yrs", "salary", "sal_mid_lpa",
         "primary_city", "num_locations", "location_clean", "key_skills", "job_type", "is_spam_posting"]
t = a[tcols].copy()
t["key_skills"] = t.key_skills.str.slice(0, 80)
datasets.append({
    "key": "analytics", "name": "Analytics Jobs", "file": "Analytics_Jobs_clean.csv",
    "desc": "Job postings scraped for analytics roles: designation, experience band, salary band, location, skills.",
    "raw": raw_n, "clean": fin_n, "cols_raw": 8, "cols_clean": a.shape[1],
    "kpis": [
        {"label": "Rows kept", "value": f"{fin_n:,}", "hint": f"of {raw_n:,} raw"},
        {"label": "Duplicates dropped", "value": f"{raw_n - fin_n:,}", "hint": "identical except s_no", "tone": "drop"},
        {"label": "Spam postings flagged", "value": f"{int(a.is_spam_posting.sum())}", "hint": "kept, excluded from EDA", "tone": "flag"},
        {"label": "Primary cities", "value": f"{a.primary_city.nunique()}", "hint": "after spelling merge"},
        {"label": "Median salary (mid)", "value": f"{v.sal_mid_lpa.median():.1f} LPA", "hint": "non-spam postings"},
    ],
    "steps": st,
    "charts": [
        {"type": "cols", "title": "Salary band distribution", "sub": "Postings per band (LPA), all rows",
         "items": [[f"{lo:g}-{hi:g}", int(n)] for _, (n, lo, hi) in band.iterrows()], "fmt": "int"},
        {"type": "bars", "title": "Role family", "sub": "Derived from job_desig, spam excluded",
         "items": pairs(v.role_family.value_counts()), "fmt": "int"},
        {"type": "bars", "title": "Top primary cities", "sub": "After Gurugram→Gurgaon, Bangalore→Bengaluru etc.",
         "items": pairs(v.primary_city.value_counts(), 10), "fmt": "int"},
        {"type": "bars", "title": "Median salary by experience", "sub": "sal_mid_lpa grouped by exp_mid_yrs",
         "items": pairs(v.groupby(exp_bins, observed=True).sal_mid_lpa.median()), "fmt": "lpa"},
        {"type": "bars", "title": "Top skills mentioned", "sub": "Split from key_skills, case-insensitive",
         "items": [[k.title() if k.islower() else k, n] for k, n in skills.most_common(12)], "fmt": "int"},
        {"type": "bars", "title": "Missing values remaining", "sub": "% of rows; kept as NaN by design", "tone": "accent",
         "items": pairs(miss[miss > 0].sort_values(ascending=False)), "fmt": "pct"},
    ],
    "examples": a_ex,
    "table": {"cols": tcols, "rows": rows(t), "flag": tcols.index("is_spam_posting"), "flag_label": "Spam only",
              "new": ["exp_mid_yrs", "sal_mid_lpa", "primary_city", "num_locations", "location_clean", "is_spam_posting", "role_family"]},
})

# ------------------------------------------------------------------ 2. DataScience Jobs
j = pd.read_csv(HERE / "DataScience_Jobs_clean.csv")
jr = pd.read_csv(RAW / "DataScience Jobs.csv")
st, raw_n, fin_n = steps("DataScience Jobs")
j["any_outlier"] = (j.outlier_num_of_jobs | j.outlier_exp | j.outlier_salary).astype(int)
ex = pd.concat([jr[["avg_salary", "min_salary", "max_salary"]].add_suffix(" (raw)"),
                j[["avg_salary_lpa", "min_salary_lpa", "max_salary_lpa", "salary_range_lpa"]]], axis=1)
jcols = ["reference_no", "company_name", "job_title", "role_family", "is_senior", "min_experience", "num_of_jobs",
         "avg_salary_lpa", "min_salary_lpa", "max_salary_lpa", "salary_range_lpa",
         "outlier_num_of_jobs", "outlier_exp", "outlier_salary", "any_outlier"]
datasets.append({
    "key": "datascience", "name": "DataScience Jobs", "file": "DataScience_Jobs_clean.csv",
    "desc": "Company-level data-science openings with min experience, number of jobs and salary (avg/min/max).",
    "raw": raw_n, "clean": fin_n, "cols_raw": jr.shape[1], "cols_clean": j.shape[1] - 1,
    "kpis": [
        {"label": "Rows kept", "value": f"{fin_n:,}", "hint": "no true duplicates"},
        {"label": "Companies", "value": f"{j.company_name.nunique():,}", "hint": f"{j.role_family.nunique()} role families"},
        {"label": "Rows with an outlier flag", "value": f"{int(j.any_outlier.sum())}", "hint": "flagged, not removed", "tone": "flag"},
        {"label": "Shared reference_no", "value": "276", "hint": "different roles, not a key", "tone": "flag"},
        {"label": "Median avg salary", "value": f"{j.avg_salary_lpa.median():.1f} LPA", "hint": f"total openings {int(j.num_of_jobs.sum()):,}"},
    ],
    "steps": st,
    "charts": [
        {"type": "bars", "title": "Median salary by role", "sub": "avg_salary_lpa, Senior merged into role family",
         "items": pairs(j.groupby("role_family").avg_salary_lpa.median().sort_values(ascending=False)), "fmt": "lpa"},
        {"type": "bars", "title": "Most openings by company", "sub": "Sum of num_of_jobs",
         "items": pairs(j.groupby("company_name").num_of_jobs.sum().sort_values(ascending=False), 10), "fmt": "int"},
        {"type": "grouped", "title": "Senior vs non-senior pay", "sub": "Median LPA by role family",
         "cats": sorted(j.role_family.unique()),
         "series": [{"name": "Senior", "tone": "primary",
                     "values": [round(float(x), 2) for x in j[j.is_senior == 1].groupby("role_family").avg_salary_lpa.median().reindex(sorted(j.role_family.unique())).fillna(0)]},
                    {"name": "Non-senior", "tone": "muted",
                     "values": [round(float(x), 2) for x in j[j.is_senior == 0].groupby("role_family").avg_salary_lpa.median().reindex(sorted(j.role_family.unique())).fillna(0)]}],
         "fmt": "lpa"},
        {"type": "cols", "title": "Median salary by min experience", "sub": "avg_salary_lpa per year of min_experience",
         "items": pairs(j.groupby("min_experience").avg_salary_lpa.median()), "fmt": "lpa"},
        {"type": "bars", "title": "Outlier flags (IQR)", "sub": "Rows flagged per rule, kept in data", "tone": "accent",
         "items": [["num_of_jobs", int(j.outlier_num_of_jobs.sum())], ["avg_salary", int(j.outlier_salary.sum())],
                   ["min_experience ≥ 13", int(j.outlier_exp.sum())]], "fmt": "int"},
    ],
    "examples": [{"title": "Salary strings converted to numbers", "headers": list(ex.columns), "rows": rows(ex.head(6))}],
    "table": {"cols": jcols, "rows": rows(j[jcols]), "flag": jcols.index("any_outlier"), "flag_label": "Outliers only",
              "new": ["avg_salary_lpa", "min_salary_lpa", "max_salary_lpa", "salary_range_lpa", "role_family", "is_senior",
                      "outlier_num_of_jobs", "outlier_exp", "outlier_salary", "any_outlier"]},
})

# ------------------------------------------------------------------ 3. JDS Skill Traits
s = pd.read_csv(HERE / "JDS_Skill_Traits_clean.csv")
sr = pd.read_excel(RAW / "JDS Skill Traits.xlsx")
st, raw_n, fin_n = steps("JDS Skill Traits")
feat = [c for c in s.columns if c.endswith("_skills")]
srf = sr.copy()
srf.columns = [c.strip().replace("-", "_") for c in srf.columns]
dup = srf[srf.duplicated(feat + ["salary_hike_high_or_low"], keep=False)].sort_values(feat).head(8)
by = s.groupby("salary_hike_high_or_low")[feat].mean()
datasets.append({
    "key": "jds", "name": "JDS Skill Traits", "file": "JDS_Skill_Traits_clean.csv",
    "desc": "Self-rated skill scores (1–5) of data scientists and whether they got a high salary hike.",
    "raw": raw_n, "clean": fin_n, "cols_raw": sr.shape[1], "cols_clean": s.shape[1],
    "kpis": [
        {"label": "Rows kept", "value": f"{fin_n}", "hint": f"of {raw_n} raw"},
        {"label": "Copy-paste duplicates", "value": f"{raw_n - fin_n}", "hint": "same scores, new id", "tone": "drop"},
        {"label": "id conflicts", "value": f"{int(s.id_conflict.sum())}", "hint": "rows flagged", "tone": "flag"},
        {"label": "High hike / low hike", "value": f"{int((s.salary_hike_high_or_low == 1).sum())} / {int((s.salary_hike_high_or_low == 0).sum())}", "hint": "balanced target"},
        {"label": "Mean skill score", "value": f"{s.total_skill_score.mean():.2f}", "hint": "of 5, all in range"},
    ],
    "steps": st,
    "charts": [
        {"type": "grouped", "title": "Average skill score by hike outcome", "sub": "Scale 1–5",
         "cats": [c.replace("_skills", "").replace("_", " ") for c in feat], "domain": [0, 5],
         "series": [{"name": "High hike (1)", "tone": "primary", "values": [round(float(x), 2) for x in by.loc[1]]},
                    {"name": "Low hike (0)", "tone": "muted", "values": [round(float(x), 2) for x in by.loc[0]]}],
         "fmt": "num"},
        {"type": "split", "title": "Target balance", "sub": "salary_hike_high_or_low",
         "items": [["High hike (1)", int((s.salary_hike_high_or_low == 1).sum()), "primary"],
                   ["Low hike (0)", int((s.salary_hike_high_or_low == 0).sum()), "muted"]]},
        {"type": "bars", "title": "Share of perfect 5.0 scores", "sub": "Ceiling effect per skill", "tone": "accent",
         "items": [[c.replace("_skills", "").replace("_", " "), round(float((s[c] == 5).mean() * 100), 1)] for c in feat], "fmt": "pct"},
    ],
    "examples": [
        {"title": "Column renamed", "headers": ["raw column", "clean column"],
         "rows": [[r, c] for r, c in zip(sr.columns, s.columns) if r != c]},
        {"title": "Duplicate groups found in raw file (first kept)", "headers": ["id"] + feat + ["salary_hike_high_or_low"],
         "rows": rows(dup[["id"] + feat + ["salary_hike_high_or_low"]])},
    ],
    "table": {"cols": list(s.columns), "rows": rows(s), "flag": list(s.columns).index("id_conflict"), "flag_label": "id conflicts only",
              "new": ["id_conflict", "total_skill_score", "maths_stats_skills"]},
})

# ------------------------------------------------------------------ 4. SDS Personality Traits
p = pd.read_csv(HERE / "SDS_Personality_Traits_clean.csv")
pr = pd.read_excel(RAW / "SDS Personality Traits.xlsx")
st, raw_n, fin_n = steps("SDS Personality Traits")
traits = ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]
p["any_flag"] = (p.id_conflict | p[[f"outlier_{t}" for t in traits]].max(axis=1)).astype(int)
byp = p.groupby("success_high_low")[traits].mean()
pcols = ["id"] + traits + ["success_high_low", "id_conflict", "outlier_agreeableness", "any_flag"]
datasets.append({
    "key": "sds", "name": "SDS Personality Traits", "file": "SDS_Personality_Traits_clean.csv",
    "desc": "Big-Five personality scores of data scientists and a high/low career success label.",
    "raw": raw_n, "clean": fin_n, "cols_raw": pr.shape[1], "cols_clean": p.shape[1] - 1,
    "kpis": [
        {"label": "Rows kept", "value": f"{fin_n}", "hint": "no exact duplicates"},
        {"label": "Headers fixed", "value": "2", "hint": "stray spaces removed"},
        {"label": "id conflicts", "value": f"{int(p.id.duplicated().sum())}", "hint": f"{int(p.id_conflict.sum())} rows flagged", "tone": "flag"},
        {"label": "IQR outliers", "value": f"{int(p[[f'outlier_{t}' for t in traits]].values.sum())}", "hint": "all in agreeableness", "tone": "flag"},
        {"label": "High / low success", "value": f"{int((p.success_high_low == 1).sum())} / {int((p.success_high_low == 0).sum())}", "hint": "balanced target"},
    ],
    "steps": st,
    "charts": [
        {"type": "grouped", "title": "Average trait score by success", "sub": "Normalised scores (~17–68)",
         "cats": [t.replace("_", " ") for t in traits],
         "series": [{"name": "High success (1)", "tone": "primary", "values": [round(float(x), 1) for x in byp.loc[1]]},
                    {"name": "Low success (0)", "tone": "muted", "values": [round(float(x), 1) for x in byp.loc[0]]}],
         "fmt": "num1"},
        {"type": "split", "title": "Target balance", "sub": "success_high_low",
         "items": [["High success (1)", int((p.success_high_low == 1).sum()), "primary"],
                   ["Low success (0)", int((p.success_high_low == 0).sum()), "muted"]]},
        {"type": "bars", "title": "Trait score range", "sub": "min – max in cleaned data", "range": True,
         "items": [[t.replace("_", " "), int(p[t].min()), int(p[t].max())] for t in traits], "fmt": "int"},
    ],
    "examples": [{"title": "Columns renamed", "headers": ["raw column", "clean column"],
                  "rows": [[repr(r), c] for r, c in zip(pr.columns, p.columns) if r != c]}],
    "table": {"cols": pcols, "rows": rows(p[pcols]), "flag": pcols.index("any_flag"), "flag_label": "Flagged only",
              "new": ["success_high_low", "id_conflict", "outlier_agreeableness", "any_flag"]},
})

charts = sorted(f.name for f in (HERE / "charts").glob("*.png"))
data = {"datasets": datasets, "gallery": charts, "built": date.today().isoformat()}
tpl = (HERE / "dashboard_template.html").read_text(encoding="utf-8")
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
(HERE / "index.html").write_text(tpl.replace("/*__DATA__*/null", payload), encoding="utf-8")
print(f"wrote index.html ({(HERE / 'index.html').stat().st_size / 1e6:.2f} MB)")
