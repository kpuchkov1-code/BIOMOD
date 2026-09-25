# Bench protocol

*Sequential instructions: what to add, at what concentration, in what volume. This is the file to have open at the bench.*

> Part of the [wet lab documentation set](README.md). The assembled Word version of all of these is `BIOMOD_2026_Project_Brief.docx`.


---

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
