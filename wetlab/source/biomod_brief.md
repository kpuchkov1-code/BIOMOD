---
title: "BIOMOD 2026: Project Brief, Deviations and Reaction Setup"
subtitle: "Imperial College London, BIOMOD 2026"
date: "25 September 2026"
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

**5. ET SSB is in the buffer but not in the model.** It coats single-stranded DNA, which is exactly what crowding acts on, and it is known to modulate RecJ-family exonuclease activity. If we use it, the model has a gap. If we omit it, we deviate from Fujii. Worth deciding deliberately rather than by default.

**6. We have PEG but no Ficoll.** Confirmed 25 September. The molecular weight of the PEG is still unconfirmed, and the model's headline result is calculated for PEG **8000** specifically, so that needs checking on the bottle.

This does not affect phase 1 at all. The reproduction run contains no crowder, so neither polymer is needed to start.

It does matter for the project as a whole, because the falsifiable claim is that PEG stops the clock and Ficoll does not. **PEG alone gives a concentration series, not a comparison.** A PEG-only result is still a real finding, but it cannot separate excluded volume from chemistry, which is the interesting part. Ficoll 400 is an ordinary catalogue reagent, so this is a purchasing lead-time problem rather than a scientific one. Put it on an order list now and it will not be a problem in November.

**7. dNTP supply caps the number of runs.** The lab tube holds 200 uL of 10 mM dNTP mix. At 80 uL per 500 uL of 4x buffer stock that is two or three runs before reordering. Aliquot it now to avoid repeated freeze-thaw.

## Not a risk any more

The exonuclease question is closed. The team secured genuine ttRecJ from Paris in August, so we are not running the mesophilic RecJf substitute and there is no enzyme-decay problem across a 12-hour run. The model was updated to match: it now runs `exo="ttRecJ"` at 45 C with the native Fujii constants.

# What goes in each well

Final concentrations are Fujii's, unchanged. Only the volume scales, from 20 uL to 100 uL.

Read the Source column before you pipette. Values marked **SI** were quoted directly from the Fujii supplementary information in our own team records. Values marked **VERIFY** are the standard PEN buffer recipe and must be checked against SI Table S1 before the first run. Do not treat this table as the protocol until that check is done.

## Final concentrations in the reaction

| Component | Final conc. | Role | Source |
| --- | --- | --- | --- |
| Tris-HCl pH 8.8 | 20 mM | Buffer | VERIFY (pH 8.8 confirmed) |
| (NH4)2SO4 | 10 mM | Ionic strength | VERIFY |
| KCl | 10 mM | Ionic strength | VERIFY |
| NaCl | 50 mM | Ionic strength | VERIFY |
| MgSO4 | 8 mM | Essential cofactor, all 3 enzymes | VERIFY |
| dNTPs (each) | 400 uM | Fuel for synthesis | **SI** |
| DTT | 4 mM | Reducing agent, enzyme stability | CONFIRMED (lab book) |
| BSA | 100 ug/mL | Enzyme stabiliser, anti-adsorption | VERIFY |
| Synperonic F108 | 0.1 % | Surfactant, prevents surface loss | VERIFY |
| Netropsin | 2 uM | Suppresses non-specific amplification | VERIFY |
| EvaGreen | 1x | Predator reporter | VERIFY |
| ET SSB | 5 ug/mL | Single-strand binding | CONFIRMED (lab book) |
| Bst polymerase | 3.7 nM | Extension | **SI** |
| Nb.BsmI nickase | 600 U/mL | Nicking | **SI** |
| ttRecJ exonuclease | 32.5 nM | Degradation | **SI** |
| Template G (AF594) | 140 nM (baseline) | The machine | Model baseline, Fujii varies this |
| Prey N | ~1-10 nM | Initiator, small seed | Fujii: "a small amount" |
| Predator P | ~1-10 nM | Initiator, small seed | Fujii: "a small amount" |
| PEG 8000 or Ficoll 400 | 0 to 18 % w/v | **Our variable.** Omit for baseline runs. | Our addition |

The five sections that follow take each component in turn: what it does, how it works, and what breaks without it. If you are pipetting, the summary table above and the volumes further down are what you need. If you are writing the wiki or answering a judge, read the detail.

## The buffer system

Five components that between them set pH, ionic strength and the magnesium supply. Two of them contain traps.

**Tris-HCl, 20 mM, pH 8.8.** Holds the pH steady against the protons released every time the polymerase forms a phosphodiester bond. Bst works best around pH 8.8, and mildly alkaline conditions keep DNA fully deprotonated and soluble.

The trap: **Tris pH falls as temperature rises**, by about 0.028 units per degree. A buffer titrated to pH 8.8 on the bench at 25 C is sitting near **pH 8.25 once the plate reaches 45 C**. That is normal and it is what Fujii's recipe assumes, so titrate at room temperature and do not try to correct for it. Just be aware the reaction is not actually running at 8.8, and never titrate a warm buffer.

**Ammonium sulfate, 10 mM.** The stringency component. Ammonium ions compete weakly at the DNA backbone and preferentially destabilise short, imperfect or mismatched duplexes, while leaving correctly matched ones intact. In a system built on 10 base pair interactions this is what keeps prey binding where it should and not somewhere almost-right. Sulfate is a kosmotropic anion that stabilises protein folding, so it helps the enzymes survive 12 hours at 45 C.

**Potassium chloride, 10 mM, and sodium chloride, 50 mM.** Monovalent cations screen the negative charge on the DNA phosphate backbone. Two strands cannot pair unless that repulsion is neutralised, so salt concentration directly sets duplex stability.

This matters more here than in most protocols. The circuit depends on 10 to 14 base pair duplexes being **marginally** stable at 45 C, forming and melting within seconds. Salt concentration is one of the two dials that sets that margin, temperature being the other. Getting the salt wrong shifts every hybridisation in the network at once, and it will look like an enzyme problem.

**Magnesium sulfate, 8 mM.** The most important single ion in the tube, and it does two unrelated jobs.

First, it is the **catalytic cofactor for all three enzymes**. Bst uses two-metal-ion catalysis: one Mg2+ activates the primer's 3' hydroxyl for attack, the other stabilises the negative charge building on the incoming dNTP's triphosphate as the bond forms. Nb.BsmI needs Mg2+ to hydrolyse the phosphodiester backbone. ttRecJ is a Mg2+-dependent nuclease. Remove magnesium and all three stop at once.

Second, being divalent it screens DNA charge far more effectively than sodium or potassium, so it stabilises every duplex in the system.

The trap: **dNTPs chelate magnesium one to one.** At 400 uM each, total dNTP is 1.6 mM, which locks up 1.6 mM of the 8 mM magnesium. Free magnesium available for catalysis is therefore closer to **6.4 mM**, not 8. Fujii's recipe already accounts for this, so do not add extra, but if you ever change the dNTP concentration you must change magnesium to match or you will silently starve the enzymes.

There is a second-order point relevant to our project specifically. PEG weakly chelates magnesium. At high PEG concentrations some of the free magnesium is sequestered, which is an effect the crowding model deliberately does **not** include, because no measured constant exists for it and the correct treatment needs divalent electrostatics rather than the monovalent approximation. If PEG results come out stronger than the model predicts, this is one candidate explanation.

## Fuel and protectors

One component the system consumes, three that keep it alive for 12 hours.

**dNTPs, 400 uM each.** The building blocks and the energy source at the same time. Every base the polymerase adds arrives as a triphosphate; the bond forms and pyrophosphate leaves, and hydrolysis of that pyrophosphate is what makes the reaction irreversible. Nothing in this system is at equilibrium, and dNTPs are what pays for that.

At 400 uM each the pool is large compared with the 140 nM template and the roughly 150 nM of strand turning over per cycle, so the model treats it as effectively infinite. That assumption is reasonable for a few hours and **questionable across a full 12-hour run**. dNTP depletion is a known, flagged limitation of the model: if the oscillation amplitude decays steadily late in a run rather than holding, running out of fuel is the first thing to check.

Practical note: dNTPs are the most freeze-thaw sensitive thing in the freezer. Aliquot into single-run volumes now.

**DTT, 4 mM.** A reducing agent. Enzymes carry cysteine residues whose thiol groups oxidise over time, forming disulfide bridges that lock the protein into a wrong shape. DTT keeps sacrificing itself to reverse that, so the enzymes stay folded and active.

Worth knowing: **DTT itself degrades**, and it degrades faster when warm and alkaline. At pH 8.5 and 40 C its half-life is on the order of hours, not days. Over a 12-hour run at 45 C the DTT is substantially gone by the end. Nothing to do about it within Fujii's recipe, but if late-run behaviour looks like gradual enzyme death, this is a plausible mechanism alongside dNTP depletion.

**BSA, 100 ug/mL.** Bovine serum albumin, a sacrificial carrier protein. Its main job here is to coat the plastic. Enzymes at single-digit nanomolar concentrations will otherwise adsorb onto the well walls and effectively disappear from solution.

This matters more for us than for Fujii. **We moved from 20 uL PCR tubes to 100 uL plate wells**, which changes the surface-to-volume ratio and the plastic the reaction touches. BSA is the main thing standing between the enzymes and the wall. Do not omit it, and if anything this is the one component worth considering raising.

**Synperonic F108, 0.1 percent.** A non-ionic surfactant. Chemically it is a triblock copolymer, polyethylene oxide then polypropylene oxide then polyethylene oxide, the same molecule sold as Pluronic F108. It adsorbs onto plastic and onto air-water interfaces, blocking protein and DNA from sticking there, and it stops bubbles forming during mixing. Together with BSA it is why Fujii's reactions survive days in a sealed tube.

**A point specific to our project.** Synperonic F108 is a polyethylene-oxide polymer. That is the same chemistry as PEG. At 0.1 percent it contributes a volume fraction of well under a tenth of a percent, far below the 10 percent w/v where we expect PEG to kill the oscillation, so it is not going to confound the result. But it does mean **every well already contains a trace PEG-family crowder, including the zero-crowder baseline**. Our baseline is not a truly crowder-free reference, it is a very-low-crowder one. Worth a sentence in the write-up rather than leaving a judge to spot it.

## Specificity and reporting

One component keeps the reaction honest. Two let us watch it. One is still undecided.

**Netropsin, 2 uM.** The least obvious component and arguably the one that decides whether a 12-hour run succeeds.

Left alone for long enough, Bst does something inconvenient: it starts synthesising DNA with no template at all. These **parasitic** or ab initio products are self-replicating, they compete for the same polymerase and dNTPs as the real circuit, and because they replicate exponentially they eventually take over the tube. Every long PEN experiment fights this.

Netropsin is the countermeasure. It is a minor-groove binder that sits in the narrow groove of the double helix, and it strongly prefers runs of four or five consecutive A-T base pairs. Parasitic products that emerge spontaneously are overwhelmingly AT-rich, because AT-rich sequences are easier to melt and re-prime. Our designed strands are the opposite: prey is 60 percent GC and contains no AT run longer than two. So netropsin binds and stalls the parasites while leaving the real circuit essentially untouched.

It is a selective poison that exploits a base-composition difference between what we want and what we do not. This is also why you cannot casually redesign these sequences to be AT-rich.

In the model, the residual background that netropsin fails to suppress is what the `LEAK` terms represent.

**EvaGreen, 1x.** The predator channel. It is a DNA-binding dye that fluoresces brightly when bound to double-stranded DNA and weakly when free in solution, so signal tracks total duplex. Duplex is dominated by predator, so we read the green trace as predator concentration.

EvaGreen was chosen over SYBR Green I because it is markedly **less inhibitory to polymerases**, which matters over 12 hours. Lulah confirmed this independently when she suggested we keep it.

One caveat to hold in mind: a dye that binds duplex also mildly **stabilises** duplex. In a system deliberately poised at the edge of duplex stability, EvaGreen is a small perturbation on the thing we are measuring. It is in Fujii's recipe too, so it is common to both, but it is not nothing.

**Alexa Fluor 594, on the 3' end of template G.** The prey channel, and it reports **backwards**.

The dye is attached to the template, not to prey. When prey hybridises to the template's 3' end, guanines on the incoming strand come within a few angstroms of the fluorophore and quench it through photoinduced electron transfer. So **fluorescence falls as prey rises**. Fujii inverts this trace before plotting, which is why the published figures look the opposite way round to raw instrument output. Expect the raw data to look wrong at first glance.

This is the component we changed, and it is the project's biggest unforced risk. See the risks section.

**ET SSB, around 100 nM. Undecided.** Extreme Thermostable Single-Stranded DNA Binding protein coats single strands, stops them folding into hairpins or mispairing, and improves polymerase processivity.

The problem is that it does its job by binding exactly the thing two other parts of the system care about. **ttRecJ is a single-strand-specific exonuclease**, so SSB and ttRecJ compete for the same substrate, and SSB is documented to modulate RecJ-family activity directly. Separately, single-stranded DNA is precisely where crowding exerts most of its effect on this network, so coating it changes what we are trying to measure.

So: include it and the model has an unrepresented interaction sitting right on the death arm. Omit it and we have deviated from Fujii in a second place. Either is defensible. What is not defensible is deciding it by accident, which is the current position.

## The three enzymes

Each one is a specific variant, and in every case the variant matters more than the family.

**Bst DNA polymerase, large fragment, 3.7 nM.** Does all the synthesis, in both the growth and the predation steps. Three properties make it the right choice:

1. **Strand displacement.** When it runs into a downstream duplex it peels that strand off and keeps going rather than stopping. The growth step needs this.
2. **No 5' to 3' exonuclease activity.** This is what "large fragment" means: the native enzyme's 5' nuclease domain has been removed. Full-length Bst would **digest** the downstream strand instead of displacing it, destroying the product we want to release. Ordering full-length Bst by mistake would break the circuit in a way that looks like a mysterious yield problem.
3. **Thermostability.** It holds activity for hours at 45 C. Its true optimum is 60 to 65 C, so at 45 C we are running it below optimum and turnover is slower than the datasheet suggests. That is expected and already baked into Fujii's concentrations.

It has no proofreading, but with 10 and 14 nucleotide products that does not matter.

**Nb.BsmI nickase, 600 U/mL.** Cuts one strand of a duplex, never both. It recognises `GAATGC` and cleaves one base beyond it.

The `Nb` prefix is the entire point. It means the enzyme nicks the strand **not** carrying the recognition sequence. In our growth complex, `GAATGC` sits in template G, so Nb.BsmI cuts the newly synthesised strand and leaves G intact. The `Nt` variant would do the opposite and destroy the template on the first cycle.

Work through the arithmetic and the nick lands **exactly** at the junction between the original prey and the fresh copy, releasing a clean 10-mer. The template is two tandem copies of prey's complement, and the single `GAATGC` site sits precisely where the seam is. That is designed, not lucky, and it is why the sequences cannot be changed casually.

The predator duplex contains `GAATG` but runs out of strand before the final `C`, so it has no site and the nickase ignores it. Also designed.

**ttRecJ exonuclease, 32.5 nM.** The death arm, and the engine of the oscillation. It degrades single-stranded DNA processively from the 5' end, down to mononucleotides. It cannot touch double-stranded DNA.

That single-strand specificity is the organising principle of the whole circuit. Species are safe while paired and vulnerable while free, which is why the template carries phosphorothioate linkages at its **5'** end specifically: block the end the enzyme starts from and G becomes permanently immune.

What makes it an oscillator rather than a decay curve is that ttRecJ binds the two substrates very differently:

| Substrate | Km | Behaviour |
| --- | --- | --- |
| Predator P | ~34 nM | Tight. Saturates the enzyme at working concentrations. |
| Prey N | ~1000 nM | Weak. Stays well below saturation throughout. |

Because predator saturates ttRecJ, predator is removed at a roughly **constant rate** regardless of how much is present. Prey, far from saturation, is removed in proportion to its concentration. That asymmetry between a zero-order and a first-order removal is the mathematical reason the system cycles instead of settling to a steady state. Take it away and there is no oscillation.

**Why thermostable specifically.** ttRecJ comes from *Thermus thermophilus* and holds activity across a 12-hour run at 45 C. The commercial alternative, NEB's RecJf, is the *E. coli* enzyme with an optimum at 37 C, and it would slowly lose activity over the run. Because the death arm is saturated, a drifting exonuclease concentration drags the period with it, and the oscillation would decay for reasons nothing to do with crowding. Securing genuine ttRecJ from Lab Jean Perrin removed that entire failure mode.

## The circuit strands and the crowders

Three oligos and one additive. Two of these are the experimental variables; the rest is fixed.

**Template G, 140 nM.** `C*G*G*CCGAATGCGGCCGAATG`, carrying Alexa Fluor 594 on the 3' end.

G is not consumed. It is the catalyst that makes prey autocatalytic, and it is the only species whose concentration stays constant through the whole run. Two modifications make that possible:

- **Phosphorothioates on the first three linkages.** Sulfur replaces a non-bridging oxygen in the backbone, which ttRecJ cannot cleave. They are at the 5' end because ttRecJ works 5' to 3'. Block the entry point and the whole strand is safe.
- **Alexa Fluor 594 on the 3' end**, positioned exactly where prey docks, so prey binding quenches it.

**G is the main tuning knob.** More template means faster prey growth, which shifts the whole limit cycle. Fujii varies G across their figures precisely because it is the parameter that moves the system through its different regimes. Our 140 nM is the model's baseline, not a universal constant. If the dilute oscillation does not appear at 140 nM, **titrating G is the first thing to try**, before touching anything else.

**Prey N, roughly 1 to 10 nM.** `CATTCGGCCG`. A seed, not a reagent. Its job is to break the symmetry of an empty system and get the first cycle going. Fujii says only "a small amount", and the exact figure is not critical because prey grows exponentially off the template within minutes regardless.

**Predator P, roughly 1 to 10 nM.** `CATTCGGCCGAATG`. Also a seed. Note that P is a palindrome, its own reverse complement, which is why it can template its own synthesis from prey.

The starting ratio of N to P sets where on the cycle you begin, which affects the phase of the first oscillation but not the period or the amplitude once the system settles. **5 nM each is a working assumption in the volume table below.** Fujii varies these deliberately in their Figure 4e experiment.

**PEG 8000 or Ficoll 400, 0 to 18 percent w/v.** The experiment.

These are the only components that are genuinely ours. They are chemically inert, they do not react with DNA or the enzymes, and they participate in no reaction in the network. They simply occupy space, and that alone changes the system through three routes:

| Route | Mechanism | Effect on the circuit |
| --- | --- | --- |
| Excluded volume | Crowders make compact states entropically favourable, because a bound pair displaces less solvent than two free molecules | Every duplex binds more tightly |
| Water activity | Crowders sequester water, raising the effective cost of the hydration shell that single strands carry | Hybridisation favoured further |
| Viscosity | Crowders slow diffusion, and more so for larger species | Encounter-limited steps slow down |

On top of these, the enzymes respond in opposite directions: **polymerase and nickase speed up** under crowding, while the **exonuclease slows down**. The exonuclease effect dominates, which is why the model predicts the death arm weakens and the limit cycle eventually collapses.

**The crowder is the only thing that changes between conditions.** Everything above stays identical across every well in a crowding series. If anything else varies, the comparison is void.

**Baseline runs contain no crowder at all.** Get a clean 90-minute oscillation with zero PEG before adding any. Measuring a crowding effect on a circuit that does not work is meaningless.

## Worked volumes for everything else

Assumes a 4x buffer stock holding the salts, magnesium, dNTPs, Synperonic, netropsin and EvaGreen. Fujii adds BSA, DTT, ET SSB, the enzymes and the oligos separately at assembly, and so should we.

| Added | Working stock | Volume into 100 uL | Delivers |
| --- | --- | --- | --- |
| 4x reaction buffer | 4x | 25.0 uL | Tris, salts, MgSO4, dNTPs, Synperonic, netropsin, EvaGreen at 1x |
| BSA | 10 mg/mL | 1.0 uL | 100 ug/mL |
| DTT | 100 mM | 1.0 uL | 1 mM |
| ET SSB | 500 ng/uL | 1.0 uL | If used, see the decision above |
| Bst polymerase | see note below | TBD | 3.7 nM |
| Nb.BsmI | 10,000 U/mL | 6.0 uL | 600 U/mL |
| ttRecJ | Paris aliquot, 1/160 dilution | 1.0 uL | 1 % v/v, the Galas working dilution |
| Oligos G, N, P | see next section | via master mix | 140 / 5 / 5 nM |
| Crowder, PEG or Ficoll | 50 percent w/v | 0 to 36 uL | 0 to 18 percent w/v |
| Nuclease-free water | | to 100 uL | Make the balance up last |

Two rows say TBD because two conversions are unresolved. Both are covered at the end of this section, and both need an email before the first run.

## Oligo concentrations and volumes

Only G needs to be accurate. N and P are seeds: being twofold out shifts the phase of the first cycle and nothing else. G sets the limit cycle, so an error there moves the result.

| Strand | Final in well | Why that number |
| --- | --- | --- |
| G, template | **140 nM** | The model baseline and the main tuning knob. Fujii scans a range across their figures. |
| N, prey | **5 nM** | Seed only. Fujii says "a small amount". Anything from 1 to 10 nM works. |
| P, predator | **5 nM** | Seed only. |

### How much that is, and how much we have

In a 100 uL well: G is 14 pmol, N is 0.5 pmol, P is 0.5 pmol.

Set that against what IDT delivered. At their smallest scale, roughly 25 nmol, the template alone covers **around 1,800 wells**, which is over a hundred full plates. Prey and predator at 0.5 pmol per well are effectively unlimited.

The oligos are not a constraint on how many runs we do and never will be. Nobody needs to ration the DNA. The real limit is the nickase, at two runs per tube. See the reagent budget below.

### Resuspension: dry tube to primary stock

IDT ships these dry. The actual delivered amount in nmol is printed on the spec sheet inside the tube, and it will not be exactly the nominal scale, so read the sheet rather than assuming.

To make a **100 uM primary stock**:

```
volume of nuclease-free water (uL) = delivered nmol x 10
```

So 25 nmol takes 250 uL, 43.7 nmol takes 437 uL. Vortex, leave 15 minutes to dissolve fully, store at -20 C. This is the archive stock and you will rarely touch it again.

TE is fine instead of water if you want better long-term stability. The EDTA in TE chelates magnesium, but carryover at these dilutions is single-digit micromolar against 8 mM Mg2+, so it does not matter.

### Working stocks

Two dilution steps, because 100 uM down to what we need is too large a jump to do accurately in one.

| Strand | Working stock | To make 100 uL |
| --- | --- | --- |
| G | **10 uM** | 10 uL primary + 90 uL water |
| N | **1 uM** | 10 uL primary + 90 uL water, then 10 uL of that + 90 uL water |
| P | **1 uM** | Same two-step dilution |

Do N and P in two steps rather than pipetting 1 uL from the primary. A P2 at the bottom of its range is the single largest source of error in this whole chain.

### Why the oligos go in the master mix

From those working stocks, one 100 uL well needs 1.4 uL of G, 0.5 uL of N and 0.5 uL of P.

You cannot pipette 0.5 uL into 13 separate wells and get 13 identical reactions. That volume is below reliable delivery on any pipette in the lab, and the well-to-well scatter would swamp the biology we are trying to measure.

So **prey and predator go into the master mix, never into individual wells**. For a batch of 16 wells, 13 used plus 3 spare for pipetting loss:

| Strand | Working stock | Into master mix | Delivers |
| --- | --- | --- | --- |
| G | 10 uM | 22.4 uL | 140 nM in every well |
| N | 1 uM | 8.0 uL | 5 nM in every well |
| P | 1 uM | 8.0 uL | 5 nM in every well |

This is exactly why Fujii's SI says to assemble shared components as a master mix and pipette only the varying component directly into the tube.

## Plate layout for a crowder series

The 4x buffer approach above works for baseline runs. For a crowding series it gets awkward, because reaching 18 percent w/v PEG from a 50 percent stock needs 36 uL, which consumes a third of the volume budget and squeezes everything else into unpipettable volumes.

Split the reaction in half instead:

```
50 uL   2x master mix      everything at double strength, identical in every well
50 uL   crowder solution   0 to 36 percent w/v, the only thing that varies
------
100 uL  final              everything at 1x, crowder at 0 to 18 percent w/v
```

The 2x master mix holds G at 280 nM, N at 10 nM and P at 10 nM. For 900 uL, enough for 16 wells with excess:

| Strand | Working stock | Into 900 uL of 2x master |
| --- | --- | --- |
| G | 10 uM | 25.2 uL |
| N | 1 uM | 9.0 uL |
| P | 1 uM | 9.0 uL |

Both halves stay at 50 uL whatever the crowder concentration. Pipetting volumes stay large, and the crowder is provably the only variable across the series. The zero-crowder control is 50 uL of water.

## Two things that will bite you

**G cannot be quantified by A260 alone.** Alexa Fluor 594 absorbs at 260 nm as well as at its own peak, so a NanoDrop reading of G overstates the DNA. IDT prints a 260 nm correction factor for the dye on the spec sheet: subtract that contribution before dividing by the extinction coefficient.

The easier route is to quantify G at **590 nm** using AF594's own extinction coefficient. The dye is attached one to one, so dye concentration is strand concentration. Since G is the one strand where accuracy matters, do both and check they agree.

**Verify the resuspension rather than trusting the nominal yield.** Delivered amounts vary, and any error in the G stock propagates straight into the parameter that sets the limit cycle. One NanoDrop reading after resuspension closes this, and it takes two minutes.

## Two conversions you must resolve first

**Bst in nM versus units.** Fujii specifies 3.7 nM. NEB sells Bst large fragment at 8,000 U/mL. There is no way to convert without NEB's specific activity for that lot. This is exactly the confusion behind the "1 percent" answer from the Paris lab and from YOKABIO: practitioners specify these enzymes as a volume fraction of the supplied stock because the molar figure is not recoverable from the datasheet. The safe route is to ask NEB technical support for the molar concentration of the M0275 lot, or adopt YOKABIO's volume-fraction approach and record it as such.

**ttRecJ concentration. Largely resolved, 25 September.** Jean-Christophe Galas wrote on 22 July that the 100 uL aliquot is **a 1/160 dilution, and that this is the standard dilution his lab uses at a final concentration of 1 percent**. So the 1 percent v/v in the lab book is not a guess borrowed from YOKABIO. It is a calibrated working dilution prepared by the group that purifies the enzyme, and it should be used exactly as written.

What is still missing is the absolute number. He gave two dilution factors but never the stock they start from, so the chain does not close:

```
in the well = neat stock / 160 / 100 = neat stock / 16,000
```

For running the reaction this does not matter. For the model it does, because the model needs a molar value. One line of email to Galas asking for the neat stock in nM or mg/mL closes it, and it can wait until after the first run.

As a plausibility check only, not as a substitute for asking: if the 1 percent is meant to land near Fujii's 32.5 nM, the neat stock would be about 520 uM, roughly 25 mg/mL for a 48 kDa protein. Concentrated, but a normal figure for a purified prep. The numbers are at least consistent.

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
| **ET SSB** | about 100 nM | **5 mg/L (5 ug/mL)** | Lab book wins, concrete figure |
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

# BENCH PROTOCOL

Every concentration and volume, in the order you do them. Reconciled with the lab book, so the numbers here are the lab book's except where noted.

## The whole thing on one page

One reaction well is always:

```
  90 uL  master mix     everything except the DNA
+ 10 uL  oligo mix      the three strands, premixed at 10x
---------
 100 uL  reaction
```

Seven stages. The first three are preparation you do once and then never again; the last four are the run itself.

| Stage | What | How often |
| --- | --- | --- |
| **1** | Component stocks: salts, buffers, dye | Once, lasts the project |
| **2** | 4x reaction buffer, 500 uL | Once per few runs |
| **3** | Oligo stocks, ending in one 10x oligo mix | **Once, then never again** |
| **4** | Master mix, 700 uL, enzymes last | Fresh every run |
| **5** | Load the plate | Every run |
| **6** | Run: 45 C, 12 h | Every run |
| **7** | Crowder layout | **Phase 2 only. Skip this for now.** |

Stages 1 to 3 are an afternoon of preparation. Once they are done, a run is stages 4 to 6 and takes about forty minutes of hands-on work.

## Stage 1: Component stocks, make once

| Stock | Make | Weigh out | Store |
| --- | --- | --- | --- |
| Tris-HCl pH 8.8 | 1.5 M, 50 mL | 9.0855 g Tris base, titrate with 1 M HCl | Room temp |
| (NH4)2SO4 | 1 M, 50 mL | 6.607 g | Room temp |
| KCl | 1 M, 50 mL | 3.7275 g | Room temp |
| NaCl | 1 M, 50 mL | 2.9222 g | Room temp |
| MgSO4 heptahydrate | 1 M, 50 mL | 12.324 g | Room temp |
| Synperonic F108 | 10 % w/v, 50 mL | 5 g, dissolve cold overnight | 4 C |
| Netropsin | 0.8 mM, 12.4 mL | all 5 mg, aliquot | -20 C, **foil** |
| BSA | 10 mg/mL, 10 mL | 0.1 g | -20 C |
| DTT | 100 mM | as supplied | -20 C, Ellis fridge stock |
| dNTP mix | 10 mM each | as supplied, **aliquot now** | -20 C |
| EvaGreen | 20x | as supplied | -20 C, **foil** |
| ET SSB | as supplied | as supplied | -20 C |

Titrate the Tris **at room temperature**. It reads about 0.55 units lower at 45 C and you must not correct for that.

Synperonic dissolves badly. Add 5 g to 40 mL cold water, cover, leave in the fridge overnight, warm to room temperature, then top up to 50 mL.

## Stage 2: 4x reaction buffer, 500 uL

Water first, EvaGreen last. Keep on ice and protect from light once the dye is in.

| # | Component | Stock | Volume | At 4x | At 1x |
| --- | --- | --- | --- | --- | --- |
| 1 | Nuclease-free water | | **112.3 uL** | | |
| 2 | Tris-HCl pH 8.8 | 1.5 M | **26.7 uL** | 80 mM | 20 mM |
| 3 | (NH4)2SO4 | 1 M | **20 uL** | 40 mM | 10 mM |
| 4 | KCl | 1 M | **20 uL** | 40 mM | 10 mM |
| 5 | NaCl | 1 M | **100 uL** | 200 mM | 50 mM |
| 6 | MgSO4 | 1 M | **16 uL** | 32 mM | 8 mM |
| 7 | dNTP mix | 10 mM each | **80 uL** | 1.6 mM each | 400 uM each |
| 8 | Synperonic F108 | 10 % | **20 uL** | 0.4 % | 0.1 % |
| 9 | Netropsin | 0.8 mM | **5 uL** | 8 uM | 2 uM |
| 10 | EvaGreen | 20x | **100 uL** | 4x | 1x |
| | **Total** | | **500 uL** | | |

## Stage 3: Oligo stocks

### Read this before the tables

The DNA goes through three tubes before it reaches a well, and it is easy to confuse them. Here is the whole path:

```
   IDT dry tube
        |  add water, once
        v
1.  TUBE STOCK, 100 uM          one tube per strand, the archive.
        |                        You touch this twice, then it lives
        |                        in the freezer.
        v
2.  WORKING DILUTION, 10 uM     N and P only. Exists purely because
        |                        1 uL is too small to pipette well.
        v
3.  OLIGO MIX, 10x              ALL THREE STRANDS IN ONE TUBE.
        |                        1000 uL, made once.
        |  10 uL per well        >>> THIS is what you pipette at
        v                        >>> the bench, and nothing else.
     the well
```

**The volumes in the tables below (16 uL, 10 uL, 30 uL) are used exactly once**, on the day you make the oligo mix. After that they never appear again. At the bench you pipette **10 uL of the finished oligo mix** into each reaction well, and that single number is the only oligo volume you ever handle again.

**Why it is called 10x.** 10 uL of the mix goes into a 100 uL well, so it gets diluted tenfold on the way in. The mix therefore has to hold every strand at ten times its final concentration. G ends up at 160 nM in the well, so the mix carries it at 1600 nM, which is 1.6 uM. Same logic for the other two.

**Why make 1000 uL when a run only needs 30.** Deliberately. It is about twenty runs' worth, and making it once means **every experiment for the rest of the project uses identically concentrated DNA**. That removes a whole class of run-to-run variation from your results at the cost of one afternoon. Split it into aliquots so you never thaw the whole thing.

### 3a. Tube stocks, 100 uM

IDT delivered amounts are confirmed, so these are exact. Let the tubes reach room temperature, spin them down before opening, then add:

| Strand | IDT delivered | Add water | Gives | Covers |
| --- | --- | --- | --- | --- |
| **G** template | 10.3 nmol | **103 uL** | 100 uM | about 640 wells |
| **N** prey | 28.6 nmol | **286 uL** | 100 uM | about 28,000 wells |
| **P** predator | 14.5 nmol | **145 uL** | 100 uM | about 4,800 wells |

Vortex, stand 15 minutes, vortex again. Template G is the limiting strand at roughly 640 wells, which is still around 60 full plates. The oligos are not a constraint.

**Aliquot the primaries before freezing them.** Split G into five tubes of about 20 uL, N and P into four or five each. Freeze-thawing a single tube repeatedly over the next two months is the realistic way to lose them, and G is both the limiting strand and the one carrying the dye.

Store all three at -20 C. **Wrap G in foil.**

### 3b. Working dilutions, 10 uM, N and P only

G is not diluted here. It goes into the mix straight from its tube stock, because 16 uL is a perfectly good volume to pipette.

| Strand | Make | How |
| --- | --- | --- |
| N | 10 uM | 10 uL of the 100 uM tube stock + 90 uL water |
| P | 10 uM | 10 uL of the 100 uM tube stock + 90 uL water |

These exist for one reason. Going straight from 100 uM would mean pipetting 1.6 uL of N and 4.8 uL of P into the mix, and a P2 at the bottom of its range is the single largest error source in this whole chain. One extra dilution step removes it.

### 3c. The oligo mix, 1000 uL at 10x

All three strands, one tube. Make this once.

| Add | From | Volume | In the mix | In the well |
| --- | --- | --- | --- | --- |
| Template G | 100 uM tube stock | **16 uL** | 1.6 uM | **160 nM** |
| Prey N | 10 uM working dilution | **10 uL** | 0.1 uM | **10 nM** |
| Predator P | 10 uM working dilution | **30 uL** | 0.3 uM | **30 nM** |
| Nuclease-free water | | **944 uL** | | |
| **Total** | | **1000 uL** | | |

Split into **5 aliquots of 200 uL**, store at -20 C wrapped in foil, and thaw one at a time. Each aliquot is 20 wells, so roughly six runs.

> **At the bench, from here on: 10 uL of this mix per reaction well.** That is the only oligo volume in the rest of the protocol. The 16, 10 and 30 above are finished with.

## Stage 4: Master mix

For **700 uL**, enough for the six master-mix wells plus generous excess. Enzymes last, straight from the freezer block, mix by gentle inversion only.

| # | Component | Stock | Per well | For 700 uL | Final |
| --- | --- | --- | --- | --- | --- |
| 1 | Nuclease-free water | | 51.25 uL | **398.6 uL** | |
| 2 | 4x reaction buffer | 4x | 25 uL | **194.4 uL** | 1x |
| 3 | BSA | 10 mg/mL | 1 uL | **7.8 uL** | 0.1 mg/mL |
| 4 | DTT | 100 mM | 4 uL | **31.1 uL** | 4 mM |
| 5 | ET SSB | 500 ug/mL | 1 uL | **7.8 uL** | 5 ug/mL |
| 6 | Bst polymerase | 8,000 U/mL | 0.75 uL | **5.8 uL** | 0.75 % v/v |
| 7 | ttRecJ | Paris aliquot, 1/160 | 1 uL | **7.8 uL** | 1 % v/v (Galas calibration) |
| 8 | Nb.BsmI | 10,000 U/mL | 6 uL | **46.7 uL** | 600 U/mL |
| | **Total** | | **90 uL** | **700 uL** | |

**Nickase check before you start.** This uses 46.7 uL of the 100 uL tube we own. The tube is 16 wells at most, so it is two runs. Do not scale this to 1800 uL: that needs 120 uL and the tube holds 100 uL.

**The enzymes bring their own crowder.** Bst, ttRecJ and Nb.BsmI are all supplied in roughly 50 percent glycerol, so these three additions put about **4 percent v/v glycerol, close to 5 percent w/v**, into every well. Glycerol is far too small to crowd the way PEG 8000 does, but it lowers water activity and raises viscosity by roughly a tenth, which is not nothing against a crowder series running 0 to 18 percent w/v. It is identical in every well, so it does not confound the comparison between crowders. It does mean the zero-crowder control is not a crowder-free reference in absolute terms, and the model's water-activity term should carry it before any absolute prediction is quoted against bench data.

## Stage 5: Load the plate

Preheat the POLARstar to **45 C at least 40 minutes beforehand**.

| Wells | Add first | Then add | What it tells you |
| --- | --- | --- | --- |
| **A1-A3** | 25 uL 4x buffer | 75 uL water | Optical baseline, plate and buffer noise |
| **B1-B3** | 90 uL master mix | 10 uL water | Enzyme autofluorescence, DNA contamination |
| **C1-C3** | 90 uL master mix | 10 uL combined oligo stock | The experiment |
| Outer ring | | water | Thermal insulation |

Seal with optical adhesive film, pressing hard along every edge. Spin the plate briefly. Load immediately.

## Stage 6: Run

- 45 C fixed, no ramps, 12 hours minimum
- Read every 2 to 5 minutes
- Green: EvaGreen, about 500 nm excitation, 520 nm emission
- Red: AF594, 584 nm excitation, 610-10 emission
- Auto-gain on wells C1-C3

**The red trace runs inverted.** Falling red fluorescence means rising prey. Do not treat that as a fault.

## Stage 7: Adding crowder, phase 2 only

The layout above has no spare volume. For a crowder series, switch to a half-and-half split so the crowder is provably the only variable:

```
50 uL   2x master mix      double strength, identical in every well
50 uL   crowder solution   0 to 36 % w/v, the only thing that varies
------
100 uL  final              everything at 1x, crowder at 0 to 18 % w/v
```

The 2x master mix is the Stage 4 recipe at half the water, with the oligos folded in at 2x: G 320 nM, N 20 nM, P 60 nM. The zero-crowder control is 50 uL of water, so baseline and crowded wells are assembled identically.

Make crowder stocks at **twice** the final w/v. Warm to dissolve, use cut tips, and make Ficoll the day before because it is very viscous.

# Before the first run

Seven things to close. The first three block the experiment; the rest block the interpretation.

- [ ] **Decide the nickase budget.** We hold one R0706S: 100 uL, 16 wells of master mix, two runs. There is no larger size, so more runs means more tubes at about 34 dollars each. This is the only consumable that genuinely limits us.
- [ ] **Ask Galas for the neat ttRecJ stock concentration**, in nM or mg/mL. Not a blocker: the 1 percent dilution is his lab's own calibration and can be used as written. This is only needed to give the model a molar number.
- [ ] **Resolve Bst units to nM**, either from NEB technical support for the M0275 lot, or by adopting a volume-fraction spec and recording it explicitly.
- [ ] **Test the AF594 signal** in a single well with labelled template alone, before committing a full run. Confirm the 610-10 filter returns usable counts off a 617 nm emitter.
- [ ] **Confirm the molecular weight of the PEG we hold.** If it is not 8000, the model's excluded-volume term needs re-deriving. Not needed for the reproduction run, which has no crowder in it.
- [ ] **Order Ficoll 400**, on a timescale, not urgently. Confirmed 25 September: we have PEG, we do not have Ficoll. Irrelevant to phase 1 but it is the comparison arm of the whole project, so it needs ordering with lead time rather than discovering late. See the note below.
- [ ] **Decide on ET SSB.** In the buffer and out of the model, or out of both. Either is defensible; the current state is neither.
- [ ] **Aliquot the dNTPs** into single-run volumes to avoid repeated freeze-thaw. The tube holds enough for two or three runs.

## Sources

- Fujii T. and Rondelez Y., *Predator-prey molecular ecosystems*, ACS Nano 2013. Circuit, sequences, buffer, enzyme concentrations, 46.5 C protocol.
- Fujii et al. supplementary information. Table S5 constants, assembly protocol, data analysis. The substantive content is here rather than in the paper.
- YOKABIO 2025 wiki, https://yokabio2025.github.io/wiki/index.html. Same circuit at BIOMOD 2025, 3rd worldwide.
- N-quenching paper. Documents which fluorophores work with nucleobase quenching: FAM, JOE, TAMRA, Alexa Fluor 594, DY-530, DY-636, DY-681.
- `crowded_mechanistic.py` and `Crowded_PredatorPrey_Mechanistic_Model.docx` in the BIOMOD repo. The seven-species model, its physical channels, and the derivation of every constant.
- FLOCK Undermind literature scan, 47 papers. Basis for the crowding coefficients and the finding that no existing paper models crowding in this oscillator.
