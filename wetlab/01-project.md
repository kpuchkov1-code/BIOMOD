# What the project is

*The circuit, the mechanism, and what the model predicts.*

> Part of the [wet lab documentation set](README.md). The assembled Word version of all of these is `BIOMOD_2026_Project_Brief.docx`.


---

# What we are building

We are rebuilding a DNA predator-prey oscillator, then asking what happens when we crowd the tube with inert polymers.

The oscillator is a chemical clock made of three short DNA strands and three enzymes. Held at a fixed temperature it does not settle to equilibrium. Instead two of the strands rise and fall in waves, roughly every 90 minutes, for 12 hours or more. It is a molecular version of the Lotka-Volterra rabbits-and-foxes model, which is where the names come from.

## The three strands

| Strand | Sequence (5' to 3') | Role |
| --- | --- | --- |
| N, prey | `CATTCGGCCG` | The rabbit. Copied off the template to make more of itself. |
| P, predator | `CATTCGGCCGAATG` | The fox. Uses prey as a template to make more of itself. |
| G, template | `C*G*G*CCGAATGCGGCCGAATG` | The grass. Not consumed. The machine that turns one prey into two. |

The asterisks on G are phosphorothioate linkages, a backbone modification that resists the exonuclease. The template survives while N and P are continually destroyed.

## The three enzymes

- **Bst polymerase, large fragment** extends a strand that has bound to a template, copying it.
- **Nb.BsmI nickase** cuts one strand of a duplex at a specific sequence, releasing the new copy.
- **ttRecJ exonuclease** degrades single-stranded DNA from the 5' end. This is the death arm, and it is what stops the system saturating.

Together these are the PEN toolbox: polymerase, exonuclease, nickase.

## What we add

Everything above reproduces the original experiment. Our contribution is to add inert crowding polymers, PEG 8000 and Ficoll 400. They react with nothing. They take up space, which changes how easily molecules meet, how tightly strands bind, and how fast the enzymes turn over.

The question is whether crowding works as a dial to tune the oscillation, and whether two chemically different crowders at the same volume fraction do the same thing. We predict they do not.

# How the circuit works

Three reactions run at once. Growth makes prey, predation converts prey into predator, and the exonuclease destroys both.

```
   Template G  ──── growth ────►  Prey N  ──── predation ────►  Predator P
  (not consumed)                    │                              │
                                    ▼                              ▼
                                 ttRecJ                          ttRecJ
                                (degraded)                     (degraded)
```

**Growth (N + G gives 2N).** Prey binds its template, Bst extends it into a full duplex, Nb.BsmI nicks the new strand, and the copy comes off. One prey in, two prey out. The template is untouched and does it again.

**Predation (N + P gives 2P).** Predator binds prey. Bst extends the predator using prey as template, so the prey is consumed and a second predator appears. This is the coupling that makes the system oscillate rather than just grow.

**Death (ttRecJ).** The exonuclease degrades free single strands. Crucially it binds predator tightly (Km around 34 nM) and prey weakly (Km around 1000 nM). Because predator saturates the enzyme and prey does not, predator death is roughly constant-rate while prey death stays proportional to concentration. That asymmetry is what closes the limit cycle.

## Reading the output

We cannot see concentrations directly, so we watch two fluorescent channels.

| Channel | Reporter | What it tracks | Direction |
| --- | --- | --- | --- |
| Green | EvaGreen, free in solution | Total double-stranded DNA, dominated by predator | Signal rises as predator rises |
| Red | Alexa Fluor 594 on the 3' end of G | Prey, via N-quenching | Signal falls as prey rises |

EvaGreen is an intercalating dye. It is not specific, but predator duplex dominates the signal, so we read it as predator.

The second channel works by nucleobase quenching. The dye sits on the template's 3' end. When prey hybridises there, nearby guanines quench the dye and fluorescence drops. So the red trace is inverted relative to prey concentration. Fujii inverts it before plotting, which is why their figures look the opposite way round to the raw data.

The two traces should run roughly a quarter-cycle out of phase: prey peaks, then predator peaks as it eats the prey, then both crash and the cycle restarts.

# What the model predicts

PEG and Ficoll should behave differently at the same volume fraction. That divergence is our falsifiable claim.

The dry-lab model (`crowded_mechanistic.py`) is a seven-species mass-action network: free N, P and G, plus the four complexes N-G, N-P, N-Exo and P-Exo, with enzyme conservation. Crowding does not enter as a fudge factor on rate constants. It enters through three physical channels that are computed once and then applied to every elementary step.

| Channel | What it does | PEG 8000 | Ficoll 400 |
| --- | --- | --- | --- |
| Excluded volume (scaled-particle theory) | Favours compact states, so binding tightens | Coil, R 3.4 nm, strong per unit volume | Sphere, R 10 nm, much milder |
| Water activity | Osmolyte effect on hybridisation | Strong, k 0.90 | Weak, k 0.25 |
| Preferential interaction (enthalpic) | Surface-burial term | Near zero, PEG is near-ideal toward DNA | 0.35, Ficoll is the enthalpic crowder |

On top of these, two enzyme-class factors are taken from measured data: polymerase and nickase turnover goes **up** under crowding, exonuclease turnover goes **down**. The exonuclease slowdown is the dominant effect, because the death arm is what holds the limit cycle together.

## Headline results

| Condition | Period | Outcome |
| --- | --- | --- |
| Dilute (no crowder) | ~90 min | Sustained oscillation, predator swings ~22 to ~154 nM |
| PEG 8000, increasing | Shortens toward ~73 min | Crosses a Hopf bifurcation, oscillation **lost** at roughly 10 to 12 percent w/v |
| Ficoll 400, increasing | Shortens | Oscillation **persists** past 18 percent w/v, amplitude reduced but alive |

So the prediction is: add PEG and the clock stops. Add the same volume fraction of Ficoll and it keeps ticking. If that holds in the wet lab it is a clean result, and it says crowding is not one single physical effect but at least two that can be separated by chemistry.

## Honest caveats

- The exonuclease crowding response is extrapolated from *E. coli* Exonuclease I, not measured for ttRecJ. **Measuring ttRecJ activity against PEG and Ficoll is the single most valuable wet-lab calibration we can do.**
- Every Ficoll 400 number is an extrapolation. No primary Ficoll 400 datum existed in the 47-paper literature scan.
- The model is a well-mixed ODE. It cannot represent local depletion zones or spatial trapping, which is real crowding physics it misses.
- Predictions are for PEG **8000** and Ficoll **400** specifically. A different molecular weight changes the excluded volume per unit w/v and the numbers do not transfer.
