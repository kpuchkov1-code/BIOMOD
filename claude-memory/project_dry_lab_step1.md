---
name: project-dry-lab-step1
description: "Dry-lab Step-1 in-silico reproduction of the Fujii predator-prey oscillator — runnable Python at C:\\Users\\KPuch\\biomod-dry-lab; now PAPER-EXACT (SI eqs 3-4, measured params), validated against SI Table S3"
metadata: 
  node_type: memory
  type: project
  originSessionId: 74e27cb6-4a28-4c0c-bfa1-be2c74bb394e
---

Built the dry-lab "Step 1" deliverables for the BIOMOD predator-prey project (see [[project-flux-pivot]]) at **`C:\Users\KPuch\biomod-dry-lab\`**. Runs on `py` (Python 3.14, numpy/scipy/matplotlib). Files: `fujii_pp_model.py` (model + solver + figures), `stability_analysis.py` (Jacobian/eigenvalue proof), `sensitivity_analysis.py` (sweeps + phase plane), `sequence_check.py` (biophysics + optional NUPACK), `crowding_map.md`, `README.md`.

**2026-06-22 update — SI obtained and model rebuilt to be paper-exact.** The Fujii SI PDF is at `C:\Users\KPuch\Downloads\nn3043572_si_001.pdf` (and the article is paywalled at pubs.acs.org/doi/10.1021/nn3043572 — ACS blocks WebFetch with 403). Key SI sections: S3 = the two-variable model derivation (eqs 3-4 dimensional, 5-6 nondimensional); S4 = measured kinetic params (Table S5); Table S1 = sequences; Table S3 = nondimensional params.

**Corrected a mechanistic error:** the original code used a generic Rosenzweig-MacArthur form (logistic growth + **Holling-II saturating predation** + linear death) with placeholder params — it oscillated for the WRONG reason. The real Fujii model (now implemented) has **linear mass-action predation** `k2*pol*N*P` and a **saturable Michaelis-Menten exonuclease degradation** `rec*kP*P/(1+P/Km,P)` — and it is that saturable decay (not predation saturation) that drives the limit cycle. Paper proves this in SI Fig S3 (linear decay → only damped) vs S5 (saturable decay → sustained cycle).

**PP1 standard-conditions params (SI Table S5, optimized, rec=32.5nM):** k1=2.0e-3, b=4.8e-5, k2=3.1e-3, kN=2.1e-2, kP=4.7e-3, Km,P=34nM; pol(Bst)=3.7nM, rec(ttRecJ)=32.5nM; control knob G(template), osc window G1≈80-200nM. **Sequences filled (SI Table S1):** N1=CATTCGGCCG, P1=CATTCGGCCGAATG (14nt palindrome), G1=CGGCCGAATGCGGCCGAATG (3x 5' phosphorothioate + 3' phos/Dy530).

**Status: quantitatively reproduces the paper.** Validated 4 ways: (1) nondimensional self-check matches SI Table S3 (β=0.086 vs 0.087, λ=4.47 vs 4.5, δ=0.392 vs 0.39, G0=52.7 vs 53, tc=2.56 vs 2.6); (2) oscillates at G1=140nM (predator ~0.5-173nM, period ~92min); (3) template-bifurcation sweep reproduces onset (osc for G1≈100-170nM vs paper ~80-200); (4) interior fixed point N*≈4.4,P*≈67.8 is unstable spiral (eig 0.0024±0.176i). Solver: LSODA, rtol=1e-9, atol=1e-12, max_step=2.0.

**Interactive explorers (2026-06-22):** two self-contained browser pages in the same folder, linked by tabs. `model_explorer.html` = dilute PP1 (live JS ODE solver + sliders + time-series/phase plots + nondimensional readout matching Table S3). `crowding_explorer.html` = the crowding novelty: master crowder `C` (% w/v) plus tunable effect-strength sliders, rate constants re-scaled by excluded volume (binding up: k1,k2,b up, KmP down), viscosity (diffusion down: k1,k2 down), and Pol/Exo turnover; headline output is a C-sweep plot (amplitude+period vs C) that flags Hopf crossings (on/off). Verified vs the Python model: C=0 recovers baseline; with PEG-like defaults the oscillation amplitude shrinks and dies out by C~25% (crowding switches it OFF) — a clean falsifiable prediction. Effect magnitudes are labelled HYPOTHESES, to be fitted to crowding literature / wet-lab enzyme-in-crowder calibration.

**Next task:** replace the crowding effect-strength guesses with literature/calibrated values (esp. ttRecJ-in-crowder, the key lever); optionally port the crowding layer into the Python model for publication-quality figures.

Related: [[project-flux-pivot]], [[project-fujii-reactome]], [[user-role]]
