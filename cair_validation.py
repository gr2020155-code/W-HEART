import pandas as pd
from w_heart import w_heart

# === CONFIGURATION ===
CSV_PATH = "CVD Dataset.csv"   
COLS = {
    "age":      "Age",
    "sex":      "Sex",
    "smoking":  "Smoking Status",
    "bmi":      "BMI",
    "sbp":      "Systolic BP",
    "diabetes": "Diabetes Status",
    "family":   "Family History of CVD",
    "ldl":      "Estimated LDL (mg/dL)",
    "hdl":      "HDL (mg/dL)",
    "tg":       "Total Cholesterol (mg/dL)",   # TG нет, берём общий холестерин
    "crp":      None,                          # нет в датасете — отключаем
    "label":    "CVD Risk Level"               # можно заменить на Score для теста
}
print("=== COLS mapping used ===")
print(COLS)


def map_row(row):
    """Преобразуем строку CAIR в параметры W-HEART без HRV (HRV отключён)."""

    # пол
    sex_val = row[COLS["sex"]]
    if isinstance(sex_val, str):
        male = sex_val.upper().startswith("M")
    else:
        male = bool(sex_val)

    # курение
    smk_raw = row[COLS["smoking"]]
    # приведение к 0/1/2 без подгонок
    if smk_raw in (0, "0", "None", "No"):
        smoking = 0
    elif smk_raw in (1, "1", "Former"):
        smoking = 1
    else:
        smoking = 2

    params = dict(
        age       = int(row[COLS["age"]]),
        male      = male,
        smoking   = smoking,
        bmi       = float(row[COLS["bmi"]]),
        sbp       = int(row[COLS["sbp"]]),
        diabetes  = bool(row[COLS["diabetes"]]),
        family    = bool(row[COLS["family"]]),
        hrv_now       = 50,   # HRV-слой отключён (нет данных)
        hrv_30d_ago   = 50,
        hrv_sd7d      = 0,
        ldl       = float(row[COLS["ldl"]]) if pd.notna(row[COLS["ldl"]]) else None,
        hdl       = float(row[COLS["hdl"]]) if pd.notna(row[COLS["hdl"]]) else None,
        tg        = float(row[COLS["tg"]])  if pd.notna(row[COLS["tg"]])  else None,
        crp       = float(row[COLS["crp"]]) if pd.notna(row[COLS["crp"]]) else None,
    )
    return params

def main():
    print("\n=== W-HEART v1.6 — CAIR-CVD validation (no HRV layer) ===\n")
    df = pd.read_csv(CSV_PATH)

    print("Columns in dataset:")
    print(list(df.columns))
    print("\nRows:", len(df))

    # если в наборе есть целевая метка
    has_label = COLS["label"] in df.columns

    risks = []
    labels = []

    for _, row in df.iterrows():
        params = map_row(row)
        res = w_heart(**params)
        risks.append(res["risk"])
        if has_label:
            labels.append(int(row[COLS["label"]]))

    df["W_risk"] = risks

    print("\nRisk summary:")
    print(df["W_risk"].describe())

    if has_label:
        from sklearn.metrics import roc_auc_score
        auc = roc_auc_score(labels, risks)
        print(f"\nAUC vs label ({COLS['label']}): {auc:.4f}")
    else:
        print("\nNo label column found, AUC not computed.")

    # сохраним файл с рисками рядом
    out_name = "cair_with_wheart_risk.csv"
    df.to_csv(out_name, index=False)
    print(f"\nSaved: {out_name}")

if __name__ == "__main__":
    main()
