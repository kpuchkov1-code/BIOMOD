# Crowding layer — mechanistic model (dry-lab Step 3)

A bottom-up, mechanistic model of how macromolecular crowding (PEG 8000 vs
Ficoll 400) reshapes the Fujii–Rondelez DNA predator–prey oscillator. Crowding
acts on every **elementary** step through one shared set of physical primitives
(scaled-particle excluded volume, Hołyst scale-dependent viscosity, enzyme-class
catalytic shifts) — it is **not** a per-constant factor fit.

## Files
- `crowded_mechanistic.py` — the model. Explicit 7-species reaction network
  (free N, P, template G + the four complexes N·G, N·P, N·Exo, P·Exo) with
  enzyme conservation. Reduces under QSSA to the validated SI eqs 3–4. Run it
  to regenerate the two figures.
- `generate_mechanistic_report.py` — builds the Word write-up with native,
  editable equations (LaTeX → MathML → OMML via Office's `MML2OMML.XSL`).
- `Crowded_PredatorPrey_Mechanistic_Model.docx` — the explainer (12 sections).
- `mechanistic_predictions.png`, `mechanistic_timeseries.png` — figures.

## Interactive version
`../site/crowding_explorer.html` runs the **same 7-species network** live in the
browser (de-stiffened binding for in-browser RK4; validated to reproduce the
LSODA reference period of ~90 min). Sliders expose the physical channels
(crowder %, radius, excluded-volume strength, viscosity, exonuclease inhibition,
polymerase boost) so you can see what each is doing.

## Headline prediction
Crowding **shortens** the period and collapses amplitude. **PEG 8000** crosses a
Hopf bifurcation and abolishes oscillation near ~10–12% w/v; **Ficoll 400**
(compact, larger R_c → less excluded volume per φ) keeps oscillating across the
whole range. That PEG-vs-Ficoll divergence at equal volume fraction is the
falsifiable, novel result.

## Caveats
All coefficients are literature-anchored, tunable hypotheses for wet-lab
calibration. All Ficoll-400 numbers are extrapolations. The exonuclease anchor
is an Exo I number — **ttRecJ activity vs crowder is the single highest-value
measurement** to calibrate the Hopf concentration.
