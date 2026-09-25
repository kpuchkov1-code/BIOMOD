# Wet lab

Everything needed to set the oscillator up at the bench: what the circuit is,
how our version departs from Fujii, what goes in every well, and the
step-by-step protocol.

Last reconciled **25 September 2026** against Audrey's lab book (pages 148-155,
24 August), the Galas correspondence, and the reagents physically in hand.

## Start here

| File | What it is |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | **The bench protocol.** Sequential instructions, every concentration and volume. This is the one to have open while pipetting. |
| [01-project.md](01-project.md) | What we are building and how the circuit works. Read once. |
| [02-deviations.md](02-deviations.md) | How our experiment differs from the 2013 paper, and what each change risks. |
| [03-reagents.md](03-reagents.md) | Every component, what it does mechanistically, and the volume that delivers it. |
| [04-budget.md](04-budget.md) | How many runs each reagent buys, and whether to halve the well volume. |
| [05-plate-layout.md](05-plate-layout.md) | Which well holds what, and why each control earns its place. |
| [06-labbook-crosscheck.md](06-labbook-crosscheck.md) | This document against Audrey's numbers: what agreed, what was corrected. |

`BIOMOD_2026_Project_Brief.docx` is all of the above assembled into one Word
document for anyone who would rather read it that way.

## Current status

**Nothing blocks a first run.** The protocol is complete and every reagent
needed for it is in hand.

Confirmed and settled:

- Well volume **100 uL**, 90 uL master mix + 10 uL combined oligo stock
- Buffer recipe, all nine components independently reproduced by the lab book
- Oligos delivered and their resuspension volumes calculated (G 103 uL, N 286 uL, P 145 uL to 100 uM)
- Nb.BsmI in hand: R0706S, 10,000 U/mL, 0.1 mL
- ttRecJ in hand: 100 uL from Lab Jean Perrin, used at 1 percent v/v

## The one real constraint

**The nickase gives two runs. Everything else gives a dozen or more.**

| Reagent | Runs it buys |
| --- | --- |
| **Nb.BsmI** | **2** |
| ttRecJ | ~12 |
| Template G | ~100 |
| Prey N, predator P | thousands |

This inverts the assumption the team worked under all summer. The
irreplaceable enzyme, the one that took a month of emails and cannot be
bought, is not the bottleneck. The ordinary catalogue enzyme is. And
Nb.BsmI has **no larger pack size** - it is sold only as R0706S, 1,000
units, so more runs means more tubes.

Do not trim the nickase per well to stretch the tube. Its concentration sets
the prey production rate, so cutting it changes the circuit. If nothing
oscillates afterwards you would not know whether to blame the crowder, the
exonuclease or the enzyme you just halved.

## Still open

None of these stop you starting.

- [ ] **Neat ttRecJ stock concentration** from Jean-Christophe Galas, in nM or mg/mL. Only needed to give the model a molar number - the 1 percent working dilution is his lab's own calibration and is correct as written.
- [ ] **POLARstar filter list**, to confirm AF594 (emits ~617 nm) can actually be read. Worth checking before spending one of two nickase runs finding out.
- [ ] **Which PEG the lab holds**, and whether there is any Ficoll 400 at all. PEG versus Ficoll is the entire experiment.
- [ ] **Provenance of G 160 nM, N 10 nM, P 30 nM.** Not Fujii's numbers. Template concentration is the main bifurcation parameter, so it matters whether these were chosen or inherited.
- [ ] **Bst molar concentration** for the M0275 lot. Still specified as 0.75 percent v/v with no molar anchor. Polymerase is usually in excess, so this is the least urgent item here.

## Divergence from the model

The model in [`../crowding/`](../crowding/) runs **G = 140 nM**; the bench will
run **160 nM**. Template concentration is the model's main bifurcation
parameter, so the predicted Hopf threshold will shift. Re-run the model at
160 nM before quoting its numbers against wet-lab data.

## Editing these files

They are generated. [`source/biomod_brief.md`](source/biomod_brief.md) is the
single authored source, split into this set and built into the .docx by the
scripts in [`source/`](source/README.md). Edit the source, not these files, or
the next rebuild will overwrite you.
