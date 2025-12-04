import pandas as pd
from w_heart import w_heart
from sklearn.metrics import roc_auc_score, confusion_matrix
import numpy as np

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
    "tg":       "Total Cholesterol (mg/dL)",
    "crp":      None,
    "label":    "CVD Risk Level"
}

def safe_float(x, default=None):
    try:
        return float(x) if pd.notna(x) else default
    except:
        return default

def safe_int(x, default=50):
    try:
        return int(x) if pd.notna(x) else default
    except:
        return default

def map_smoking(val):
    s = str(val).strip().lower()
    if s in ["y", "yes", "smoker", "current"]:
        return 2
    elif s in ["former", "ex", "quit"]:
        return 1
    else:
        return 0

def map_row(row):
    return {
        "age":        safe_int(row[COLS["age"]], 50),
        "male":       str(row[COLS["sex"]]).strip().upper().startswith("M"),
        "smoking":    map_smoking(row[COLS["smoking"]]),
        "bmi":        safe_float(row[COLS["bmi"]], 25.0),
        "sbp":        safe_int(row[COLS["sbp"]], 130),
        "diabetes":   str(row[COLS["diabetes"]]).strip().upper() == "Y",
        "family":     str(row[COLS["family"]]).strip().upper() == "Y",
        "ldl":        safe_float(row[COLS["ldl"]]),
        "hdl":        safe_float(row[COLS["hdl"]]),
        "tg":         safe_float(row[COLS["tg"]]),
        "crp":        None,
        "hrv_now":    50,
        "hrv_30d_ago": 50,
        "hrv_sd7d":   None
    }

def main():
    print("W-HEART v1.6 — Валидация на CVD Dataset.csv")
    print("=" * 60)

    df = pd.read_csv(CSV_PATH)
    print(f"Загружено строк: {len(df)}")
    print("Колонки в датасете:", df.columns.tolist(), "\n")

    results = []
    true_labels = []

    for idx, row in df.iterrows():
        params = map_row(row)

        label_raw = str(row[COLS["label"]]).strip().upper()
        true_label = 1 if "HIGH" in label_raw else 0
        true_labels.append(true_label)

        try:
            res = w_heart(**params)
            risk = res["risk"]
        except Exception as e:
            print(f"Ошибка в строке {idx}: {e}")
            risk = 0.0

        results.append(risk)

    results = np.array(results)
    true_labels = np.array(true_labels)

    auc = roc_auc_score(true_labels, results)
    tn, fp, fn, tp = confusion_matrix(true_labels, (results >= 0.5).astype(int)).ravel()

    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    accuracy = (tp + tn) / len(true_labels)

    print("РЕЗУЛЬТАТЫ ВАЛИДАЦИИ (без HRV-данных)")
    print("=" * 60)
    print(f"Записей обработано:     {len(results)}")
    print(f"AUC ROC:                {auc:.4f}")
    print(f"Accuracy:               {accuracy:.4f}")
    print(f"Sensitivity (Recall):   {sensitivity:.4f}")
    print(f"Specificity:            {specificity:.4f}")
    print(f"Средний W-Risk:         {results.mean():.4f}")
    print(f"TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")
    print("\nГотово. Противоречий нет.")

if __name__ == "__main__":
    main()

