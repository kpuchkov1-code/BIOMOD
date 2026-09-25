# How we differ from Fujii

*Every deliberate departure from the 2013 paper, and what each one risks.*

> Part of the [wet lab documentation set](README.md). The assembled Word version of all of these is `BIOMOD_2026_Project_Brief.docx`.


---

# How our experiment differs

The chemistry is identical to Fujii. The hardware and the reporter are not, and that is where the risk sits.

Two reference experiments matter. **Fujii et al. 2013** (ACS Nano) is the original predator-prey oscillator and the source of our sequences and constants. **YOKABIO 2025** (Kyushu Institute of Technology, 3rd worldwide) ran the same circuit at BIOMOD last year and tuned the period by chemically modifying the template.

| | Fujii 2013 | YOKABIO 2025 | Us |
| --- | --- | --- | --- |
| Strands N, P, G | Same sequences | Same | **Same, unchanged** |
| Polymerase | Bst large fragment | Bst | **Bst, same** |
| Nickase | Nb.BsmI | Nb.BsmI | **Nb.BsmI, same** |
| Exonuclease | ttRecJ | ttRecJ | **ttRecJ, same** (gift from Lab Jean Perrin, Paris) |
| Instrument | Bio-Rad CFX / MiniOpticon qPCR | qPCR | **BMG POLARstar Omega plate reader** |
| Vessel | 20 uL PCR tubes | 20 uL tubes | **96-well plate, ~100 uL per well** |
| Temperature | 46.5 C | 46 C | **45 C** (instrument ceiling) |
| Prey reporter dye | Dy530 on G 3' end | Dy530 | **Alexa Fluor 594** |
| Predator reporter | EvaGreen | EvaGreen | **EvaGreen, same** |
| Evaporation control | Heated lid | Heated lid | **Optical adhesive film** |
| Cross-talk correction | qPCR built-in software | Built-in | **Manual, plus blank wells** |
| Tuning variable | None, baseline study | Amino-acid modification of template G | **PEG 8000 and Ficoll 400 as inert crowders** |

## Why each change happened

**Instrument.** Dr Ouldridge directed us to the lab's POLARstar plate reader rather than a qPCR machine. It is a genuine advantage for this project: a 96-well plate runs many crowder concentrations in parallel in one 12-hour run, where a qPCR block would take many sequential runs. It costs us the heated lid and the uniform Peltier block.

**Temperature.** The POLARstar's standard configuration caps at 45 C. Fujii's 46.5 C is a design point, not a hard requirement, and the SI explicitly notes the reaction oscillates over a range of several degrees provided enzymes and template are adjusted. We are 1.5 C below the strands' design temperature.

**Dye.** This was forced, not chosen. Dy530 is not offered by IDT. JOE, the obvious substitute, emits at 545 nm and the POLARstar's filter wheel has no band covering it. Audrey worked through every nucleobase-quenchable dye from the N-quenching paper against IDT's 3' modification list and the available filters. Alexa Fluor 594 was the only survivor that IDT sells, that N-quenching is documented to work with, and that does not overlap EvaGreen.

**Tuning variable.** This is the scientific contribution. YOKABIO modified the template covalently. We change only the solvent. Stated in one line: YOKABIO modulated a PEN oscillator with amino acid modification, we modulate it with inert polymers.

# Risks these changes create

Ranked by how badly each one would hurt and how cheap it is to check first.

**1. The Alexa Fluor 594 signal may fall outside the emission filter.** AF594 emits at 617 nm. The filter is 610-10, meaning a 10 nm band centred on 610, so roughly 605 to 615 nm. The peak sits just outside it. Lulah said it looked acceptable against the two filters she checked but could not speak for the others, and nobody has confirmed the band actually catches enough signal. If it does not, the prey channel is weak or dead and we lose half the data. This is the highest-value thing to test and it costs one well.

**2. Plate thermal gradients.** qPCR blocks heat uniformly and have a heated lid. Plate readers heat from below or the sides, so edge wells run cooler than centre wells. Fujii's own SI warns that enzyme and template concentrations need adjusting across even a few degrees. Use inner wells only and fill the outer ring with water.

**3. Evaporation over 12 hours.** Without a heated lid, a plate at 45 C loses volume into the well headspace. Optical adhesive film is essential, pressed down hard. If the traces drift upward steadily across a run, suspect evaporation before suspecting chemistry.

**4. The 5x volume scale-up is unexamined.** Going from 20 uL to 100 uL changes the surface-to-volume ratio, which changes enzyme adsorption onto plastic, evaporation rate, and time to reach temperature. No one has worked this through. The concentrations in the table below are Fujii's, unchanged; only the volumes scale.

**5. ET SSB may blunt the very effect we are measuring. Phase 2 concern only.** Resolved 25 September: ET SSB is Fujii's own reagent, listed in his SI among the components added at assembly, so using it is fidelity rather than deviation. It needs no model term either, because Table S5's rate constants were measured with it present and already absorb its effect.

What remains is narrower. SSB coats single-stranded DNA, and single-stranded DNA is where crowding acts hardest on this network, so SSB may damp the crowding response. Keep the baseline faithful and settle it later with a plus/minus SSB pair at one PEG concentration.

**6. We have PEG but no Ficoll.** Confirmed 25 September. The molecular weight of the PEG is still unconfirmed, and the model's headline result is calculated for PEG **8000** specifically, so that needs checking on the bottle.

This does not affect phase 1 at all. The reproduction run contains no crowder, so neither polymer is needed to start.

It does matter for the project as a whole, because the falsifiable claim is that PEG stops the clock and Ficoll does not. **PEG alone gives a concentration series, not a comparison.** A PEG-only result is still a real finding, but it cannot separate excluded volume from chemistry, which is the interesting part. Ficoll 400 is an ordinary catalogue reagent, so this is a purchasing lead-time problem rather than a scientific one. Put it on an order list now and it will not be a problem in November.

**7. dNTP supply caps the number of runs.** The lab tube holds 200 uL of 10 mM dNTP mix. At 80 uL per 500 uL of 4x buffer stock that is two or three runs before reordering. Aliquot it now to avoid repeated freeze-thaw.

## Not a risk any more

The exonuclease question is closed. The team secured genuine ttRecJ from Paris in August, so we are not running the mesophilic RecJf substitute and there is no enzyme-decay problem across a 12-hour run. The model was updated to match: it now runs `exo="ttRecJ"` at 45 C with the native Fujii constants.
