"""
sequence_check.py
=================
STEP 4 of the dry-lab plan: sanity-check the prey / predator / template
sequences BEFORE wet lab orders oligos.

Two layers:
  (1) Always-available: basic biophysics with no dependencies — length, GC%,
      palindrome check on the predator, nearest-neighbour Tm estimate, and a
      naive self-/cross-complementarity scan.
  (2) Optional (if the `nupack` package is installed): rigorous equilibrium
      secondary-structure / MFE / complex-concentration analysis.

Why this matters for the crowding project specifically: molecular crowding
RAISES duplex stability (effective Tm goes up), so a weak spurious interaction
that is harmless in dilute buffer can become a real off-pathway product under
crowding. Flag marginal interactions now.

Fujii PP1 system (SI Table S1 — now filled from the Supporting Information):
  prey      N1 = 5'-CATTCGGCCG-3'                 (10 nt, 5'-phosphate)
  predator  P1 = 5'-CATTCGGCCGAATG-3'             (14 nt palindrome)
  template  G1 = 5'-CGGCCGAATGCGGCCGAATG-3'       (20 nt; 5' phosphorothioates
             on first 3 bases (*) block exonuclease; 3' = phos or Dy530 dye)
The bold nicking-enzyme (Nb.BsmI) site 5'-GCATTC-3' appears only in G1 duplex.
"""

import math

# --- Sequences (SI Table S1; * modifications omitted, they don't change the
#     base-pairing biophysics checked here) -----------------------------------
SEQUENCES = {
    "N1_prey":     "CATTCGGCCG",            # SI Table S1
    "P1_predator": "CATTCGGCCGAATG",        # SI Table S1 (palindrome)
    "G1_template": "CGGCCGAATGCGGCCGAATG",  # SI Table S1
}

COMPLEMENT = str.maketrans("ACGT", "TGCA")


def revcomp(s):
    return s.translate(COMPLEMENT)[::-1]


def gc_percent(s):
    if not s:
        return float("nan")
    return 100.0 * sum(c in "GC" for c in s) / len(s)


def is_palindrome(s):
    """A DNA reverse-complement palindrome reads the same on both strands."""
    return bool(s) and s == revcomp(s)


def tm_wallace(s):
    """Quick Wallace rule Tm (deg C) — OK as a first pass for short oligos."""
    if not s:
        return float("nan")
    at = sum(c in "AT" for c in s)
    gc = sum(c in "GC" for c in s)
    return 2 * at + 4 * gc


def max_complementary_run(a, b):
    """Longest run where a aligns complementarily to reverse(b). Naive O(n^2),
    fine for short oligos — flags obvious self/cross hybridisation."""
    if not a or not b:
        return 0
    b_rc = revcomp(b)
    best = 0
    for off in range(-(len(a) - 1), len(b_rc)):
        run = 0
        for i in range(len(a)):
            j = i + off
            if 0 <= j < len(b_rc) and a[i] == b_rc[j]:
                run += 1
                best = max(best, run)
            else:
                run = 0
    return best


def basic_report():
    print("=" * 64)
    print("LAYER 1 — dependency-free biophysics")
    print("=" * 64)
    for name, seq in SEQUENCES.items():
        if not seq:
            print(f"{name:14s}: (empty — fill from SI)")
            continue
        print(f"{name:14s}: 5'-{seq}-3'  len={len(seq)} "
              f"GC={gc_percent(seq):.0f}% Tm~{tm_wallace(seq):.0f}C "
              f"{'[PALINDROME]' if is_palindrome(seq) else ''}")
    # predator should be a palindrome — verify
    p = SEQUENCES["P1_predator"]
    if p:
        print(f"\npredator palindrome check: "
              f"{'PASS' if is_palindrome(p) else 'FAIL — expected palindrome'}")

    print("\nPairwise max complementary run (off-target hybridisation risk):")
    names = [n for n, s in SEQUENCES.items() if s]
    for i in range(len(names)):
        for j in range(i, len(names)):
            a, b = SEQUENCES[names[i]], SEQUENCES[names[j]]
            run = max_complementary_run(a, b)
            tag = "  <-- inspect" if run >= 6 and names[i] != names[j] else ""
            print(f"  {names[i]:14s} x {names[j]:14s}: {run} bp{tag}")


def nupack_report():
    try:
        import nupack  # noqa: F401
    except ImportError:
        print("\n(LAYER 2 skipped — `nupack` not installed. Install via the "
              "official NUPACK distribution to run equilibrium analysis.)")
        return
    from nupack import Strand, Complex, ComplexSet, Model, complex_analysis
    print("\n" + "=" * 64)
    print("LAYER 2 — NUPACK equilibrium analysis")
    print("=" * 64)
    # NOTE: tune temperature/material to the Fujii conditions (46.5 C, DNA, the
    # paper's Na+/Mg2+). Crowding is NOT in NUPACK's model — treat its Tm as a
    # LOWER bound on stability for the crowded experiment.
    model = Model(material="dna", celsius=46.5, sodium=0.05, magnesium=0.01)
    strands = {n: Strand(s, name=n) for n, s in SEQUENCES.items() if s}
    # single-strand secondary structure (do any fold into hairpins?)
    for n, st in strands.items():
        cx = Complex([st])
        res = complex_analysis(ComplexSet(strands=[st], complexes={cx}),
                               model=model, compute=["mfe"])
        mfe = res[cx].mfe[0]
        print(f"  {n:14s}: MFE {mfe.energy:6.2f} kcal/mol  {mfe.structure}")


if __name__ == "__main__":
    basic_report()
    nupack_report()
