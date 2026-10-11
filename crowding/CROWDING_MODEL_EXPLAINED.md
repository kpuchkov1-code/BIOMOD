# The crowding model, explained simply

*Companion to `Crowded_PredatorPrey_Mechanistic_Model.docx` (the full technical write-up). This version skips the equations-as-proof style and just walks through the reasoning. Updated 2026-07-27 for the confirmed setup: exonuclease = ttRecJ, plate reader ceiling = 45°C.*

## 1. The system we're perturbing

The Fujii-Rondelez DNA predator-prey oscillator is a test tube reaction with two short synthetic DNA strands acting like a predator and prey population:

- **Prey (N)** copies itself off a template strand (G), the way a rabbit population grows.
- **Predator (P)** copies itself by consuming prey — literally uses N as raw material to make more of itself.
- An **exonuclease** (ttRecJ, in your setup) chews up both N and P over time, playing the role of natural death.

Three enzymes run this: a polymerase (extends strands), a nickase (cuts them at the right spot so they detach and can be reused as templates), and the exonuclease (degrades them). Get the rates right and, like a real predator-prey system, the populations of N and P rise and fall in a repeating cycle — about 90 minutes per cycle in dilute buffer.

## 2. Why crowding is the interesting question

That 90-minute cycle was measured in ordinary dilute buffer. A real cell interior is nothing like dilute buffer — it's packed with proteins, RNA, sugars, at 20-30% of the volume taken up by "stuff." That packing is called **macromolecular crowding**, and it's known to change how molecules bind to each other and how fast enzymes work, without changing the chemistry itself. Nobody had modeled what crowding does to *this specific* oscillator, so that's the gap the model fills. PEG 8000 and Ficoll 400 are the two standard synthetic crowding agents used to mimic this in the lab, and they're chemically quite different from each other, which turns out to matter a lot.

## 3. The wrong way to model it (and why it was rejected)

The lazy version: take the oscillator's four main rate constants and just multiply each by some fitted "crowding goes here" number until the output looks plausible. That was tried first (kept in the repo as `crowded_model.py`, labeled rejected) and rejected for a simple reason: it's curve-fitting the conclusion. It can't explain *why* PEG and Ficoll would behave differently, and every constant is fit independently even though the same physical crowding effect is really acting on all of them at once.

## 4. The actual approach: break it into real steps, then let physics act once

The real trick is that each of those four lumped rate constants is secretly hiding several separate physical events:

1. Two strands finding each other and sticking together (a binding/unbinding equilibrium)
2. An enzyme grabbing hold of a strand (another binding step)
3. The enzyme actually doing its chemistry (the true "rate" step)
4. The whole process being throttled by how fast molecules can diffuse and bump into each other in a crowded soup

The model writes out all of these explicitly, as a network of 7 tracked quantities: free prey (N), free predator (P), free template (G), and four "stuck together" complexes (prey+template, prey+predator, prey+enzyme, predator+enzyme). Then it defines **five physical effects that crowding produces**, and every one of the elementary steps above is only allowed to feel crowding through those five effects — nothing is fit separately per-step. That's the whole point: one set of physics, many downstream consequences, instead of many independent fudge factors.

The five effects, in plain terms:

- **"There's less room" (excluded volume).** If molecule A and B are floating in a crowded soup and could either stay separate or stick together into one compact blob, the crowded soup actually *prefers* the compact blob, because two separate objects taking up space cost the soup more room than one merged object. This is pure geometry — it doesn't care about chemistry, only size and shape. This is the textbook scaled-particle-theory effect, and it's the one most people think of first when they hear "crowding."
- **"PEG and Ficoll aren't just different-sized balls, they're different chemicals" (the enthalpic effect).** Effect #1 treats every crowder as a featureless hard sphere. But real chemistry papers (Sung & Nesbitt) show PEG is a fairly "polite," near-neutral crowder toward DNA, while Ficoll actively prefers to stay away from DNA surfaces — which, counter-intuitively, makes Ficoll extra good at stabilizing the compact "stuck together" state, on top of its geometric effect. This channel is what actually makes PEG and Ficoll behave differently at the same concentration, rather than differing only because Ficoll happens to be a bigger molecule.
- **"Crowding agents soak up water" (water activity).** PEG in particular is a strong osmotic agent — it competes hard for water molecules. When two DNA strands zip together they release a couple of water molecules to the surroundings; if water is scarce (because PEG is hogging it), that release is more favorable, so PEG nudges strands toward sticking together through this separate, chemistry-specific channel.
- **"Everything moves slower in syrup" (viscosity).** Before two molecules can react they have to physically collide, and collision rate depends on how fast they diffuse. Crowding thickens the effective local viscosity, so it slows down every diffusion-limited encounter — including binding steps.
- **"Enzymes speed up or slow down depending on what kind they are."** This one isn't derived from geometry — it's taken straight from published enzyme experiments. Polymerases and nickases have been measured to work *faster* under crowding (better binding/processivity). Exonucleases like ttRecJ have been measured to work *slower* under crowding (Sasaki's data on a related E. coli exonuclease). These get folded in as literature numbers because you can't derive "this specific enzyme's chemistry changed" from pure physics — you have to measure it or borrow the closest measured analog.

`★ Insight ─────────────────────────────────────`
The reason this design matters scientifically: the same excluded-volume term that stabilizes a DNA duplex also, automatically, tightens enzyme-substrate binding, because it's the *same equation* applied to a different pair of molecules with different sizes. And the same viscosity term that slows the polymerase also slows the exonuclease. Nothing is free to move independently — if you change the underlying crowder size or chemistry, every downstream rate shifts together, consistently. That's what makes it a mechanistic model instead of a curve fit: the constraints come from physics, not from wanting a particular answer.
`─────────────────────────────────────────────────`

## 5. Calibrating it to match reality

Before adding any crowding at all, the model has to reproduce the known dilute (no-crowder) behavior — the real, published 90-minute cycle. Two small corrections were needed to get there:

- A uniform ~20% slowdown on the catalytic rates, because the simplified textbook equations for this oscillator secretly assume enzymes react instantly compared to binding, while the fuller step-by-step version here tracks the fact that some prey and predator are temporarily "parked" in bound complexes and not available to react. Accounting for that parked population requires slightly gentler rates to land on the same 90-minute period.
- A tiny constant trickle of new prey and predator ("leak"), representing real background activity where the polymerase occasionally extends a strand without a proper template. This isn't invented — it's a known minor behavior of this enzyme system — but it also serves a practical purpose: without it, the simulated population dips can mathematically get stuck at exactly zero, which is numerically fragile and not realistic.

With those two corrections, the no-crowding version of the model reproduces the published period and amplitude closely (see the numbers printed when the script runs).

## 6. The result

Once crowding is switched on, both PEG and Ficoll shorten the period and shrink the swing between predator highs and lows — that part is expected and mild. The interesting part is what happens as you keep increasing the concentration:

- **PEG 8000** eventually crosses a threshold (around 10-12% w/v) where the oscillation stops entirely and the system just settles to a flat, non-oscillating state. In math terms, this is called crossing a Hopf bifurcation.
- **Ficoll 400** keeps oscillating all the way up to the highest concentrations tested (past 16-18% w/v) — it never hits that same wall.

That divergence — PEG kills the oscillation, Ficoll doesn't, at the *same* volume fraction — is the actual novel, testable prediction. It only shows up because the model gives PEG and Ficoll different chemistry (channels 2 and 3 above), not just different sizes.

## 7. What your two updates change

**Exonuclease = ttRecJ (confirmed).** Good news: this is actually the *simpler* outcome. All of the model's original numbers (how much exonuclease is around, how it competes between prey and predator) were derived from Fujii's original published data, which used ttRecJ. The model previously had this set to a placeholder alternative enzyme "in case the team switched," which would have needed extra unproven re-mapping. Confirming ttRecJ removes that uncertainty and the model's constants apply directly, no re-derivation needed. It's also thermostable at your operating temperature, so it won't lose activity over a long run — an assumption the model leans on (enzyme amount stays constant throughout) is now on solid ground.

**Plate reader ceiling = 45°C (confirmed).** This one's a genuine, if small, mismatch: the strands in this oscillator are chemically designed to work best around 46°C, and the published dilute baseline the model calibrates against was measured at 46.5°C. Running at 45°C is about 1.5°C below that design point. Practically, this mostly matters for the *baseline* dilute cycle (how tightly strands stick together and exactly how fast the enzymes turn over both shift a little with temperature) — it does **not** meaningfully affect the crowding physics itself, because the crowding effects in the model are written in a form that's naturally temperature-independent (they only depend on how much stuff is excluding volume, not on the ambient temperature). So: the PEG-vs-Ficoll story and the Hopf-off concentration prediction should hold up fine at 45°C. What could drift slightly is the exact period/amplitude numbers of the *un-crowded* baseline. If your actual 45°C dilute run comes out noticeably off from ~90 minutes, that's the piece to re-tune first — not the crowding terms.

Net effect of both updates on the model's headline prediction: essentially nothing changes. Running the updated model confirms the dilute cycle is still ~90 minutes and the PEG Hopf-off point is still right around 10% w/v.

## 8. Where the model is honestly limited

- It treats the test tube as perfectly well-mixed. Real crowding also creates local pockets and traps molecules aren't as free to roam — that needs a fundamentally different kind of model (spatial/particle-based) and isn't something this style of model can fix.
- The Mg²⁺ buffer ions aren't accounted for (deliberately switched off — the only available formula was for the wrong kind of ion, and turning it on would have been worse than leaving it out).
- The exonuclease's crowding sensitivity is borrowed from a related but different enzyme's published data, since ttRecJ itself hasn't been measured under crowding yet — that's the single most valuable wet-lab measurement to do next, since it directly sets where the PEG cutoff lands.
- All the Ficoll 400 numbers are extrapolated, since no paper in the literature scan measured Ficoll directly on a system like this.

None of these change the shape of the prediction — they're exactly the kind of gaps a wet-lab measurement is meant to close.
