# What goes in each well

*Every component, what it does, and the volume that delivers it.*

> Part of the [wet lab documentation set](README.md). The assembled Word version of all of these is `BIOMOD_2026_Project_Brief.docx`.


---

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
