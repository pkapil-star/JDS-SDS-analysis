"""
SAS CU Hackathon — EDA on Job Market Data (Person 2's part)
=============================================================
Run this in VS Code / PyCharm. Produces 5 charts (as PNGs in ./charts/)
+ a printed takeaway line for each, ready to paste into the Approach Note
(Section 4.1 — Descriptive / Market Analysis).

UPDATED to use Person 1's CLEANED files (see cleaning_log.md in the
project) instead of the raw CSVs — salary/experience are already numeric,
locations are already deduped into primary_city, and spam postings are
dropped before any analysis (per the cleaning log's own instruction).

SETUP (run once in a terminal):
    pip install pandas matplotlib

FILES EXPECTED (same folder as this script, or edit the paths below):
    DataScience_Jobs_clean.csv
    Analytics_Jobs_clean.csv
"""

import re
import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 0. CONFIG — edit these two paths if your files are named/placed differently
# ----------------------------------------------------------------------
DS_PATH = "DataScience_Jobs_clean.csv"
AJ_PATH = "Analytics_Jobs_clean.csv"
OUT_DIR = "charts"

# Palette (from the house dataviz method — sequential blue for single-series magnitude)
BLUE = "#2a78d6"
INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"
SURFACE = "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": INK,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "font.family": "sans-serif",
    "font.size": 10,
})

os.makedirs(OUT_DIR, exist_ok=True)


# ----------------------------------------------------------------------
# 1. PARSING HELPERS
# ----------------------------------------------------------------------
# Salary and experience are already numeric in the cleaned files
# (avg_salary_lpa, sal_mid_lpa, min_experience, exp_mid_yrs) — no parsing
# needed for those anymore. key_skills is still free text, so it still
# needs splitting + the junk-token filter below.

def split_multi(value):
    """'Python, SQL, Java' -> ['Python', 'SQL', 'Java']
    Drops junk tokens (e.g. a trailing '...' left over from truncated
    free-text lists in key_skills — a real messy-data issue in this
    dataset, worth a line in the report's Data Exploration section)."""
    if pd.isna(value):
        return []
    tokens = [x.strip() for x in re.split(r"[,/|]", str(value)) if x.strip()]
    return [t for t in tokens if re.search(r"[A-Za-z]{2,}", t)]


# ----------------------------------------------------------------------
# 2. LOAD
# ----------------------------------------------------------------------
ds = pd.read_csv(DS_PATH)
aj = pd.read_csv(AJ_PATH)

# Drop spam/fake postings before any analysis — per cleaning_log.md,
# Person 1 flagged these but deliberately didn't delete them from the
# file, so we exclude them here instead.
n_before = len(aj)
aj = aj[aj["is_spam_posting"] == 0].copy()
print(f"Analytics Jobs: excluded {n_before - len(aj)} flagged spam postings "
      f"({len(aj)} rows remain).")

# Use the already-cleaned numeric columns directly
ds["avg_salary_lakhs"] = ds["avg_salary_lpa"]
ds["min_experience_num"] = ds["min_experience"]

aj["salary_lakhs"] = aj["sal_mid_lpa"]
aj["experience_years"] = aj["exp_mid_yrs"]

print(f"DataScience Jobs: {len(ds)} rows loaded, "
      f"{ds['avg_salary_lakhs'].isna().sum()} missing salary values.")
print(f"Analytics Jobs:   {len(aj)} rows loaded, "
      f"{aj['salary_lakhs'].isna().sum()} missing salary values.")


# ----------------------------------------------------------------------
# 3. CHART 1 — Top 15 companies by average salary (DataScience Jobs)
# ----------------------------------------------------------------------
top_companies = (
    ds.dropna(subset=["avg_salary_lakhs"])
    .groupby("company_name")["avg_salary_lakhs"]
    .mean()
    .sort_values(ascending=False)
    .head(15)
)

fig, axp = plt.subplots(figsize=(8, 6))
axp.barh(top_companies.index[::-1], top_companies.values[::-1], color=BLUE, height=0.6)
axp.set_xlabel("Average salary (Lakhs INR)")
axp.set_title("Top 15 companies by average data science salary", fontsize=12, weight="bold")
axp.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/01_top_companies_by_salary.png", dpi=150)
plt.close()

print(f"\n[Chart 1] Highest-paying company (avg): "
      f"{top_companies.index[0]} (~{top_companies.values[0]:.1f}L)")


# ----------------------------------------------------------------------
# 4. CHART 2 — Top 20 in-demand skills (Analytics Jobs, key_skills column)
# ----------------------------------------------------------------------
all_skills = aj["key_skills"].dropna().apply(split_multi).explode()
top_skills = all_skills.value_counts().head(20)

fig, axp = plt.subplots(figsize=(8, 7))
axp.barh(top_skills.index[::-1], top_skills.values[::-1], color=BLUE, height=0.6)
axp.set_xlabel("Number of job postings mentioning this skill")
axp.set_title("Top 20 in-demand skills", fontsize=12, weight="bold")
axp.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/02_top_skills.png", dpi=150)
plt.close()

print(f"[Chart 2] Most in-demand skill: "
      f"{top_skills.index[0]} ({top_skills.values[0]} postings)")


# ----------------------------------------------------------------------
# 5. CHART 3 — Top 15 locations by number of postings (Analytics Jobs)
# ----------------------------------------------------------------------
# primary_city is already deduped/standardised by Person 1's cleaning
# (e.g. Gurugram -> Gurgaon) — one city per row, no splitting needed.
top_locations = aj["primary_city"].dropna().value_counts().head(15)

fig, axp = plt.subplots(figsize=(8, 6))
axp.barh(top_locations.index[::-1], top_locations.values[::-1], color=BLUE, height=0.6)
axp.set_xlabel("Number of job postings")
axp.set_title("Top 15 locations by job postings", fontsize=12, weight="bold")
axp.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/03_top_locations.png", dpi=150)
plt.close()

print(f"[Chart 3] Location with most postings: "
      f"{top_locations.index[0]} ({top_locations.values[0]} postings)")


# ----------------------------------------------------------------------
# 6. CHART 4 — Top 15 designations by number of postings (Analytics Jobs)
# ----------------------------------------------------------------------
top_designations = aj["job_desig"].dropna().value_counts().head(15)

fig, axp = plt.subplots(figsize=(8, 6))
axp.barh(top_designations.index[::-1], top_designations.values[::-1], color=BLUE, height=0.6)
axp.set_xlabel("Number of job postings")
axp.set_title("Top 15 designations by job postings", fontsize=12, weight="bold")
axp.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/04_top_designations.png", dpi=150)
plt.close()

print(f"[Chart 4] Most common designation: "
      f"{top_designations.index[0]} ({top_designations.values[0]} postings)")


# ----------------------------------------------------------------------
# 7. CHART 5 — Experience vs Salary relationship (Analytics Jobs)
# ----------------------------------------------------------------------
scatter_df = aj.dropna(subset=["experience_years", "salary_lakhs"])

fig, axp = plt.subplots(figsize=(8, 6))
axp.scatter(scatter_df["experience_years"], scatter_df["salary_lakhs"],
            color=BLUE, alpha=0.35, s=25, edgecolors="none")
axp.set_xlabel("Experience (years, midpoint of range)")
axp.set_ylabel("Salary (Lakhs INR, midpoint of bucket)")
axp.set_title("Experience vs Salary", fontsize=12, weight="bold")
axp.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/05_experience_vs_salary.png", dpi=150)
plt.close()

corr = scatter_df["experience_years"].corr(scatter_df["salary_lakhs"])
print(f"[Chart 5] Correlation between experience and salary: {corr:.2f}")

print(f"\nAll 5 charts saved in ./{OUT_DIR}/ — ready to drop into the report.")
