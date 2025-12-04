# W-HEART  
**PAN-based cardiovascular resilience and system stability engine (v1.6 core release)**  
*Non-medical algorithm. No heuristics. No statistical fitting. Pure systemic logic.*

---

##  Abstract
W-HEART is a **system-level cardiovascular stability model** based on PAN-logic principles.  
It does **not** use medical heuristics, epidemiological assumptions, or statistical training.  
The engine evaluates **vascular informational load (N_vasc)** and compares it against  
a **critical threshold of systemic collapse (N_crit)** to determine:

- stability vs destabilization
- proximity to phase transition
- irreversible failure triggers
- risk trajectory and evolution direction

This is **not a diagnostic tool**, but a **logical stability model of a biological system.**

---

##  Core Idea

Every biological system has:
1. **Parameters increasing internal contradiction (stress load)**  
2. **A critical threshold of structural coherence (N_crit)**  
3. **A phase point where control breaks → irreversible trajectory (chaos branch)**  

W-HEART quantifies these layers **without axioms**.  
No "normal/healthy ranges" — only *contradiction vs stability logic*.

---

## 🔷 Input Parameters

| Parameter | Type | Meaning |
|---|---|---|
| `age` | int | years |
| `male` | bool | sex flag |
| `smoking` | 0–2 | 0 none / 1 former / 2 active |
| `bmi` | float | mass/height² |
| `sbp` | int | systolic pressure |
| `diabetes` | bool | T2D indicator |
| `family` | bool | inherited risk |
| `hrv_now` | int | RMSSD current (ms) |
| `hrv_30d_ago` | int | baseline month ago |
| `hrv_sd7d` | int | SDNN-7d variability window |
| `ldl` | mg/dl | Low density lipoproteins |
| `hdl` | mg/dl | High density lipoproteins |
| `tg` | mg/dl | Triglycerides |
| `crp` | mg/l | hs-CRP inflammation marker |

---

##  Risk Output

```python
{
  "W-Risk": "0.923441",
  "Phase": "System Stable / Approaching threshold",
  "N_vasc": 5472,
  "N_crit": 8192,
  "Version": "W-HEART v1.6"
}
| Risk State  | Meaning                                            |
| ----------- | -------------------------------------------------- |
| **<0.7**    | stable system, low contradiction                   |
| **0.7–0.9** | structural tension rising                          |
| **0.9–1.0** | near critical phase boundary                       |
| **=1.0**    | irreversible trajectory or single-trigger collapse |
A single extreme parameter (SBP≥180, HRV≤15, CRP≥15 etc.) may produce instant criticality, regardless of the rest.
| Feature                                 | ✓            |
| --------------------------------------- | ------------ |
| Core PAN-engine                         | ✓            |
| Lipid & inflammation layer              | ✓            |
| Critical single-trigger collapse logic  | ✓            |
| Dataset test integration (CAIR/MIT-BIH) | ⧗ next       |
| App Interface (W-HEART UI)              | ⧗ planned    |
| Arweave permanent bundle                | ⧗ next stage |
License

MIT License
(Usage in medical decision-making without clinical validation is prohibited.)

W-HEART is a theoretical resilience engine, not medical advice.

Roadmap

v1.7 — add trajectory predictor (HRV target, delay gain)

W-HEART App (mobile/web)

Dataset validation suite (CAIR-CVD, MIT-BIH)

Arweave permanent archive + DOI

Developed within W-Structure, logic-first universe model.
No axioms. Zero heuristics. 100% contradiction-free.


