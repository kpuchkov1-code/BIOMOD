# Plate layout and controls

*Which well holds what, and why each control earns its place.*

> Part of the [wet lab documentation set](README.md). The assembled Word version of all of these is `BIOMOD_2026_Project_Brief.docx`.


---

# Plate layout and controls

Thirteen wells per run. Use inner wells only and fill the outer ring with water to insulate against edge cooling.

| Wells | Contents | What it tells us |
| --- | --- | --- |
| B2-B4 | Full reaction, triplicate | The oscillation itself |
| C2-C4 | Blank: everything except oligos | Background from buffer, dye and enzymes. Catches enzyme autofluorescence and DNA contamination. |
| D2-D4 | Buffer only: no enzymes, no oligos | Background from plate and buffer alone |
| E2 | No prey | Gain adjustment, single well |
| F2 | No predator | Gain adjustment, single well |

The two gain-adjustment wells need only one well each, not triplicates. They exist so the POLARstar can set detector gain against a known signal floor before the run starts.

Comparing the blank against the buffer-only control is the troubleshooting step. High signal in the blank but not in buffer-only points to the enzymes: autofluorescence or nucleic acid contamination. High signal in both points to the plate or the buffer. Once the first run is clean, later runs need only the blank.

## Working through the plate

A 96-well plate holds far more wells than one run uses, and plates are expensive. Load 13 wells, seal the whole plate with optical film, run it, then peel the film off, load the next 13 wells further down, and reseal. Update the well allocations in the POLARstar protocol each time, so B2-B4 becomes G2-G4 and so on.

## Assembly order

1. Make stock solutions of each buffer component.
2. Make the 4x buffer stock.
3. Make the master mix: everything shared across all wells, assembled on ice.
4. Resuspend the oligos and make the combined oligo stock.
5. Pipette anything that differs well to well directly into the well first, in minimal volume, then add master mix on top. This keeps the shared components identical across wells.
6. Seal, mix gently, spin the plate down.
7. Load into the POLARstar, already preheated to 45 C for at least 40 minutes.

Preheating matters. Going in cold means the enzymes work at the wrong temperature while the plate equilibrates, and the first cycle is unreliable.

## First run should have no crowder

Run the baseline to a clean 90-minute oscillation before adding any PEG or Ficoll. If the dilute cycle does not work, nothing measured under crowding means anything. YOKABIO spent most of their project just getting the baseline circuit to run, and they still placed 3rd. Expect this to take several attempts.
