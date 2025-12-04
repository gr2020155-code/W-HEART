from w_heart import w_heart

print("\n================= W-HEART v1.6 TEST RUNNER =================\n")

tests = {
    "Healthy young":                 dict(age=28, male=True, smoking=0, bmi=22.4, sbp=118, hrv_now=78, hrv_30d_ago=72, hrv_sd7d=45, ldl=110, hdl=62, tg=90, crp=0.5),
    "Middle age stable":            dict(age=47, male=False, smoking=0, bmi=25.1, sbp=128, hrv_now=55, hrv_30d_ago=58, hrv_sd7d=38, ldl=135, hdl=55, tg=120, crp=2.0),
    "Pre-hypertensive tension":     dict(age=52, male=True, smoking=1, bmi=29.5, sbp=148, hrv_now=40, hrv_30d_ago=50, hrv_sd7d=32, ldl=160, hdl=42, tg=180, crp=4.0),
    "High LDL risk":                dict(age=61, male=True, smoking=0, bmi=27.8, sbp=136, hrv_now=48, hrv_30d_ago=54, hrv_sd7d=44, ldl=240, hdl=53, tg=130, crp=1.8),
    "Inflammation fire":            dict(age=55, male=False, smoking=0, bmi=26.2, sbp=132, hrv_now=50, hrv_30d_ago=52, hrv_sd7d=46, ldl=155, hdl=48, tg=170, crp=18),
    "Autonomic chaos (HRV↓)":       dict(age=45, male=True, smoking=2, bmi=31.4, sbp=142, hrv_now=12, hrv_30d_ago=45, hrv_sd7d=20, ldl=150, hdl=38, tg=200, crp=7),
    "Autonomic chaos (HRV↑)":       dict(age=33, male=False, smoking=0, bmi=23.0, sbp=118, hrv_now=190, hrv_30d_ago=60, hrv_sd7d=155, ldl=120, hdl=65, tg=90, crp=0.8),
}

for name, params in tests.items():
    result = w_heart(**params)
    print(f"{name}:")
    print("  risk:", result["risk"])
    print("  phase:", result["phase"])
    print("  N_vasc:", result["N_vasc"], "/", result["N_crit"])
    print("-------------------------------------------------------")

print("\n============================================================\n")
