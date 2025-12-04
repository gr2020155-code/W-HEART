import math

def w_heart(
    age: int, male: bool, smoking: int, bmi: float, sbp: int = 130,
    diabetes: bool = False, family: bool = False,
    hrv_now: int = 50, hrv_30d_ago: int = 50, hrv_sd7d: int = 0,
    ldl: float = None, hdl: float = None, tg: float = None,
    crp: float = None
) -> dict:
    """
    W-HEART v1.6 — systemic cardiovascular stability engine based on PAN-logic.
    No heuristics. No medical assumptions. No statistical training.
    """

    # --- Cumulative informational load (N_vasc) ---
    N_age = max(0, age - 40) ** 2 * 4
    N_smoke = [0, 304, 784][smoking]
    N_bmi = max(0, int(bmi * 10 - 210)) ** 2 // 16
    N_sbp = max(0, sbp - 115) ** 2 // 25
    N_diabetes = 1024 if diabetes else 0
    N_family = 896 if family else 0
    N_hrv_drop = max(0, hrv_30d_ago - hrv_now) * 32

    # PAN window HRV stability
    N_hrv_inst = 0
    if hrv_sd7d is not None:
        lo, hi = 30, 80
        if hrv_sd7d < lo:
            N_hrv_inst = (lo - hrv_sd7d) ** 2
        elif hrv_sd7d > hi:
            N_hrv_inst = (hrv_sd7d - hi) ** 2

    # Lipids
    N_lipids = 0
    if ldl: N_lipids += max(0, int((ldl - 130) // 10)) * 64
    if hdl: N_lipids += max(0, int((60 - hdl) // 5)) * 96
    if tg and hdl and hdl > 0:
        ratio = tg / hdl
        if ratio > 3.0: N_lipids += 1024
        elif ratio > 2.0: N_lipids += 512

    # Inflammation
    N_crp = 0
    if crp:
        if crp > 10: N_crp = 32
        elif crp > 3: N_crp = 16
        elif crp > 1: N_crp = 8

    # Final cumulative load
    N_vasc = N_age + N_smoke + N_bmi + N_sbp + N_diabetes + N_family + \
             N_hrv_drop + N_hrv_inst + N_lipids + N_crp

    # Critical mass
    N_crit = 8192 if male else 7168

    # --- Single critical parameter collapse ---
    irreversible = False
    critical_trigger = None

    if sbp >= 180 or sbp <= 80:
        N_vasc = max(N_vasc, int(N_crit * 0.90))
        critical_trigger = "SBP collapse"
    elif crp and crp >= 15:
        N_vasc = max(N_vasc, int(N_crit * 0.92))
        critical_trigger = "Inflammation fire"
    elif ldl and ldl >= 220:
        N_vasc = max(N_vasc, int(N_crit * 0.88))
        critical_trigger = "LDL overload"
    elif tg and hdl and hdl > 0 and tg / hdl >= 6.0:
        N_vasc = max(N_vasc, int(N_crit * 0.93))
        critical_trigger = "Endothelial collapse"

    # Chaotic HRV failure (chaos branch)
    if hrv_now <= 15 or hrv_now >= 180 or (hrv_sd7d and hrv_sd7d >= 150):
        irreversible = True
        critical_trigger = "Autonomic chaos"
        N_vasc = N_crit

    # --- Risk / phase result ---
    if irreversible or N_vasc >= N_crit:
        risk = 1.0
        phase = f"Irreversible — {critical_trigger}"
    else:
        dist = N_crit - N_vasc
        risk = (N_crit**4 - dist**4) / N_crit**4
        phase = "Stable system"

    return {
        "risk": round(risk, 6),
        "phase": phase,
        "N_vasc": N_vasc,
        "N_crit": N_crit,
        "version": "v1.6"
    }
