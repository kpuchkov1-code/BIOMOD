# Cross-check against the lab book

*Audrey's bench numbers against this document: agreements, corrections, and what is still outstanding.*

> Part of the [wet lab documentation set](README.md). The assembled Word version of all of these is `BIOMOD_2026_Project_Brief.docx`.


---

# Cross-check against the lab book

Audrey's lab book (pages 148 to 155, dated 24 August) independently reproduces the buffer recipe I had marked VERIFY. **All nine buffer components match exactly.** Those rows are now confirmed, not assumed.

## Confirmed, no action

| Component | Lab book | This document | |
| --- | --- | --- | --- |
| Tris-HCl pH 8.8 | 20 mM | 20 mM | agree |
| (NH4)2SO4 | 10 mM | 10 mM | agree |
| KCl | 10 mM | 10 mM | agree |
| NaCl | 50 mM | 50 mM | agree |
| MgSO4 | 8 mM | 8 mM | agree |
| dNTPs each | 400 uM | 400 uM | agree |
| Synperonic F108 | 0.1 % | 0.1 % | agree |
| Netropsin | 2 uM | 2 uM | agree |
| EvaGreen | 1x | 1x | agree |
| BSA | 100 mg/L | 100 ug/mL | agree, same number |
| Nb.BsmI | 6 uL per 100 uL well | 6 uL per 100 uL well | agree exactly |

## Where the lab book is right and this document was wrong

| Item | I had | Lab book | |
| --- | --- | --- | --- |
| **DTT** | 1 mM | **4 mM** | Lab book wins, corrected throughout |
| **ET SSB** | about 100 nM, flagged undecided | **5 mg/L (5 ug/mL)** | Lab book wins, and it is Fujii's reagent |
| **Template G** | 140 nM | **160 nM** | Lab book wins for the bench |
| **Prey N** | 5 nM | **10 nM** | Lab book wins |
| **Predator P** | 5 nM | **30 nM** | Lab book wins |

The lab book also adds two handling details this document missed: **template G must be wrapped in foil**, because the AF594 label photobleaches, and **netropsin is light-sensitive too**.

Note that predator is seeded at three times prey, not equal. That is a deliberate asymmetry and it sets where on the cycle the first oscillation starts.

## Three things the lab book has not caught

**1. The planned master mix needs more nickase than we own.** This is arithmetic, not opinion.

The lab book plans 1800 uL of master mix for 20 reactions, calling for **120 uL of Nb.BsmI**. NEB R0706S contains 1,000 units at 10,000 units/mL, which is **100 uL of enzyme solution in total**.

The 20-reaction master mix cannot be made. It is 20 percent short of the entire tube.

**Confirmed 25 September: we hold one R0706S, 10,000 U/mL, 0.1 mL.** At 6 uL per 100 uL well that is a hard ceiling of **16 wells of master mix out of the entire tube**, before any pipetting loss. The nine-well plate actually drawn up (A1-3, B1-3, C1-3) needs six wells of master mix, about 47 uL of nickase, so **one tube covers two runs and no more**.

There is **no larger size to order**. Unlike almost every neighbouring enzyme in NEB's catalogue, Nb.BsmI is sold only as R0706S, 1,000 units. More nickase means more tubes, at roughly 34 US dollars per run on NEB's 2025 academic list price of 68 dollars per tube. Check Imperial's own supplier price before budgeting off that.

**2. The Bst and ttRecJ concentrations are not anchored to Fujii.** The lab book sets Bst at 0.75 percent v/v and ttRecJ at 1 percent v/v, and the worked example defines the final concentration as 0.75 percent of the stock, then solves for the volume. That is circular: it returns 0.75 percent of 100 uL by construction.

Those volume fractions are not Fujii's 3.7 nM and 32.5 nM. For Nb.BsmI it does not matter, because 600 units/mL is a real specification.

**For ttRecJ this concern is now largely withdrawn.** Galas's email of 22 July confirms the aliquot is a 1/160 dilution prepared specifically to be used at 1 percent. The lab book's figure is his lab's own calibration, so the death arm is correctly dosed even though we cannot yet state it in nM. See the resolved note earlier in this document.

**For Bst it still stands.** 0.75 percent v/v is a YOKABIO number with no molar anchor, and the lab book's worked example is circular: it defines the final concentration as 0.75 percent of the stock and then solves for the volume, which returns 0.75 uL by construction. Polymerase is usually in excess so this bothers us less, but it is unresolved.

**3. There is no room for PEG.** The layout is 90 uL master mix plus 10 uL oligos, totalling exactly 100 uL. Adding crowder means displacing something. Phase 2 needs a different layout, given at the end of the protocol below.

## One consequence for the dry lab

The model runs at **G = 140 nM**; the bench will run at **160 nM**. Template concentration is the model's main bifurcation parameter, so the predicted Hopf threshold will shift. The model should be re-run at 160 nM before its numbers are quoted against wet-lab data.
