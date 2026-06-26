# Crowding → model parameter map (Step 3 bridge)

This is the hand-off from "reproduce Fujii" to "add our novelty." It does **not**
change the equation *structure* — it makes specific rate constants functions of
crowder concentration `C` (PEG 8000 or Ficoll 400).

The point of doing Step 2 (sensitivity) first: only the parameters the
oscillation is *sensitive* to are worth modelling carefully. Cross-reference the
sensitivity index from `sensitivity_analysis.py` against this table.

## Physical effects and which parameter they hit

| Crowding effect | Reduced-model parameter | Direction | Mechanistic note |
|---|---|---|---|
| **Excluded volume** raises effective concentrations / activities | `a` (predation/attack), prey replication `r` | ↑ rates | mass-action speed-up; depletion attraction favours complex formation |
| **Increased viscosity** slows diffusion | diffusion-limited association → caps `a`, `r` | ↓ rates | competes with the excluded-volume speed-up — net sign is **not obvious a priori** |
| **Enzyme kinetics shift** (Pol, Nic, Exo) | `r`, `h` (handling), `m` (Exo death) | either | crowding can change kcat and KM; ttRecJ activity under crowding is the key unknown |
| **Duplex stabilisation** (effective Tm ↑) | binding steps feeding `r`, `a`; off-target risk | ↑ stability | favours productive hybridisation but also spurious products |

## How to implement (minimal, honest)

Replace each affected constant with a scaling factor:

```
r(C)   = r0   * f_r(C)
a(C)   = a0   * f_a(C)
m(C)   = m0   * f_m(C)
```

Start with the simplest defensible `f(C)`:
- **Empirical**: linear or exponential fit `f(C) = 1 + k·C` / `exp(k·C)` to the
  crowding literature for that specific enzyme/step.
- **First-principles option**: scaled-particle / excluded-volume theory for the
  association steps; Stokes–Einstein `D ∝ 1/η(C)` for the diffusion cap.

Then re-run `fujii_pp_model.py` across a `C` grid and predict how **period** and
**amplitude** move. That prediction is the falsifiable hypothesis wet lab tests.

## The interesting science (why this isn't a foregone conclusion)

Excluded volume **speeds reactions up** while viscosity **slows diffusion down**.
These push the oscillation period in opposite directions. The model's job is to
predict which wins in the PP1 system — and whether crowding can push a
non-oscillating parameter set *across the Hopf bifurcation* into oscillation (or
vice versa). That bifurcation-shift framing is the strongest version of the
result.

## Open inputs needed before this step is quantitative
- Crowding-dependence data for **ttRecJ**, **Bst pol**, **Nb.BsmI** (literature
  search — likely sparse; may need our own wet-lab calibration runs).
- η(C) for PEG 8000 / Ficoll 400 at 46.5 °C.
- ΔTm vs `C` for the PP1 duplexes (NUPACK gives the dilute baseline; crowding
  correction from literature).
