---
name: project-fujii-reactome
description: "Teammate-produced 'Fujii et al. reactome' — a detailed reaction-network map of the predator-prey system, organized into Prey Growth / Predation / Death / Fluorescence Interference modules; the species+reaction basis for the dry-lab ODE model"
metadata: 
  node_type: memory
  type: project
  originSessionId: dd312f27-a868-4a24-8cfa-b58e3c2af24e
---

A teammate produced a one-page diagram titled **"Fujii et al. reactome"** (file: `C:\Users\KPuch\Downloads\Fujii et al. reactome (1).pdf`). It is the mechanistic species/reaction map underpinning the dry-lab model of the Fujii & Rondelez predator-prey oscillator (see [[project-flux-pivot]]).

Structure — four color-coded functional modules:
- **PREY GROWTH** (green): autocatalytic N replication on G template — `N-G(o)` → `N-G(o)-Pol` → `-N-G(o)-N-`, then `Nic` nicking releases new N.
- **PREDATION** (red): P grows on prey — `N-P(o)` → `N-P(o)-Pol` → `P(o)-P(o)`.
- **DEATH** (grey): Exo (ttRecJ) degradation — `N-Exo`, `P(o)-Exo` decay arm for N and P.
- **FLUORESCENCE INTERFERENCE** (purple): reporter-confounding species (`P-G`, `G(sc/o)-N`) affecting green/yellow readout.

Key conventions:
- Conformational states tracked explicitly: o = open, c = closed (hairpin), sc = semi-closed — because enzyme activity is conformation-dependent.
- Species color/border = fluorescence behavior: black = none/weak, green border = strong green only, yellow border = strong yellow.
- Reactions labeled with module-prefixed IDs (Pol.11, Nic.12, Exo.21, BD.xx, B.xx, D.16).

Modeling assumptions stated on the diagram: intermediate hairpin states not explicitly modeled (assumed much less stable); `-N-G-N-` never dissociates into G + N-N (too enthalpically costly); templates well-protected so no G degraded by Exo; dissociations of hairpinable species default to hairpin product; complexes grouped into single species unless conformation matters for enzyme activity.

How to apply: This is the canonical species+reaction list to compile into the ODE system. When doing dry-lab modeling, reconcile this reactome with the two-variable nondimensional model from the Fujii SI (eqs 5-6) noted in [[project-flux-pivot]].

Related: [[project-flux-pivot]], [[user-role]]
