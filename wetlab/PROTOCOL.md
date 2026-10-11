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
| Netropsin | 0.8 mM, 12.4 mL | all 5 mg, 12 aliquots, steps below | -20 C, **foil** |
| BSA | 10 mg/mL, 10 mL | 0.1 g | -20 C |
| DTT | 100 mM | as supplied | -20 C, Ellis fridge stock |
| dNTP mix | 10 mM each | as supplied, **aliquot now** | -20 C |
| EvaGreen | 20x | as supplied | -20 C, **foil** |
| ET SSB | as supplied | as supplied | -20 C |

Titrate the Tris **at room temperature**. It reads about 0.55 units lower at 45 C and you must not correct for that.

Synperonic dissolves badly. Add 5 g to 40 mL cold water, cover, leave in the fridge overnight, warm to room temperature, then top up to 50 mL.

### Netropsin, 0.8 mM, 12 aliquots

Read the vial label before you weigh anything. The 12.4 mL below assumes **netropsin
dihydrochloride, MW 503.4**, which is what Sigma ships as N6635. A different salt form
has a different molecular weight and needs a different volume, so recompute it rather
than trusting the number here.

Netropsin is light-sensitive and it is a DNA binder. Gloves, and keep it out of the light
from the moment the vial is open.

1. **Let the vial reach room temperature** before opening it, then spin it down briefly so
   none of the powder is sitting in the cap. It is 5 mg in total and you cannot afford to
   lose any of it on a lid.
2. **Dissolve in the vial, not in a fresh tube.** Add 1 mL of nuclease-free water directly
   to the supplied vial and pipette gently to dissolve. Transferring dry powder loses
   material on the tube wall; dissolving in place does not.
3. **Rinse the vial twice** with 1 mL of water each time, carrying each rinse into a 15 mL
   foil-wrapped tube along with the first millilitre. This is the step that decides whether
   you get 0.8 mM or something 10 percent lower.
4. **Top up to 12.4 mL** with nuclease-free water. That gives 0.8 mM. Invert to mix, and do
   not vortex hard.
5. **Split into 12 aliquots of about 1 mL** in amber or foil-wrapped tubes. Label each one
   `Netropsin 0.8 mM` with the date.
6. **Store at -20 C, wrapped in foil.** Thaw one tube at a time and keep the other eleven
   untouched.

Each 500 uL batch of 4x buffer takes 5 uL, so a single 1 mL aliquot covers far more buffer
than this project will ever make. The 12 tubes are a freeze-thaw safeguard, not a supply
calculation: the point is that you never thaw the whole 12.4 mL.

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

**Store the finished buffer at -20 C, wrapped in foil, split into 5 aliquots of 100 uL.**
Each aliquot is 4 wells. Three of the ten components do not tolerate being left in the
fridge or repeatedly thawed: the dNTPs degrade slowly, and both EvaGreen and netropsin
are light-sensitive. Aliquoting means a run thaws 100 uL rather than putting the whole
batch through another freeze-thaw cycle.

**The dNTPs cap how many batches you can make.** One batch takes 80 uL of the 200 uL
dNTP tube, so the tube is 2.5 batches, about 50 wells. Reordering dNTPs is the quiet
prerequisite for a third batch.

## Stage 3: Oligo stocks

One afternoon, nineteen steps, done once for the whole project. The DNA passes through
three tubes before it reaches a well:

```
   IDT dry tube
        |  add water, once
        v
   TUBE STOCK, 100 uM           one per strand. Made and drawn from on
        |                       one afternoon, then it lives in the freezer.
        v
   WORKING DILUTION, 10 uM      N and P only. Exists purely because 1.6 uL
        |                       is too small to pipette accurately.
        v
   OLIGO MIX, 1000 uL at 10x    ALL THREE STRANDS IN ONE TUBE.
        |                       Made once. About twenty runs.
        |  10 uL per well       >>> THIS is what you pipette at the bench,
        v                       >>> and nothing else.
      the well
```

### Before you start

Out on the bench: about **1.7 mL of nuclease-free water** decanted into a working tube,
fresh pre-racked tips, a minifuge, a vortex, and roughly fifteen labelled 1.5 mL tubes.
Read the note on tips and water at the end of this stage first if nobody has.

Two rules that hold throughout:

- **A fresh tip for every strand, every time.** The stocks are 100 uM and the well needs
  10 to 160 nM, so a trace of one strand in another's tube is a large contamination.
- **Only one oligo tube open at a time.** Three open tubes of 100 uM DNA side by side is
  how strands end up in each other.

**Do not freeze anything until step 19.** Everything the dilutions and the mix need is
withdrawn from the primaries on the same afternoon they are made, so the primaries are
frozen once, at the end, and never thawed again unless you remake the mix.

| Strand | IDT delivered | Water to add | Gives | Covers |
| --- | --- | --- | --- | --- |
| **N** prey | 28.6 nmol | **286 uL** | 100 uM | about 28,000 wells |
| **P** predator | 14.5 nmol | **145 uL** | 100 uM | about 4,800 wells |
| **G** template | 10.3 nmol | **103 uL** | 100 uM | about 640 wells |

### The nineteen steps

1. **Bring all three IDT tubes to room temperature** before opening anything. A cold tube
   pulls condensation out of the air and onto the dried pellet.
2. **Spin all three down**, a few seconds in a minifuge or 30 seconds at 3,000 g. IDT ships
   a dried film that is often loose in the cap and is invisible. Opening an unspun tube is
   the commonest way to lose part of a strand before you start.
3. **N first: add 286 uL of water** onto the pellet rather than down the wall. Cap, vortex
   20 to 30 seconds. N is the strand to make your mistakes on, at 28,000 wells.
4. **Then P: add 145 uL.** Cap, vortex 20 to 30 seconds.
5. **Then G: add 103 uL.** Cap, vortex 20 to 30 seconds, and drape foil over it. G is both
   the limiting strand and the one carrying the dye, so it goes last, once your hands know
   the sequence.
6. **Stand all three for 15 minutes** at room temperature. The strands are 10 to 22 nt and
   need no heating. Do not warm G.
7. **Vortex each again, then spin each briefly** to bring droplets down from the cap and
   walls. That spin is part of the measurement: volume left in the cap is strand missing
   from your concentration. All three are now 100 uM.
8. **Withdraw 16 uL of G** into a fresh tube and label it `G for mix`. Fresh tip.
9. **Withdraw 10 uL of N** into a fresh tube. Fresh tip.
10. **Withdraw 10 uL of P** into a fresh tube. Fresh tip.
11. **Add 90 uL of water to the 10 uL of N**, giving 100 uL at 10 uM. Vortex.
12. **Add 90 uL of water to the 10 uL of P**, giving 100 uL at 10 uM. Vortex.
13. **Put 944 uL of water into a fresh 1.5 mL tube.** This becomes the oligo mix, so water
    goes in first.
14. **Add the three strands to it:** 16 uL of G from step 8, 10 uL of the N dilution, and
    30 uL of the P dilution. That is 1000 uL total.
15. **Vortex the mix, spin briefly, and keep it covered.** This tube is now the only oligo
    volume in the rest of the protocol.
16. **Split the mix into 5 aliquots of 200 uL.** Each is 20 wells, about six runs.
17. **Split what is left of G, about 87 uL, into 4 or 5 tubes of roughly 20 uL.** One
    aliquot is exactly one future mix, so no G tube is ever refrozen.
18. **Put the N and P primaries into one tube each,** or two if you want insurance against
    dropping one. The leftover 10 uM dilutions go into one tube each as well.
19. **Label every tube** with strand, concentration and date, label the box too, and
    **freeze everything at -20 C.** Put the G aliquots and the mix in one opaque box.

### The tubes you end up with

Have about **sixteen 1.5 mL tubes** labelled before you start. Thirteen to fifteen of them
go into the freezer at step 19; the rest are working tubes you throw away the same day.

| Tube | Contents | Concentration | Volume | Write on it | Store |
| --- | --- | --- | --- | --- | --- |
| 1 | Water, decanted to work from | | ~1.7 mL | `NF water` | Discard |
| 2 | G, resuspended, for the mix | 100 uM | 16 uL | `G for mix` | Used up at step 14 |
| 3 | Mixing tube for the oligo mix | 10x | 1000 uL | `OLIGO MIX 10x <date>` | Emptied at step 16 |
| 4 to 8 | **Oligo mix aliquots** | **10x** | **5 x 200 uL** | `OLIGO MIX 10x <date> 1/5` to `5/5` | **-20 C, opaque box** |
| 9 to 12 | **G primary aliquots** | **100 uM** | **4 x ~22 uL** | `G 100uM <date>` | **-20 C, foil or opaque box** |
| 13 | **N primary** | **100 uM** | **276 uL** | `N 100uM <date>` | **-20 C** |
| 14 | **P primary** | **100 uM** | **135 uL** | `P 100uM <date>` | **-20 C** |
| 15 | N working dilution, leftover | 10 uM | 90 uL | `N 10uM <date>` | -20 C |
| 16 | P working dilution, leftover | 10 uM | 70 uL | `P 10uM <date>` | -20 C |

Tubes 13 and 14 can simply be the original IDT tubes, relabelled. Split them in two if you
want insurance against dropping one. Tube 3 can be one of the five mix aliquots if you would
rather not use a sixth tube.

**Write the concentration on every tube, not just the strand.** The one label that can ruin
a run is `N`, because there are two N tubes in the freezer at 100 uM and 10 uM and they
differ tenfold. The same goes for P. A tube marked only with a strand letter is an ambiguous
tube, and the ambiguity surfaces three weeks later when somebody else is at the bench.

Label the box as well as the tubes. Marker rubs off a frosted cap in a gloved hand.

### The volumes, as a table

| Add | From | Volume | In the mix | In the well |
| --- | --- | --- | --- | --- |
| Template G | 100 uM tube stock | **16 uL** | 1.6 uM | **160 nM** |
| Prey N | 10 uM working dilution | **10 uL** | 0.1 uM | **10 nM** |
| Predator P | 10 uM working dilution | **30 uL** | 0.3 uM | **30 nM** |
| Nuclease-free water | | **944 uL** | | |
| **Total** | | **1000 uL** | | |

> **At the bench, from here on: 10 uL of this mix per reaction well.** That is the only
> oligo volume in the rest of the protocol. The 16, 10 and 30 above are finished with.

### Why it is done this way

**Why the mix is called 10x.** 10 uL goes into a 100 uL well, so it is diluted tenfold on
the way in and has to carry every strand at ten times its final concentration. G ends up at
160 nM in the well, so the mix holds it at 1600 nM.

**Why make 1000 uL when a run needs 30.** It is about twenty runs, and making it once means
every experiment for the rest of the project uses identically concentrated DNA. That
removes a whole class of run-to-run variation for the cost of one afternoon.

**Why N and P get diluted but G does not.** Going straight from 100 uM would mean pipetting
1.6 uL of N and 4.8 uL of P, and a P2 at the bottom of its range is the single largest error
source in this chain. G's 16 uL is a perfectly good volume, so G skips the step. Both
dilutions are single-use intermediates, not stocks: the mix takes 10 and 30 uL, so 90 and
70 uL are left over. Keep them, but they are not precious.

**Why aliquot sizes differ.** Aliquoting buys one thing, which is not thawing a tube you
are not using. So the mix, which you open every run, is split five ways; the N and P
primaries, which you may never open again, are not. Splitting everything five ways is five
times the labelling for no benefit.

**Why G is the exception.** Not freeze-thaw. Template concentration is the model's main
bifurcation parameter, there is an unresolved 140 versus 160 nM discrepancy against the
model, and a G titration would mean several separate mixes and so several separate
withdrawals. Matching one 20 uL aliquot to one mix means each of those costs a fresh tube
rather than a thaw.

**What the premade mix costs you.** It fixes the N:P:G ratio. That is the right trade for a
crowding study, where crowder percentage is the only thing varying between wells. But
varying one strand independently later means a new mix, not an adjustment to this one.

**On foil.** AF594 is one of the more photostable dyes and foil is not strictly needed for a
15 minute stand under room lighting. Keep G off a sunlit bench, and drape foil over it
anyway so nobody has to make the judgement call on the afternoon it gets left out for three
hours. The photobleaching that actually threatens this experiment happens in the well, at
160 nM, under the reader's excitation across a 12 hour run.

**Do not quantify the strands.** IDT's delivered nmol is reliable, and on G the AF594
absorbance contaminates an A260 reading, so a nanodrop number would be worse than trusting
the label.

### A note on tips and water

**Sterile and nuclease-free are two different certifications and you want the second one.**
Sterility means no viable microbes, which this reaction does not care about. Nuclease-free
means certified free of DNase and RNase, which it does. Autoclaving delivers the first and
not reliably the second, so an autoclaved tip is not automatically a safe tip.

In practice: fresh tips from a sealed, pre-racked box are fine, and almost all pre-racked
tips from the major brands are certified both. Loose tips from an open bulk bag are
certified neither, and a bag that people have had their hands in is the one thing to avoid.
Filter tips are worth using for the 100 uM stocks, to keep aerosol out of the pipette
barrel.

**The bigger risk is not nucleases, it is the strands contaminating each other,** which is
why the fresh-tip rule above is absolute rather than advisory. A trace of P in the N tube
would change the circuit's dynamics and look like a failed experiment rather than a
pipetting error.

**Decant the water** you are going to use into a separate tube and work from that, rather
than putting a tip into the stock bottle repeatedly. One careless tip contaminates the
bottle, and nothing afterwards will tell you it happened.

Milli-Q is acceptable for the netropsin stock, which is a small molecule nucleases cannot
touch. Use certified nuclease-free water here in Stage 3, where the strands are DNA sitting
in a freezer for two months, and remember that G's phosphorothioate linkages protect it
from exonucleases only. An endonuclease would still cut it.

**Total water for Stage 3: about 1,658 uL,** or 1.7 mL, being 534 uL for the tube stocks,
180 uL for the working dilutions and 944 uL for the mix. Buy 5 mL and there is room to
remake the mix once.


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
- [ ] **Aliquot the dNTPs** into single-run volumes to avoid repeated freeze-thaw. The tube holds enough for two or three runs.

## Sources

- Fujii T. and Rondelez Y., *Predator-prey molecular ecosystems*, ACS Nano 2013. Circuit, sequences, buffer, enzyme concentrations, 46.5 C protocol.
- Fujii et al. supplementary information. Table S5 constants, assembly protocol, data analysis. The substantive content is here rather than in the paper.
- YOKABIO 2025 wiki, https://yokabio2025.github.io/wiki/index.html. Same circuit at BIOMOD 2025, 3rd worldwide.
- N-quenching paper. Documents which fluorophores work with nucleobase quenching: FAM, JOE, TAMRA, Alexa Fluor 594, DY-530, DY-636, DY-681.
- `crowded_mechanistic.py` and `Crowded_PredatorPrey_Mechanistic_Model.docx` in the BIOMOD repo. The seven-species model, its physical channels, and the derivation of every constant.
- FLOCK Undermind literature scan, 47 papers. Basis for the crowding coefficients and the finding that no existing paper models crowding in this oscillator.
