import pandas as pd
from w_heart import w_heart_v1_6

CSV_PATH = "CVD Dataset.csv"

COLS = {
    "age":      "Age",
    "sex":      "Sex",
    "smoking":  "Smoking Status",         # <-- единственно верная колонка
    "bmi":      "BMI",
    "sbp":      "Systolic BP",
    "diabetes": "Diabetes Status",
    "family":   "Family History of CVD",
    "ldl":      "Estimated LDL (mg/dL)",
    "hdl":      "HDL (mg/dL)",
    "tg":       "Total Cholesterol (mg/dL)",   # TG нет, используем общий холестерин
    "crp":      None,
    "label":    "CVD Risk Level"
}

print("=== COLS mapping used ===")
print(COLS)

def map_row(row):
    # smoking → numeric 0/1/2
    smk_raw = str(row[COLS["smoking"]]).lower()
    if "never" in smk_raw or smk_raw == "0": smoking = 0
    elif "former" in smk_raw or smk_raw == "1": smoking = 1
    else: smoking = 2

    return {
        "age": int(row[COLS["age"]]),
        "male": True if row[COLS["sex"]] in ["M", "Male", 1] else False,
        "smoking": smoking,
        "bmi": float(row[COLS["bmi"]]),
        "sbp": int(row[COLS["sbp"]]),
        "diabetes": True if row[COLS["diabetes"]] in [1, "Yes"] else False,
        "family": True if row[COLS["family"]] in [1, "Yes"] else False,
        "ldl": float(row[COLS["ldl"]]) if not pd.isna(row[COLS["ldl"]]) else None,
        "hdl": float(row[COLS["hdl"]]),
        "tg": float(row[COLS["tg"]]),
        "crp": None
    }

def main():
    df = pd.read_csv(CSV_PATH)
    print("\n=== W-HEART v1.6 — CAIR-CVD validation (no HRV layer) ===\n")

    print("Columns in dataset:")
    print(df.columns.tolist(), "\n")

    risks = []
    for _, row in df.iterrows():
        p = map_row(row)
        res = w_heart_v1_6(**p)
        risks.append(res["risk_value"])

    print(f"Processed records: {len(risks)}")
    print(f"Mean risk: {sum(risks)/len(risks):.4f}")
    print("Validation complete.")

if __name__ == "__main__":
    main()
