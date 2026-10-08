import sys, json
import pandas as pd

base = sys.argv[1]

files = {
    "ds_jobs": f"{base}/DataScience Jobs.csv",
    "an_jobs": f"{base}/Analytics Jobs.csv",
    "jds": f"{base}/JDS Skill Traits.xlsx",
    "sds": f"{base}/SDS Personality Traits.xlsx",
}

for name, path in files.items():
    print("="*100)
    print(name, path)
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    print(df.dtypes)
    print("--- head ---")
    print(df.head(5).to_string())
    print("--- null counts ---")
    print(df.isnull().sum())
    print("--- describe (numeric) ---")
    print(df.describe(include='all').to_string())
