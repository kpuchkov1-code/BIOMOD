---
name: project-flux-pivot
description: "BIOMOD project pivoted from \"FLUX\" (I1-FFL via PEN toolbox + molecular crowding) to replicating the Fujii/Rondelez 2013 predator-prey oscillator with added molecular crowding"
metadata: 
  node_type: memory
  type: project
  originSessionId: f20e0f45-c077-4906-890e-bf6710924590
---

Original plan ("project FLUX"): implement an incoherent type-1 feed-forward loop (I1-FFL) using the polymerase-exonuclease-nickase (PEN) toolbox under molecular crowding (PEG 8000, Ficoll 400). Slide deck "JACK BIOMOD PRESENTATION.pdf" describes this.

**Current direction (as of 2026-05-18):** Drop the I1-FFL novelty angle. Instead replicate the Fujii & Rondelez 2013 ACS Nano predator-prey (PP) molecular ecosystem paper and introduce molecular crowding as the novel contribution.

Why: Replicating an established PP oscillator is more feasible within the competition timeline than building an unprecedented I1-FFL in PEN toolbox; crowding still provides novelty because no prior work has tuned a PEN-toolbox oscillator under crowded conditions.

How to apply: When advising on this project, anchor on the Fujii PP1 system (N1=CATTCGGCCG, P1=14 bp palindrome, G1 template, Bst pol + Nb.BsmI + ttRecJ exonuclease, 46.5 °C). The two-variable model from the Fujii SI (eqs 5–6 nondimensional, eqs 3–4 dimensional) is the starting point for any modeling work. Crowders to consider: PEG 8000 and Ficoll 400.

Related: [[user-role]]
