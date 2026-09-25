# Reagent budget and well volume

*How many runs each reagent buys, why the nickase is the bottleneck, and whether to halve the well to 50 uL.*

> Part of the [wet lab documentation set](README.md). The assembled Word version of all of these is `BIOMOD_2026_Project_Brief.docx`.


---

# Reagent budget and the well volume decision

## How many runs each reagent buys

One run is six wells of master mix (B1-3 and C1-3). A1-3 carry buffer and water only, so they cost no enzyme. Assume 700 uL of master mix per run, which is a comfortable excess over the 540 uL strictly needed.

| Reagent | What we hold | Per run | Runs |
| --- | --- | --- | --- |
| **Nb.BsmI** | 100 uL | 46.7 uL | **2** |
| ttRecJ | 100 uL | 7.8 uL | about 12 |
| Template G | 10.3 nmol | ~0.1 nmol | about 100 |
| Prey N, Predator P | 28.6 / 14.5 nmol | negligible | thousands |
| dNTPs | one tube | 80 uL per 500 uL buffer | 2 to 3 |

**The nickase is the bottleneck, and nothing else is close.** This is worth stating plainly because it inverts the assumption the team has been working under since July. The irreplaceable reagent, the one that took a month of emails and cannot be bought at any price, gives us twelve runs. The ordinary catalogue enzyme gives us two.

A note on the ttRecJ figure. Galas calculated 1,000 reactions from the 100 uL aliquot, but he assumed 10 uL reactions. Ours are ten times larger, so the same aliquot covers about 100 wells, not 1,000. Twelve runs, not a hundred and twenty.

## Should we halve the well to 50 uL?

Every reagent count above doubles if we do: four runs of nickase, twenty-five of ttRecJ. That is the whole argument in favour, and it is a real one.

**Evaporation is the argument against, and it is specific to this project.** A 96-well plate presents the same surface area whether the well holds 50 or 100 uL, so the same absolute volume of water leaves over a 12-hour run at 45 C. At 50 uL that is twice the fraction of the reaction. Everything left behind concentrates as it happens, including the crowder.

That is the problem. Crowder concentration is the independent variable. Letting it drift upward during the run, and drift further in a 50 uL well than a 100 uL one, puts a systematic error directly on the axis being measured.

It is defensible with the sealing already planned, an optical adhesive film pressed hard at every edge plus the water moat in the outer ring. **The test is to weigh the plate before and after the run.** Under about 2 percent mass loss and the concern is closed with a number rather than an argument.

Three smaller costs:

- **Signal.** Top-reading optics see roughly half the material, so about half the fluorescence. Gain compensates but the noise floor does not fall with it, so signal-to-noise degrades. The AF594 red channel is already the marginal one.
- **Focal height.** The reader focuses at a fixed height above the well and the optimum moves with fill depth. Re-run gain and focus adjustment rather than reusing settings, and never compare raw counts between a 50 uL run and a 100 uL one.
- **Viscous crowder.** Delivering 25 uL of 18 percent PEG accurately is harder than 50 uL. Cut tips, slow aspiration, reverse pipetting.

One thing that looks like a problem and is not: the small enzyme volumes. Bst at 0.375 uL is unpipettable, but it never gets pipetted alone. It goes into the master mix, which stays large. Per well the handling is 45 uL of mix and 5 uL of oligo stock, both comfortable.

**Recommendation.** Run the first experiment at 100 uL exactly as written, because it should be comparable to Fujii and to the protocol everyone has read. Weigh the plate. If evaporation behaves, move to 50 uL for the crowder sweep, where many conditions matter and the doubled budget buys something real.
