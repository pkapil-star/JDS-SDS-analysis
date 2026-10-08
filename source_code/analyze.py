import sys, json, re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

base = sys.argv[1]
outdir = sys.argv[2]

COLOR_PRIMARY = "#2C5F8A"
COLOR_SECOND = "#E07B39"
COLOR_GRID = "#D9D9D9"
plt.rcParams.update({
    "font.size": 10,
    "axes.edgecolor": "#444444",
    "axes.grid": True,
    "grid.color": COLOR_GRID,
    "grid.linewidth": 0.6,
    "axes.axisbelow": True,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

results = {}

# ---------------------------------------------------------------
# 1. Data Science Jobs
# ---------------------------------------------------------------
ds = pd.read_csv(f"{base}/DataScience Jobs.csv")

def parse_lakh(x):
    if pd.isna(x):
        return np.nan
    x = str(x).strip().upper().replace("L", "")
    try:
        return float(x)
    except ValueError:
        return np.nan

for col in ["avg_salary", "min_salary", "max_salary"]:
    ds[col + "_num"] = ds[col].apply(parse_lakh)

results["ds_jobs"] = {
    "n_rows": int(len(ds)),
    "n_companies": int(ds["company_name"].nunique()),
    "n_job_titles": int(ds["job_title"].nunique()),
    "total_postings_sum_num_of_jobs": int(ds["num_of_jobs"].sum()),
    "avg_salary_lakh_mean": round(float(ds["avg_salary_num"].mean()), 2),
    "avg_salary_lakh_median": round(float(ds["avg_salary_num"].median()), 2),
    "min_salary_lakh_mean": round(float(ds["min_salary_num"].mean()), 2),
    "max_salary_lakh_mean": round(float(ds["max_salary_num"].mean()), 2),
    "min_experience_mean": round(float(ds["min_experience"].mean()), 2),
    "min_experience_median": float(ds["min_experience"].median()),
    "corr_experience_avgsalary": round(float(ds["min_experience"].corr(ds["avg_salary_num"])), 3),
    "corr_numjobs_avgsalary": round(float(ds["num_of_jobs"].corr(ds["avg_salary_num"])), 3),
    "top_job_titles": ds["job_title"].value_counts().head(10).to_dict(),
}

top_companies = ds.groupby("company_name")["num_of_jobs"].sum().sort_values(ascending=False).head(12)
results["ds_jobs"]["top_companies_by_postings"] = top_companies.to_dict()

top_titles = ds["job_title"].value_counts().head(8).index.tolist()
sal_by_title = ds[ds["job_title"].isin(top_titles)].groupby("job_title")["avg_salary_num"].mean().sort_values(ascending=False)
results["ds_jobs"]["avg_salary_by_title_lakh"] = {k: round(v, 2) for k, v in sal_by_title.to_dict().items()}

fig, ax = plt.subplots(figsize=(7.5, 4.2))
top_companies.sort_values().plot(kind="barh", ax=ax, color=COLOR_PRIMARY)
ax.set_xlabel("Total job postings (sum of num_of_jobs)")
ax.set_ylabel("")
ax.set_title("Top 12 Companies by Data Science Job Postings (2024-25)")
plt.tight_layout()
plt.savefig(f"{outdir}/ds_top_companies.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(7.5, 4.2))
sal_by_title.sort_values().plot(kind="barh", ax=ax, color=COLOR_SECOND)
ax.set_xlabel("Average salary (INR Lakh p.a.)")
ax.set_ylabel("")
ax.set_title("Average Offered Salary by Data Science Job Title")
plt.tight_layout()
plt.savefig(f"{outdir}/ds_salary_by_title.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.scatter(ds["min_experience"], ds["avg_salary_num"], alpha=0.35, s=18, color=COLOR_PRIMARY, edgecolors="none")
mask = ds["min_experience"].notna() & ds["avg_salary_num"].notna()
z = np.polyfit(ds.loc[mask, "min_experience"], ds.loc[mask, "avg_salary_num"], 1)
xs = np.linspace(ds["min_experience"].min(), ds["min_experience"].max(), 50)
ax.plot(xs, np.poly1d(z)(xs), color=COLOR_SECOND, linewidth=2)
ax.set_xlabel("Minimum experience required (years)")
ax.set_ylabel("Average salary (INR Lakh p.a.)")
ax.set_title("Experience vs Average Salary — Data Science Jobs")
plt.tight_layout()
plt.savefig(f"{outdir}/ds_experience_vs_salary.png", dpi=160)
plt.close()

# ---------------------------------------------------------------
# 2. Analytics Jobs
# ---------------------------------------------------------------
an = pd.read_csv(f"{base}/Analytics Jobs.csv")

def exp_bounds(x):
    if pd.isna(x):
        return (np.nan, np.nan)
    m = re.findall(r"\d+", str(x))
    if len(m) >= 2:
        return (float(m[0]), float(m[1]))
    elif len(m) == 1:
        return (float(m[0]), float(m[0]))
    return (np.nan, np.nan)

bounds = an["experience"].apply(exp_bounds)
an["exp_min"] = bounds.apply(lambda t: t[0])
an["exp_max"] = bounds.apply(lambda t: t[1])
an["exp_mid"] = (an["exp_min"] + an["exp_max"]) / 2

results["an_jobs"] = {
    "n_rows": int(len(an)),
    "n_unique_designations": int(an["job_desig"].nunique()),
    "n_unique_locations_raw": int(an["location"].nunique()),
    "pct_missing_job_description": round(100 * an["job_description"].isna().mean(), 1),
    "pct_missing_job_type": round(100 * an["job_type"].isna().mean(), 1),
    "pct_missing_key_skills": round(100 * an["key_skills"].isna().mean(), 1),
    "exp_mid_mean": round(float(an["exp_mid"].mean()), 2),
    "top_designations": an["job_desig"].value_counts().head(10).to_dict(),
    "salary_bucket_counts": an["salary"].value_counts().to_dict(),
    "job_type_counts_nonnull": an["job_type"].value_counts().to_dict(),
}

an["primary_location"] = an["location"].apply(lambda s: str(s).split(",")[0].strip())
top_locs = an["primary_location"].value_counts().head(12)
results["an_jobs"]["top_primary_locations"] = top_locs.to_dict()

skill_counter = {}
for s in an["key_skills"].dropna():
    for tok in str(s).split(","):
        tok = tok.strip().lower()
        if len(tok) < 2:
            continue
        skill_counter[tok] = skill_counter.get(tok, 0) + 1
top_skills = pd.Series(skill_counter).sort_values(ascending=False).head(15)
results["an_jobs"]["top_key_skills"] = top_skills.to_dict()

fig, ax = plt.subplots(figsize=(7.5, 4.2))
an["job_desig"].value_counts().head(12).sort_values().plot(kind="barh", ax=ax, color=COLOR_PRIMARY)
ax.set_xlabel("Number of job postings")
ax.set_ylabel("")
ax.set_title("Top 12 Job Designations — Analytics Jobs Dataset")
plt.tight_layout()
plt.savefig(f"{outdir}/an_top_designations.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(7.5, 4.2))
order = an["salary"].value_counts().index.tolist()
an["salary"].value_counts().loc[order].plot(kind="bar", ax=ax, color=COLOR_SECOND)
ax.set_xlabel("Salary band (INR Lakh p.a.)")
ax.set_ylabel("Number of postings")
ax.set_title("Salary Band Distribution — Analytics Jobs")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{outdir}/an_salary_bands.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(7.5, 4.2))
top_locs.sort_values().plot(kind="barh", ax=ax, color=COLOR_PRIMARY)
ax.set_xlabel("Number of postings (primary location)")
ax.set_ylabel("")
ax.set_title("Top 12 Hiring Locations — Analytics Jobs")
plt.tight_layout()
plt.savefig(f"{outdir}/an_top_locations.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(7.5, 4.6))
top_skills.sort_values().plot(kind="barh", ax=ax, color=COLOR_SECOND)
ax.set_xlabel("Frequency of mention")
ax.set_ylabel("")
ax.set_title("Top 15 Key Skills Requested — Analytics Jobs")
plt.tight_layout()
plt.savefig(f"{outdir}/an_top_skills.png", dpi=160)
plt.close()

# ---------------------------------------------------------------
# 3. JDS Skill Traits (Junior Data Scientists)
# ---------------------------------------------------------------
jds = pd.read_excel(f"{base}/JDS Skill Traits.xlsx")
jds.columns = [c.strip() for c in jds.columns]
skill_cols = ["big_data_skills", "maths-stats_skills", "coding_skills", "ai_and_ml_skills", "dashboard_and_storytelling_skills"]
target = "salary_hike_high_or_low"

corr_jds = jds[skill_cols + [target]].corr()[target].drop(target).sort_values(ascending=False)
results["jds"] = {
    "n_rows": int(len(jds)),
    "pct_high_hike": round(100 * jds[target].mean(), 1),
    "skill_means_overall": {c: round(float(jds[c].mean()), 2) for c in skill_cols},
    "skill_means_by_class": jds.groupby(target)[skill_cols].mean().round(2).to_dict(),
    "corr_with_target": {k: round(float(v), 3) for k, v in corr_jds.items()},
}

X = jds[skill_cols].values
y = jds[target].values
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
scaler = StandardScaler().fit(Xtr)
Xtr_s, Xte_s = scaler.transform(Xtr), scaler.transform(Xte)
clf = LogisticRegression(max_iter=1000).fit(Xtr_s, ytr)
pred = clf.predict(Xte_s)
results["jds"]["logreg"] = {
    "test_size": int(len(yte)),
    "accuracy": round(float(accuracy_score(yte, pred)), 3),
    "precision": round(float(precision_score(yte, pred)), 3),
    "recall": round(float(recall_score(yte, pred)), 3),
    "f1": round(float(f1_score(yte, pred)), 3),
    "coefficients_standardized": {c: round(float(w), 3) for c, w in zip(skill_cols, clf.coef_[0])},
}
cm = confusion_matrix(yte, pred)
results["jds"]["logreg"]["confusion_matrix"] = cm.tolist()

rf = RandomForestClassifier(n_estimators=300, random_state=42, max_depth=4).fit(Xtr, ytr)
rf_pred = rf.predict(Xte)
results["jds"]["rf"] = {
    "accuracy": round(float(accuracy_score(yte, rf_pred)), 3),
    "feature_importance": {c: round(float(w), 3) for c, w in zip(skill_cols, rf.feature_importances_)},
}

fig, ax = plt.subplots(figsize=(7.5, 4.2))
means_by_class = jds.groupby(target)[skill_cols].mean()
means_by_class.index = ["Low hike (0)", "High hike (1)"]
means_by_class.T.plot(kind="bar", ax=ax, color=[COLOR_SECOND, COLOR_PRIMARY])
ax.set_ylabel("Mean skill score (1-5 scale)")
ax.set_xlabel("")
ax.set_title("JDS Skill Profile by Salary-Hike Outcome")
plt.xticks(rotation=25, ha="right")
ax.legend(title="")
plt.tight_layout()
plt.savefig(f"{outdir}/jds_skills_by_class.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(6.2, 5.2))
corr_full = jds[skill_cols + [target]].corr()
im = ax.imshow(corr_full.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr_full.columns)))
ax.set_yticks(range(len(corr_full.columns)))
ax.set_xticklabels(corr_full.columns, rotation=45, ha="right", fontsize=8)
ax.set_yticklabels(corr_full.columns, fontsize=8)
for i in range(len(corr_full.columns)):
    for j in range(len(corr_full.columns)):
        ax.text(j, i, f"{corr_full.values[i,j]:.2f}", ha="center", va="center", fontsize=7,
                 color="white" if abs(corr_full.values[i, j]) > 0.5 else "black")
ax.set_title("Correlation Matrix — JDS Skill Traits")
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig(f"{outdir}/jds_corr_heatmap.png", dpi=160)
plt.close()

# ---------------------------------------------------------------
# 4. SDS Personality Traits (Senior Data Scientists)
# ---------------------------------------------------------------
sds = pd.read_excel(f"{base}/SDS Personality Traits.xlsx")
sds.columns = [c.strip() for c in sds.columns]
trait_cols = ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]
target_s = "success_ classification_ high_low"
sds.rename(columns={target_s: "success_high_low"}, inplace=True)
target_s = "success_high_low"

corr_sds = sds[trait_cols + [target_s]].corr()[target_s].drop(target_s).sort_values(ascending=False)
results["sds"] = {
    "n_rows": int(len(sds)),
    "pct_high_success": round(100 * sds[target_s].mean(), 1),
    "trait_means_overall": {c: round(float(sds[c].mean()), 1) for c in trait_cols},
    "trait_means_by_class": sds.groupby(target_s)[trait_cols].mean().round(1).to_dict(),
    "corr_with_target": {k: round(float(v), 3) for k, v in corr_sds.items()},
}

Xs = sds[trait_cols].values
ys = sds[target_s].values
Xtr, Xte, ytr, yte = train_test_split(Xs, ys, test_size=0.25, random_state=42, stratify=ys)
scaler2 = StandardScaler().fit(Xtr)
Xtr_s, Xte_s = scaler2.transform(Xtr), scaler2.transform(Xte)
clf2 = LogisticRegression(max_iter=1000).fit(Xtr_s, ytr)
pred2 = clf2.predict(Xte_s)
results["sds"]["logreg"] = {
    "test_size": int(len(yte)),
    "accuracy": round(float(accuracy_score(yte, pred2)), 3),
    "precision": round(float(precision_score(yte, pred2)), 3),
    "recall": round(float(recall_score(yte, pred2)), 3),
    "f1": round(float(f1_score(yte, pred2)), 3),
    "coefficients_standardized": {c: round(float(w), 3) for c, w in zip(trait_cols, clf2.coef_[0])},
}
cm2 = confusion_matrix(yte, pred2)
results["sds"]["logreg"]["confusion_matrix"] = cm2.tolist()

rf2 = RandomForestClassifier(n_estimators=300, random_state=42, max_depth=4).fit(Xtr, ytr)
rf2_pred = rf2.predict(Xte)
results["sds"]["rf"] = {
    "accuracy": round(float(accuracy_score(yte, rf2_pred)), 3),
    "feature_importance": {c: round(float(w), 3) for c, w in zip(trait_cols, rf2.feature_importances_)},
}

fig, ax = plt.subplots(figsize=(7.5, 4.2))
means_by_class_s = sds.groupby(target_s)[trait_cols].mean()
means_by_class_s.index = ["Low success (0)", "High success (1)"]
means_by_class_s.T.plot(kind="bar", ax=ax, color=[COLOR_SECOND, COLOR_PRIMARY])
ax.set_ylabel("Mean trait score")
ax.set_xlabel("")
ax.set_title("SDS Big-Five Trait Profile by Success Outcome")
plt.xticks(rotation=20, ha="right")
ax.legend(title="")
plt.tight_layout()
plt.savefig(f"{outdir}/sds_traits_by_class.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(6.2, 5.2))
corr_full_s = sds[trait_cols + [target_s]].corr()
im = ax.imshow(corr_full_s.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr_full_s.columns)))
ax.set_yticks(range(len(corr_full_s.columns)))
ax.set_xticklabels(corr_full_s.columns, rotation=45, ha="right", fontsize=8)
ax.set_yticklabels(corr_full_s.columns, fontsize=8)
for i in range(len(corr_full_s.columns)):
    for j in range(len(corr_full_s.columns)):
        ax.text(j, i, f"{corr_full_s.values[i,j]:.2f}", ha="center", va="center", fontsize=7,
                 color="white" if abs(corr_full_s.values[i, j]) > 0.5 else "black")
ax.set_title("Correlation Matrix — SDS Personality Traits")
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig(f"{outdir}/sds_corr_heatmap.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(7.5, 4.2))
sds[trait_cols].plot(kind="box", ax=ax, color=dict(boxes=COLOR_PRIMARY, whiskers=COLOR_PRIMARY, medians=COLOR_SECOND, caps=COLOR_PRIMARY))
ax.set_ylabel("Score")
ax.set_title("Distribution of Big-Five Trait Scores — SDS Dataset")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(f"{outdir}/sds_boxplot.png", dpi=160)
plt.close()

with open(f"{outdir}/results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)

print(json.dumps(results, indent=2, default=str))
