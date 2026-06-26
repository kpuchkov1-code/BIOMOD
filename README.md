# BIOMOD dry-lab — pre-wet-lab deliverables

In-silico work for the Fujii & Rondelez (2013, *ACS Nano*) DNA predator–prey
oscillator, ahead of crowding experiments. Everything here runs on a laptop —
**no wet lab required** — and is the Step 1–4 work dry lab can finish before the
bench starts.

## What's here

| File | Dry-lab step | What it does |
|------|--------------|--------------|
| `fujii_pp_model.py` | **1. Reproduce** | The **paper-exact** two-variable model (SI eqs 3–4) with the SI's **measured** parameters (Table S5, PP1); produces the time-series, phase-portrait, and template-bifurcation figures. |
| `stability_analysis.py` | **1. Reproduce (proof)** | Numerical fixed-point + Jacobian/eigenvalue check that the oscillation is real — independent of the integrator. |
| `sensitivity_analysis.py` | **2. Sensitivity** | One-at-a-time parameter sweeps (which knobs set period/amplitude) + phase-plane/nullcline picture. |
| `sequence_check.py` | **4. Sequences** | Biophysical sanity checks on prey/predator/template; optional NUPACK equilibrium analysis. |
| `crowding_map.md` | **3. Crowding hooks** | Where molecular crowding enters the model — which parameters, which direction. (Bridge to the *next* phase.) |

## ✅ Status: quantitatively reproduces the paper

The model now uses the SI's exact equations and **measured kinetic parameters**
(no placeholders). It is validated three independent ways:

1. **Nondimensional self-check** — the `β, λ, δ, G₀, t_c` computed from the
   Table S5 rate constants match **SI Table S3** (PP1) to within a few percent
   (β=0.086 vs 0.087, λ=4.47 vs 4.5, δ=0.392 vs 0.39, G₀=52.7 vs 53 nM,
   t_c=2.56 vs 2.6 min). This proves the implementation is faithful.
2. **Dynamics** — at standard conditions with template G1 = 140 nM the system
   settles into a sustained relaxation limit cycle (predator ≈ 0.5 → 173 nM,
   period ≈ 92 min).
3. **Template bifurcation** — sweeping G1 reproduces the paper's onset of
   oscillations (oscillates for G1 ≈ 100–170 nM here; paper ≈ 80–200 nM,
   Fig S11): a fixed point at low template, oscillations at intermediate, and
   damping back to a fixed point at high template.
4. **Analytic** (`stability_analysis.py`) — the interior fixed point
   (N* ≈ 4.4, P* ≈ 67.8 nM) is an **unstable spiral** (eigenvalues
   0.0024 ± 0.176i), so Poincaré–Bendixson guarantees a surrounding limit cycle.

See `fujii_reproduction.png`, `bifurcation_G.png`, `sensitivity.png`,
`phase_plane.png`.

## The model (SI eqs 3–4, exactly)

```
dN/dt = k1·pol·G·N/(1 + b·G·N)   -  k2·pol·N·P  -  rec·kN·N/(1 + P/Km,P)
        \___ prey growth ______/    \_predation_/   \__ prey decay ______/

dP/dt = k2·pol·N·P  -  rec·kP·P/(1 + P/Km,P)
        \_predation_/   \_ predator decay ___/
```

PP1 standard-conditions parameters (SI Table S5, optimized, rec = 32.5 nM):
`k1 = 2.0e-3`, `b = 4.8e-5`, `k2 = 3.1e-3`, `kN = 2.1e-2`, `kP = 4.7e-3`,
`Km,P = 34 nM`; enzymes `pol (Bst) = 3.7 nM`, `rec (ttRecJ) = 32.5 nM`;
control knob `G (template) = 140 nM`.

### ⚠️ This corrected an earlier mechanistic error

The first version of this file used a generic Rosenzweig–MacArthur form
(logistic prey growth + **Holling-II saturating predation** + linear death).
That oscillated, but for the **wrong reason**. The real Fujii system has:

- **linear** (mass-action) predation `k2·pol·N·P`, *not* a saturating one;
- a **saturable Michaelis–Menten degradation** term — the oscillation engine.

The paper proves (SI Fig S3 vs S5) that with first-order/linear degradation the
system can only damp to a fixed point; it is the **saturable exonuclease**
(ttRecJ as a limited catalytic resource the predator can swamp) that creates the
sustained limit cycle. Don't reintroduce the Holling/logistic form.

## Interactive explorers (open in a browser, no install)

Two self-contained HTML pages (live ODE solving + plotting in JavaScript, linked by
tabs at the top):

- `model_explorer.html` — **dilute** PP1 oscillator. Sliders for every knob
  (template, enzymes, rate constants), live time-series + phase portrait, a
  nondimensional readout that matches SI Table S3, and a plain-language explanation.
- `crowding_explorer.html` — **crowded** version (the BIOMOD novelty). Adds a master
  crowder-concentration `C` and tunable effect-strength sliders. Crowding re-scales
  the rate constants via excluded-volume (binding up: `k1,k2,b` up, `Km,P` down),
  viscosity (diffusion down: `k1,k2` down), and Pol/Exo turnover shifts. The key
  output is a **C-sweep prediction plot** (amplitude + period vs `C`) that flags when
  crowding crosses the Hopf boundary and switches the oscillation on/off. Effect
  magnitudes are clearly labelled as hypotheses to be fitted to data, not measured
  values.

## How to run the Python deliverables

```powershell
py fujii_pp_model.py        # self-check + reproduction + template bifurcation
py stability_analysis.py    # analytic unstable-spiral proof
py sensitivity_analysis.py  # -> sensitivity.png, phase_plane.png
py sequence_check.py        # prints biophysics report
```

Dependencies: `numpy`, `scipy`, `matplotlib` (installed). NUPACK is optional and
only used by Layer 2 of `sequence_check.py`.

## Still open

1. **Sequences** — `sequence_check.py` still needs the predator `P1` and
   template `G1` strands filled from SI Table S1
   (`P1 = CATTCGG-CCGAATG`, `G1 = C*G*G*CCGAATG-CGGCCGAATG`).
2. **Crowding layer** — not yet coded. `crowding_map.md` is the plan: make the
   affected rate constants functions of crowder concentration `C` and predict
   how period/amplitude (and the bifurcation onset) move.

## Two model levels (don't conflate them)

- **Reduced 2-variable model** (this code) — for *dynamics*: does it oscillate,
  what's the period, how do parameters move it. This is what reproduces the
  paper's oscillation figures and what crowding will perturb.
- **Full mechanistic reactome** (teammate's diagram / SI Fig S1) — every species
  and conformational state, Pol/Nic/Exo complexes, fluorescence-interfering
  species. Heavier; the SI's Section S3 derivation shows how it collapses to the
  2-variable model above.

## Mechanistic mapping (reduced model ↔ reactome modules)

| Reduced-model term | Reactome module | Enzyme |
|--------------------|-----------------|--------|
| prey growth `k1·pol·G·N/(1+b·G·N)` | PREY GROWTH (green); saturating on template/Nic | Pol + Nic on G |
| predation `k2·pol·N·P` | PREDATION (red); linear mass action | Pol on N·P |
| decay `rec·kN·N/(1+P/Km,P)`, `rec·kP·P/(1+P/Km,P)` | DEATH (grey); saturable, shared exonuclease | Exo (ttRecJ) |
| — | FLUORESCENCE INTERFERENCE (purple) | reporter model only |
