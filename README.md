# JDS / SDS Analysis — Team Grayhat (SAS × CU Hackathon)

Data cleaning, exploratory analysis and modelling of four hackathon datasets:
Analytics Jobs, DataScience Jobs, JDS Skill Traits and SDS Personality Traits.

## Layout

| Path | Contents |
|---|---|
| `Grayhat/SAS Data Problem Statement and Instructions Hackathon/` | Raw datasets as provided (`Analytics Jobs.csv`, `DataScience Jobs.csv`, `JDS Skill Traits.xlsx`, `SDS Personality Traits.xlsx`) and `Data Description Doc.pdf` |
| `clean_data.py` | Cleaning pipeline: reads the 4 raw files, writes 4 cleaned CSVs + `cleaning_log.md` |
| `cleaned/` | Cleaned CSVs, `cleaning_log.md`, EDA script (`eda_jobs_market.py`) and charts, and the dashboard (`build_dashboard.py`, `dashboard_template.html`, built `index.html`) |
| `source_code/` | Analysis and report source: `analyze.py` (EDA + logistic regression / decision tree / random forest), `explore.py`, `diagrams.py`, and the `*.js` files that assemble the report `.docx` |

## Reproduce

Requires Python 3 with `pandas`, `numpy`, `openpyxl`, `matplotlib`, `scikit-learn`.

```bash
# 1. clean the raw data
python clean_data.py "Grayhat/SAS Data Problem Statement and Instructions Hackathon" cleaned

# 2. EDA charts (run inside cleaned/)
cd cleaned && python eda_jobs_market.py

# 3. rebuild the dashboard page (cleaned/index.html)
python build_dashboard.py
```

Open `cleaned/index.html` through a local server so the charts and CSV downloads resolve:

```bash
cd cleaned && python -m http.server 8765
```

## Cleaning summary

| Dataset | Raw rows | Clean rows | Notes |
|---|---|---|---|
| Analytics Jobs | 15,841 | 14,840 | 1,001 duplicates dropped; experience/salary bands parsed to numbers; locations normalised; 121 spam postings flagged |
| DataScience Jobs | 1,602 | 1,602 | salary strings converted to LPA; role families derived; IQR outliers flagged, not removed |
| JDS Skill Traits | 139 | 118 | copy-paste duplicates dropped; id conflicts flagged |
| SDS Personality Traits | 161 | 161 | header spaces fixed; id conflicts and outliers flagged |

Full step-by-step detail: [`cleaned/cleaning_log.md`](cleaned/cleaning_log.md).
