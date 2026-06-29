"""
generate_mechanistic_report.py
==============================
Builds the Word document for the MECHANISTIC crowded predator-prey model
(crowded_mechanistic.py): explicit reaction network + crowding physics on every
elementary step. Run after crowded_mechanistic.py (consumes its two figures).
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os
import latex2mathml.converter as _l2m
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
AMBER = RGBColor(0xC4, 0x78, 0x28)
GREY = RGBColor(0x55, 0x55, 0x55)
MONO, SERIF = "Consolas", "Georgia"

# --- native Word equation support (LaTeX -> MathML -> OMML) -------------------
# Office ships an XSLT (MML2OMML.XSL) that converts MathML into the Office Math
# markup (OMML) Word renders natively. We convert each LaTeX string to MathML
# with latex2mathml, transform it, and drop the resulting <m:oMath> element
# straight into a paragraph -- a real, editable Word equation, not an image.
_XSL_CANDIDATES = [
    r"C:/Program Files/Microsoft Office/root/Office16/MML2OMML.XSL",
    r"C:/Program Files (x86)/Microsoft Office/root/Office16/MML2OMML.XSL",
    r"C:/Program Files/Microsoft Office/Office16/MML2OMML.XSL",
]
_XSL_PATH = next((p for p in _XSL_CANDIDATES if os.path.exists(p)), None)
_OMML_XSLT = etree.XSLT(etree.parse(_XSL_PATH)) if _XSL_PATH else None


def _latex_to_omml(latex):
    mathml = _l2m.convert(latex)
    return _OMML_XSLT(etree.fromstring(mathml)).getroot()


doc = Document()
doc.styles["Normal"].font.name = SERIF
doc.styles["Normal"].font.size = Pt(10.5)


def heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = NAVY if level <= 2 else AMBER
        run.font.name = SERIF
    return h


def body(text, italic=False, size=10.5, color=None, align=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    r.italic = italic
    r.font.size = Pt(size)
    r.font.name = SERIF
    if color is not None:
        r.font.color.rgb = color
    return p


def omath(latex, center=True):
    """Insert a native, editable Word equation from a LaTeX string."""
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(5)
    if _OMML_XSLT is not None:
        p._p.append(_latex_to_omml(latex))
    else:                                   # graceful fallback if Office XSL absent
        r = p.add_run(latex); r.font.name = MONO; r.font.size = Pt(9.5)
    return p


def scheme(text):
    """A reaction scheme (arrows, not an equation): styled monospace block."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.font.name = MONO
    r.font.size = Pt(9.5)
    r.font.color.rgb = NAVY
    return p


def bullet(text, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_lead:
        r = p.add_run(bold_lead); r.bold = True
        r.font.name = SERIF; r.font.size = Pt(10.5)
    r2 = p.add_run(text); r2.font.name = SERIF; r2.font.size = Pt(10.5)
    return p


def caveat(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    r = p.add_run("⚠  " + text)
    r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = AMBER
    return p


def make_table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        c = t.rows[0].cells[j]; c.text = ""
        run = c.paragraphs[0].add_run(h)
        run.bold = True; run.font.size = Pt(9); run.font.name = SERIF
    for row in rows:
        cells = t.add_row().cells
        for j, val in enumerate(row):
            cells[j].text = ""
            run = cells[j].paragraphs[0].add_run(str(val))
            run.font.size = Pt(8.5); run.font.name = SERIF
    if widths:
        for j, w in enumerate(widths):
            for r in t.rows:
                r.cells[j].width = Inches(w)
    return t


# ---- TITLE -------------------------------------------------------------------
title = doc.add_paragraph(); title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("A Mechanistic Model of Molecular Crowding in the\n"
                  "DNA Predator–Prey Oscillator")
r.bold = True; r.font.size = Pt(19); r.font.name = SERIF; r.font.color.rgb = NAVY
sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("Bottom-up reaction network with crowding physics on every "
                "elementary step — PEG 8000 vs Ficoll 400 in the "
                "Fujii–Rondelez PEN circuit")
r.italic = True; r.font.size = Pt(12); r.font.name = SERIF; r.font.color.rgb = GREY
m = doc.add_paragraph(); m.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = m.add_run("BIOMOD dry-lab · Step 3 · mechanistic model + implementation "
              "(crowded_mechanistic.py)")
r.font.size = Pt(10); r.font.color.rgb = GREY
doc.add_paragraph()

# ---- 1 EXEC ------------------------------------------------------------------
heading("1.  What this model is, and why it is built this way", 1)
body("This is a mechanistic, bottom-up model of how macromolecular crowding "
     "reshapes our DNA predator–prey oscillator. It is deliberately NOT the "
     "earlier approach of multiplying the four lumped rate constants by fitted "
     "factors. The lumped constants k1, k2, kN, kP each hide several distinct "
     "physical steps — strand hybridization (an equilibrium), enzyme–"
     "substrate binding (a Michaelis constant), catalytic turnover, and a "
     "diffusional encounter. Crowding does not act on the lump; it acts on each "
     "of those elementary steps, through physics that is shared across the whole "
     "circuit.")
body("So the model does three things differently:")
bullet("free prey N, free predator P, free template G, and the four complexes "
       "(N·G, N·P, N·Exo, P·Exo), with enzyme conservation. "
       "The saturable-exonuclease behaviour that drives the oscillation is an "
       "emergent consequence of the ttRecJ being a conserved, limited resource, "
       "not a term written in by hand.", "It resolves the reaction network.  ")
bullet("scaled-particle excluded-volume free energy, scale-dependent viscosity / "
       "diffusion, water activity, and ion screening. The SAME excluded-volume "
       "free energy that stabilises a duplex also tightens enzyme binding; the "
       "SAME viscosity that slows the polymerase slows the exonuclease. These "
       "are not free to fit independently — they all descend from volume "
       "fraction, crowder size, and the species' radii.",
       "It drives every step from one set of physical primitives:  ")
bullet("by construction the network collapses, under a quasi-steady-state "
       "approximation, onto the validated reduced model (SI eqs 3–4); its "
       "elementary constants reproduce the SI Table S5 effective parameters. "
       "That reduction is the documented 'simplify if necessary' fall-back.",
       "It stays anchored to the validated dilute model.  ")
body("Headline prediction. Crowding shortens the period (90 → ~73 min) and "
     "steadily collapses the amplitude. PEG 8000 drives the circuit across a "
     "Hopf bifurcation to a stable fixed point at ~10–11% w/v, abolishing "
     "oscillation; Ficoll 400, a compact near-ideal crowder, keeps the circuit "
     "oscillating across the whole experimental range. That PEG-vs-Ficoll "
     "divergence at equal volume fraction is the central, falsifiable result.")
caveat("Every excluded-volume, viscosity, and enzyme coefficient is a literature-"
       "anchored, tunable hypothesis for wet-lab calibration. All Ficoll-400 "
       "numbers are extrapolations (no primary Ficoll-400 datum exists in the "
       "surveyed literature); the ion channel is Na+-based (our buffer is Mg2+) "
       "and is off by default.")

# ---- 2 NETWORK ---------------------------------------------------------------
heading("2.  The explicit reaction network", 1)
body("Prey N replicates autocatalytically on template G; predator P replicates "
     "on N, consuming it; the shared exonuclease ttRecJ degrades both. Polymerase "
     "(non-limiting in this regime) is folded into the catalytic constants. The "
     "elementary steps are:")
scheme("Prey growth :  N + G  ⇌[kon_NG/koff_NG]⇌  C_NG  —kcat_g→  G + 2 N")
scheme("Predation   :  N + P  ⇌[kon_NP/koff_NP]⇌  C_NP  —kcat_p→  2 P")
scheme("Death (N)   :  N + E  ⇌[kon_eN/koff_eN]⇌  C_NE  —kcat_eN→ E")
scheme("Death (P)   :  P + E  ⇌[kon_eP/koff_eP]⇌  C_PE  —kcat_eP→ E")
scheme("Conservation:  G_tot = G + C_NG ;   E_tot (rec) = E + C_NE + C_PE")
body("Two features of the reduced model emerge here mechanistically rather than "
     "being imposed:")
bullet("the saturating prey-growth term 1/(1+b·G·N) of the reduced model "
       "is just finite template — G_tot = G + C_NG. Replication saturates "
       "when the template is occupied.", "Template saturation.  ")
bullet("the competitive factor 1/(1+P/Km,P) of the reduced model is exonuclease "
       "conservation with the predator a HIGH-affinity (low-Km) substrate that "
       "occupies ttRecJ, and the prey a LOW-affinity (high-Km) substrate that "
       "does not. The predator competitively shields the prey from degradation "
       "— the heart of the oscillation — with no hand-written term.",
       "The oscillation engine.  ")

# ---- 3 ARCHITECTURE ----------------------------------------------------------
heading("3.  Architecture: physics in, dynamics out", 1)
make_table(
    ["Layer", "Contents"],
    [["0  Control", "concentration c (% w/v); molecular weight M; identity "
      "(PEG 8000 / Ficoll 400)"],
     ["1  Physical primitives", "volume fraction φ; excluded-volume free "
      "energy μ_ex(r,φ); correlation length ξ; scale-dependent "
      "viscosity η_eff(r) and diffusivity; water activity; free-ion fraction"],
     ["2  Elementary constants", "kon, koff (→ K) and kcat for every step, "
      "each DERIVED from the Layer-1 primitives and the species' sizes"],
     ["3  Network dynamics", "7-species mass-action ODEs integrated → period, "
      "amplitude, Hopf boundary vs (c, M, identity)"]],
    widths=[1.6, 5.0])

# ---- 4 PRIMITIVES ------------------------------------------------------------
heading("4.  Layer 1 — the shared physical primitives", 1)

heading("4.1  Excluded-volume free energy (scaled-particle theory)", 2)
body("The free-energy cost of inserting a convex solute of radius r into a "
     "crowder of radius R_c at packing fraction φ (Minton; Lebowitz):")
omath(r"\frac{\mu_{ex}(r)}{RT} = -\ln(1-\varphi) + "
      r"\left(3z + 3z^{2} + z^{3}\right)\frac{\varphi}{1-\varphi}, "
      r"\quad z=\frac{r}{R_c}")
body("The three terms are the surface, curvature, and volume contributions to "
     "excluded volume. For an association A + B ↔ AB the driving force is the "
     "difference — the compact product excludes less volume than the separated "
     "reactants, so crowding favours binding:")
omath(r"\frac{\Delta\Delta G_{assoc}}{RT} = \mu_{ex}(r_{AB}) - "
      r"\mu_{ex}(r_A) - \mu_{ex}(r_B) \quad (<0 \Rightarrow \text{crowding stabilises } AB)")
body("This single function supplies the excluded-volume contribution to EVERY "
     "association in the network — strand hybridization and enzyme binding "
     "alike — differing only by the species' radii. It is the same physics "
     "that gives Knowles' bimolecular-duplex stabilization and Zimmerman's "
     "enhanced polymerase–DNA binding.")

heading("4.2  Scale-dependent viscosity and diffusion", 2)
body("A diffusing species feels a viscosity that depends on its size relative to "
     "the polymer mesh ξ (Holyst, PEG / coils):")
omath(r"\frac{\eta_{eff}(r)}{\eta_0} = \exp\left[b\left(\frac{R_{eff}}{\xi}"
      r"\right)^{a}\right], \quad \frac{1}{R_{eff}^{2}}=\frac{1}{R_h^{2}}+"
      r"\frac{1}{r^{2}}, \quad \xi = R_c\left(\frac{c}{c^{*}}\right)^{-0.75}")
body("with a ≈ 0.78, b ≈ 1.61 (PEG family). A diffusion-limited "
     "association rate then scales as kon ∝ 1/η_eff at the larger "
     "partner's radius. Small strands feel near-solvent viscosity; large enzymes "
     "feel much more. Ficoll, a compact sphere with no mesh, instead uses the "
     "Mooney hard-sphere law:")
omath(r"\frac{\eta}{\eta_0}=\exp\left[\frac{[\eta]\,\varphi}{1-\varphi/\varphi_{max}}\right]")
caveat("a, b are Holyst-family values from later papers (Sozański 2016); "
       "the 2009 original states only 'constants close to unity', and PEG 8000 "
       "was not directly fitted (nearest data PEG 6000/12000).")

heading("4.3  Water activity and ion screening (secondary / optional)", 2)
body("Crowding lowers water activity (preferential hydration); for short duplexes "
     "this is a modest, regime-dependent correction to the hybridization free "
     "energy (Knowles 2011; Markarian 2010), kept small here. Separately, "
     "nonionic crowders sequester buffer cations (Bielec 2021), lengthening the "
     "Debye screening length; because like-charged DNA strands cannot associate "
     "without screening (Kowalski 2022), this slows hybridization. The ion "
     "channel is off by default.")
caveat("Bielec is parameterized for Na+; our buffer is Mg2+ — the ion "
       "channel is an explicit extrapolation, exposed only for exploration.")

# ---- 5 ELEMENTARY MAPPING ----------------------------------------------------
heading("5.  Layer 2 — elementary constants and how crowding moves them", 1)
body("Each lumped constant of the reduced model resolves into elementary steps. "
     "The dilute values are fixed by inverting the quasi-steady-state map onto "
     "SI Table S5:")
make_table(
    ["Reduced constant", "Mechanistic identity", "Dilute value set by"],
    [["k1 (prey growth)", "kcat_g · K1   (K1 = N·G assoc. const.)",
      "k1·pol = kcat_g·K1"],
     ["b (growth saturation)", "K1 / G_tot", "finite template"],
     ["k2 (predation)", "kcat_p · K2   (K2 = N·P assoc. const.)",
      "k2·pol = kcat_p·K2"],
     ["kN (prey decay)", "kcat_eN / Km_N   (Km_N large → N linear)",
      "Km_N ≈ 1000 nM"],
     ["kP (predator decay)", "kcat_eP / Km_P", "Km_P = 34 nM"],
     ["Km,P (competition)", "Km_P = (koff_eP + kcat_eP)/kon_eP", "= 34 nM"]],
    widths=[1.7, 3.0, 1.9])
body("")
body("Crowding then acts on the elementary pieces, consistently. Association "
    "equilibria shift by the excluded-volume free energy (on-rate set by "
    "diffusion, off-rate by thermodynamic consistency); intrinsic turnover "
    "shifts by enzyme class:")
omath(r"K(\varphi) = K^{0}\exp\left(-\frac{\Delta\Delta G}{RT}\right), \quad "
      r"k_{on}(\varphi)=\frac{k_{on}^{0}}{\eta_{eff}}, \quad "
      r"k_{off}=\frac{k_{on}}{K}")
omath(r"k_{cat}^{pol/nick}(\varphi)=k_{cat}^{0}\,e^{+c_{P}\varphi}, \quad "
      r"k_{cat}^{exo}(\varphi)=k_{cat}^{0}\,e^{-c_{E}\varphi}")
body("In words:")
bullet("each association equilibrium shifts by the excluded-volume free energy "
       "(§4.1), plus optional water-activity and ion terms: "
       "K(φ) = K⁰·exp(−ΔΔG/RT). The on-rate kon "
       "slows by diffusion (§4.2); koff = kon/K keeps kinetics and "
       "thermodynamics consistent.", "Binding / hybridization.  ")
bullet("intrinsic turnover is enzyme-class-specific and cannot be derived from "
       "excluded volume, so it is taken from enzyme data: polymerase + nickase "
       "turnover up (kcat_g, kcat_p · e^{c·φ}, c from Akabayov), "
       "exonuclease turnover down (kcat_eN, kcat_eP · e^{−c·φ}, "
       "c = ln(5.5)/0.166 from Sasaki's Exo I at 20% PEG 8000).",
       "Catalytic turnover.  ")
body("The emergent effect on the reduced constants (read off from the elementary "
     "set) for PEG 8000: predation k2 and growth k1 rise together (excluded "
     "volume + processivity), the exonuclease decays kN, kP fall (catalytic "
     "inhibition), and Km,P drifts down only slightly — consistent with "
     "Sasaki's finding that crowding moves the nuclease Vmax, not its Km.")

# ---- 6 CALIBRATION -----------------------------------------------------------
heading("6.  Calibration to the experiment", 1)
body("Two small calibrations turn the QSSA-mapped constants into a robust "
     "explicit network whose dilute limit matches the measured ~90 min cycle:")
bullet("the naive QSSA estimate ignores prey/predator held in the N·G and "
       "N·P complexes; the explicit network resolves that bound pool, which "
       "slightly slows the free-pool cycle. A timescale factor of 0.8 on the "
       "catalytic constants restores the measured period; the resulting effective "
       "constants sit at ~0.8× the reduced-model fit (b and Km,P unchanged).",
       "Timescale (×0.8).  ")
bullet("a small template-independent leak (background synthesis ~0.02 nM/min "
       "prey, 0.006 nM/min predator) — a documented feature of the "
       "Montagne/Fujii PEN toolbox — lifts the troughs off the absorbing "
       "zero state. Without it any deterministic PEN model sits on a homoclinic "
       "knife-edge where a vanishing predator cannot recover. With it, the limit "
       "cycle is robust (predator stays ≳ 22 nM), as the experiment shows.",
       "Template-independent leak.  ")
body("Dilute result: period 90 min, predator 22 → 154 nM, prey 0 → 27 nM "
     "— a robust relaxation oscillation. Implied effective constants: "
     "k1 1.6e-3, k2 2.5e-3, kN 1.7e-2, kP 3.8e-3 (all ~0.8× SI), "
     "b 4.8e-5 and Km,P 34 (exact).")

# ---- 7 ODE -------------------------------------------------------------------
heading("7.  The full model, written out", 1)
body("With the free enzyme set by conservation, E = rec − C_NE − C_PE, and "
     "template-independent leak terms λ_N, λ_P, the seven states evolve as:")
omath(r"\frac{dN}{dt} = -k_{on}^{NG}NG + k_{off}^{NG}C_{NG} + 2k_{cat}^{g}C_{NG} "
      r"- k_{on}^{NP}NP + k_{off}^{NP}C_{NP} - k_{on}^{eN}NE + k_{off}^{eN}C_{NE} + \lambda_N")
omath(r"\frac{dP}{dt} = -k_{on}^{NP}NP + k_{off}^{NP}C_{NP} + 2k_{cat}^{p}C_{NP} "
      r"- k_{on}^{eP}PE + k_{off}^{eP}C_{PE} + \lambda_P")
omath(r"\frac{dG}{dt} = -k_{on}^{NG}NG + k_{off}^{NG}C_{NG} + k_{cat}^{g}C_{NG}")
omath(r"\frac{dC_{NG}}{dt} = k_{on}^{NG}NG - k_{off}^{NG}C_{NG} - k_{cat}^{g}C_{NG}")
omath(r"\frac{dC_{NP}}{dt} = k_{on}^{NP}NP - k_{off}^{NP}C_{NP} - k_{cat}^{p}C_{NP}")
omath(r"\frac{dC_{NE}}{dt} = k_{on}^{eN}NE - k_{off}^{eN}C_{NE} - k_{cat}^{eN}C_{NE}")
omath(r"\frac{dC_{PE}}{dt} = k_{on}^{eP}PE - k_{off}^{eP}C_{PE} - k_{cat}^{eP}C_{PE}")
body("Every kon, koff, kcat is the Layer-2 function of (φ, M, identity). At "
     "φ = 0 they reduce to the dilute set and the network reproduces the "
     "validated 90 min cycle.")

# ---- 8 IDENTITY --------------------------------------------------------------
heading("8.  PEG 8000 vs Ficoll 400 — the identity axis", 1)
bullet("flexible linear coil, crowder radius R_c ≈ 3.4 nm. Small radius "
       "means a large excluded-volume free energy per unit φ and a real "
       "semidilute mesh (scale-dependent viscosity). Strong exonuclease "
       "inhibition (Sasaki, PEG 8000). Near-ideal/entropic toward DNA folding, "
       "enthalpic toward enzymes.", "PEG 8000.  ")
bullet("compact, highly branched quasi-sphere, R_c ≈ 10 nm. Large radius "
       "means a much smaller excluded-volume effect per unit φ, no mesh "
       "(Mooney hard-sphere viscosity), and milder enzyme effects "
       "(Homchaudhuri: Ficoll slows reactions far less than extended polymers).",
       "Ficoll 400.  ")
body("Because R_c enters μ_ex through z = r/R_c, the same volume fraction "
     "produces a substantially larger excluded-volume effect for PEG than for "
     "Ficoll — which is exactly why the model predicts the two crowders to "
     "have qualitatively different effects on the oscillation. Molecular weight "
     "enters through R_c, c* and ξ, so the model predicts chain-length "
     "dependence as well as concentration dependence.")
caveat("No surveyed paper used Ficoll 400; all Ficoll coefficients are "
       "extrapolations from compact-crowder behaviour and must be calibrated.")

# ---- 9 PREDICTIONS -----------------------------------------------------------
heading("9.  Predictions", 1)
fig1 = os.path.join(HERE, "mechanistic_timeseries.png")
if os.path.exists(fig1):
    doc.add_picture(fig1, width=Inches(6.4))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
body("Figure 1. Settled dynamics of the mechanistic network: dilute, and at 5% "
     "and 10% w/v PEG 8000. The amplitude shrinks and the cycle approaches the "
     "fixed point as crowding increases.", italic=True, size=9)

fig2 = os.path.join(HERE, "mechanistic_predictions.png")
if os.path.exists(fig2):
    doc.add_picture(fig2, width=Inches(6.4))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
body("Figure 2. Predicted period (left) and predator amplitude (right) vs "
     "crowder concentration. PEG 8000 crosses the Hopf boundary (amplitude "
     "→ 0) near 10–11% w/v; Ficoll 400 keeps oscillating throughout.",
     italic=True, size=9)

make_table(
    ["Condition", "Period (min)", "Predator amp (nM)", "Oscillating?"],
    [["Dilute", "90", "132", "yes (robust)"],
     ["5% w/v PEG 8000", "78", "76", "yes"],
     ["8% w/v PEG 8000", "73", "19", "yes, near boundary"],
     ["~11% w/v PEG 8000", "—", "~0", "NO — Hopf crossing"],
     ["16% w/v Ficoll 400", "69", "38", "yes (still oscillating)"]],
    widths=[2.0, 1.3, 1.6, 1.7])
body("")
body("The single most testable claims for the wet lab: (1) crowding shortens the "
     "period; (2) PEG 8000 abolishes oscillation near ~10–11% w/v; (3) at "
     "equal volume fraction Ficoll 400 is far milder and preserves oscillation. "
     "Predicting the period and the Hopf concentration across crowder identity "
     "and molecular weight — from physical primitives rather than a direct "
     "fit — is the benchmark the literature recommends.")

# ---- 10 REDUCTION ------------------------------------------------------------
heading("10.  Reduction to the two-variable model (simplify if needed)", 1)
body("Applying the quasi-steady-state approximation to the four complexes and the "
     "free enzyme,")
omath(r"C_{NG}=K_1 NG, \quad C_{NP}=K_2 NP, \quad "
      r"E=\frac{rec}{1+N/K_m^{N}+P/K_m^{P}}")
body("collapses the seven equations to the validated two-variable form (Fujii "
     "SI eqs 3–4):")
omath(r"\frac{dN}{dt}=\frac{k_1\,pol\,G\,N}{1+bGN} - k_2\,pol\,N\,P "
      r"- \frac{rec\,k_N\,N}{1+P/K_{m,P}}")
omath(r"\frac{dP}{dt}=k_2\,pol\,N\,P - \frac{rec\,k_P\,P}{1+P/K_{m,P}}")
body("with crowding-dependent constants given by the derived expressions:")
omath(r"k_1(\varphi)=\frac{k_{cat}^{g}(\varphi)K_1(\varphi)}{pol}, \quad "
      r"b(\varphi)=\frac{K_1(\varphi)}{G_{tot}}, \quad "
      r"k_2(\varphi)=\frac{k_{cat}^{p}(\varphi)K_2(\varphi)}{pol}, \quad "
      r"k_N(\varphi)=\frac{k_{cat}^{eN}(\varphi)}{K_m^{N}(\varphi)}")
caveat("Scope of the reduction. This collapse is exact only in the strict "
       "fast-binding limit and without the leak. Numerically, the bare "
       "two-variable model is far more fragile than the full network: with the "
       "same derived constants it mis-predicts the dilute period (~45 vs 90 min) "
       "and loses oscillation almost immediately, because it cannot hold the prey "
       "and predator transiently sequestered in the N·G, N·P and enzyme "
       "complexes. The reduction is therefore the right tool for analytic "
       "intuition and for the functional FORM of each constant's crowding "
       "dependence, but the QUANTITATIVE predictions (period, Hopf concentration, "
       "PEG-vs-Ficoll divergence) come from integrating the full seven-species "
       "network. The interactive explorer runs that full network.")

# ---- 11 ASSUMPTIONS ----------------------------------------------------------
heading("11.  Assumptions and calibration priorities", 1)
bullet("polymerase is non-limiting (folded into kcat) — consistent with the "
       "reduced model treating pol as a constant; only the exonuclease is the "
       "limiting, saturating resource.", "Pol not limiting.  ")
bullet("intermediate hairpin conformers are not resolved (assumed fast/unstable, "
       "as in the Fujii SI and the team reactome).", "Conformers lumped.  ")
bullet("the strong exonuclease anchor (5.5×) is an Exo I number; ttRecJ "
       "activity vs PEG is the single highest-value calibration measurement.",
       "ttRecJ ≠ Exo I.  ")
bullet("excluded-volume radii, the Holyst a/b, the enzyme kcat coefficients, "
       "and the leak magnitude are tunable; the model's qualitative predictions "
       "(period shortening, PEG Hopf crossing, Ficoll mildness) are robust to "
       "their precise values, but the Hopf concentration is not — fit it.",
       "Coefficients are hypotheses.  ")
bullet("all Ficoll-400 numbers are extrapolations; the Mg2+ ion channel is off "
       "by default.", "Known gaps.  ")
body("Priority calibration: (1) ttRecJ activity vs PEG 8000 and vs Ficoll 400; "
     "(2) prey/predator hybridization on-rate and stability vs crowder and MW; "
     "(3) solution viscosity vs crowder and MW at 46.5 °C; (4) the leak rate.")

# ---- 12 REFERENCES -----------------------------------------------------------
heading("12.  Key references (subset of the 47-paper scan)", 1)
body("Access: [full] full text; [abs] abstract; [2°] secondary. Catalog "
     "numbers per the Undermind report.", italic=True, size=9)
refs = [
    "[#1] Fujii & Rondelez (2013) Predator-prey molecular ecosystems. ACS Nano "
    "7:27. — baseline network + SI eqs 3–4, Table S5. [full]",
    "[#3] Montagne et al. (2011) Programming an in vitro DNA oscillator. Mol Syst "
    "Biol 7:466. — PEN toolbox, leak reactions. [full]",
    "[#4] Bielec et al. (2021) Ion complexation… J Phys Chem Lett 13:112. "
    "— ion-sequestration channel, K∝[Na+]^2.51. [full]",
    "[#7] Holyst et al. (2009) Scaling form of viscosity… PCCP 11:9025. "
    "— scale-dependent viscosity η_eff=η₀exp[b(R/ξ)^a]. "
    "[abs; a,b via 2° Sozański 2016]",
    "[#8] Knowles et al. (2011) Preferential interaction vs excluded volume… "
    "PNAS 108:12699. — bimolecular-duplex excluded-volume stabilization, "
    "m-values. [full]",
    "[#12] Berezhkovskii & Szabó (2016) Crowding effects on bimolecular "
    "rates. J Phys Chem B 120:5998. — Collins–Kimball + depletion "
    "e^{βΔU}. [full]",
    "[#14] Zhou, Rivas & Minton (2008) Macromolecular crowding… Annu Rev "
    "Biophys 37:375. — excluded-volume theory, enhancement magnitudes. [full]",
    "[#15/#42] Minton (2001 JBC; 1998 Methods Enzymol) — scaled-particle "
    "activity coefficients. [via 2° #14]",
    "[#17] Weilandt & Hatzimanikatis (2018) Crowding and Michaelis–Menten. "
    "Biophys J 117:355. — Km, Vmax under crowding. [full]",
    "[#18] Baltierra-Jasso et al. (2015) Crowding-induced hairpin hybridization. "
    "JACS 137:16020. — PEG 8000 k_close +4×, ΔΔG −1.73 "
    "kcal/mol. [full]",
    "[#19] Markarian & Schlenoff (2010) Crowding and ionic strength on "
    "hybridization. J Phys Chem B 114:10620. — regime-dependent water/ion "
    "coupling. [full]",
    "[#22] Sasaki et al. (2006) Crowding and DNA polymerase. Biotechnol J 1:440. "
    "— Pol binding up, intrinsic kcat down. [abs]",
    "[#23] Sasaki et al. (2007) Regulation of DNA nucleases by crowding. NAR "
    "35:4086. — endo up, exo down ~5.5× (Vmax) at 20% PEG 8000. [full]",
    "[#24] Zimmerman & Harrison (1987) Crowding increases polymerase–DNA "
    "binding. PNAS 84:1871. — enzyme-binding enhancement. [abs]",
    "[#26] Kowalski et al. (2022) Screening of Coulomb repulsions… Nat "
    "Commun 13:6451. — like-charged DNA needs counter-ion screening. [full]",
    "[#38] Akabayov et al. (2013) Crowding and DNA replication. Nat Commun "
    "4:1615. — replication up ~2–4× at 4% PEG. [full]",
    "[#35] Homchaudhuri et al. (2006) Crowding by dextrans and Ficolls. "
    "Biopolymers 83:477. — Ficoll far milder than extended polymers. [abs]",
    "[#46] Echeverría et al. (2018) Damping of catalytic oscillators under "
    "crowding. Physica A. — precedent for crowding-induced damping.",
]
for r_ in refs:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.first_line_indent = Inches(-0.3)
    run = p.add_run(r_); run.font.size = Pt(8.5); run.font.name = SERIF

doc.add_paragraph()
n = doc.add_paragraph()
r = n.add_run("Implementation: crowded_mechanistic.py (7-species network; "
              "reproduces the validated dilute cycle, then drives every "
              "elementary constant from the shared crowding primitives). The "
              "two-variable reduction is the documented simplification.")
r.italic = True; r.font.size = Pt(9); r.font.color.rgb = GREY

out = os.path.join(HERE, "Crowded_PredatorPrey_Mechanistic_Model.docx")
try:
    doc.save(out)
except PermissionError:
    base, ext = os.path.splitext(out)
    i = 2
    while True:
        alt = f"{base}_v{i}{ext}"
        try:
            doc.save(alt)
            out = alt
            break
        except PermissionError:
            i += 1
print(f"saved {out}")
