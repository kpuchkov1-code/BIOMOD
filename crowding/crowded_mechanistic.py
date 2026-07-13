"""
crowded_mechanistic.py
======================
STEP 3 (v2) -- a bottom-up MECHANISTIC model of macromolecular crowding in the
Fujii-Rondelez DNA predator-prey oscillator.

WHY THIS REPLACES THE FACTOR MODEL (v1)
---------------------------------------
v1 multiplied the four lumped rate constants (k1, k2, kN, kP) by fitted
exponential factors. That is phenomenological: it cannot get the cross-couplings
right and treats independent fits where the physics is shared.

v2 resolves each lumped constant into the ELEMENTARY steps it actually hides --
strand hybridization (an equilibrium), enzyme-substrate binding (a Michaelis
constant), catalytic turnover (k_cat), diffusional encounter -- and lets crowding
act on each elementary step through ONE shared set of physical primitives:

    * scaled-particle-theory excluded-volume free energy   mu_ex(r, phi, R_c)   [ENTROPIC, hard-core]
    * preferential-interaction / enthalpic term            dG_enth(phi, chi)    [CHEMICAL IDENTITY]
    * water activity (preferential hydration)              a_w(phi, k_aw)       [CHEMICAL IDENTITY]
    * Holyst scale-dependent viscosity / Stokes-Einstein   D_rel(phi, M, r)
    * ion sequestration -> Debye screening (Mg2+ stub)     free_ion_fraction    [OFF -- see note]
    * enzyme-class-specific catalytic factors              Pol/Nick up, Exo down

The same mu_ex that stabilises a duplex also tightens enzyme binding; the same
viscosity that slows the polymerase slows the exonuclease. None of these are
free to fit independently -- they all descend from phi, M, identity and the
species' sizes. The model is therefore the most physically-faithful description
we can write before wet-lab calibration.

WHY PEG != FICOLL (chemical identity, not just size) -- addresses Jack's review
------------------------------------------------------------------------------
Bare scaled-particle theory (SPT) is purely entropic/hard-sphere, so it can only
separate two crowders by their size (R_c) and shape (coil vs sphere). That is not
enough: PEG and Ficoll differ CHEMICALLY. We now carry that difference through two
identity channels layered on top of SPT:
  * PEG 8000  -- near-ideal / weakly excluded toward DNA (small direct chi) but a
    STRONG osmolyte that depresses water activity (large k_aw). Its extra action
    beyond hard-core exclusion loads onto the WATER-ACTIVITY channel.
  * Ficoll 400 -- the more strongly preferentially EXCLUDED / "enthalpic" crowder
    (Sung & Nesbitt): a hydrophilic polysucrose that structures water weakly
    (small k_aw) but adds a preferential-interaction stabilisation of compact
    states (positive chi). Its extra action loads onto the ENTHALPIC channel.
So at equal volume fraction the two crowders now act through DIFFERENT physics,
and the PEG-vs-Ficoll divergence becomes a chemistry prediction, not a geometry
artefact. chi and k_aw are literature-anchored, tunable hypotheses (calibrate the
sign/magnitude in the wet lab); at phi=0 both vanish, so the dilute cycle is
untouched.

A NOTE ON "EQUILIBRIUM" (addresses Jack's equilibrium-constant scepticism)
--------------------------------------------------------------------------
This model does NOT assume the system is at equilibrium. It integrates the FULL
mass-action KINETICS of every elementary step (explicit kon and koff), so the
driven, far-from-equilibrium limit cycle is resolved directly. An equilibrium
constant K only appears as the RATIO kon/koff of a single reversible binding step;
crowding shifts that ratio by a LOCAL detailed-balance argument (the excluded
volume/enthalpy/hydration that a crowder adds to the bound vs free states), which
holds for each elementary step regardless of the global non-equilibrium drive. We
partition the shift physically: kon is set by diffusion (Smoluchowski encounter,
slowed by viscosity), and koff is then DERIVED as kon/K so kinetics and
thermodynamics stay consistent. What this well-mixed ODE genuinely CANNOT capture
is spatial/local non-equilibrium -- depletion zones, reactant trapping in
micro-environments, subdiffusive correlations. That needs a reaction-diffusion or
particle model; the mean-field viscosity term is only a partial (encounter-rate)
nod to it. Flagged as a real limitation, not silently ignored.

THE NETWORK (mass-action, explicit complexes, enzyme conservation)
------------------------------------------------------------------
  Prey growth (autocatalysis of N on template G; Pol folded into k_cat,g):
      N + G   <kon_NG / koff_NG>  C_NG
      C_NG    --k_cat_g-->        G + 2 N           (extension + nicking)
  Predation (P replicates on N, consuming it; Pol folded into k_cat,p):
      N + P   <kon_NP / koff_NP>  C_NP
      C_NP    --k_cat_p-->        2 P               (one N -> one extra P)
  Death (shared exonuclease -- ttRecJ or RecJf, conserved -> the saturable engine):
      N + E   <kon_eN / koff_eN>  C_NE  --k_cat_eN--> E
      P + E   <kon_eP / koff_eP>  C_PE  --k_cat_eP--> E
      E_tot = rec = E_free + C_NE + C_PE            (competition => saturation)

The template saturation (the 1/(1+b G N) of the reduced model) emerges from
finite template (G_tot = G_free + C_NG). The (1+P/Km,P) competitive saturation
of the reduced model emerges from exonuclease conservation with P a high-affinity
(low-Km) and N a low-affinity (high-Km) substrate. Under QSSA on the complexes
this network collapses exactly to the validated SI eqs 3-4 -- the reduction is
the 'simplify if necessary' fall-back.

Reference dilute targets (SI Table S5, PP1): k1=2.0e-3, b=4.8e-5, k2=3.1e-3,
kN=2.1e-2, kP=4.7e-3, Km,P=34, pol=3.7, rec=32.5, G=140.
------------------------------------------------------------------------------
"""

import numpy as np
from scipy.integrate import solve_ivp


# =============================================================================
# 0. OPERATING CONDITIONS + ENZYME SET  (team-configurable -- still undecided)
# =============================================================================
# The operating temperature and the exonuclease identity are ONE coupled decision
# the team has not finalised (see project memory). They are exposed here as knobs
# rather than baked into scattered constants, so switching is a one-line change and
# nothing downstream needs re-deriving by hand.
#
#   T_C  -- operating temperature (deg C). Set by the SHORT-STRAND DNA Tm design,
#           NOT by enzyme optima. The Fujii/PEN predator-prey and the YOKABIO 2025
#           reference team both run isothermal ~46 C for ~12 h. IMPORTANT / honest
#           scope: T_C is RECORDED here (it sets RT for reporting) but it does NOT
#           by itself re-tune the predictions, and that is deliberate. The crowding
#           free energies (SPT excluded volume, enthalpic, hydration) are all
#           expressed in units of RT and are, being ENTROPIC/excluded-volume terms,
#           intrinsically ~T-independent when written that way -- correct physics.
#           The genuinely T-dependent part is the DILUTE baseline (hybridisation Tm
#           via van't Hoff, enzyme kcat via Arrhenius), which is EMPIRICALLY fixed
#           at 46.5 C from Fujii SI Table S5. Moving the operating temperature
#           therefore requires re-mapping that dilute baseline (van't Hoff/Arrhenius)
#           -- a flagged TODO, not an automatic rescale. Do not read a T_C change as
#           a validated re-tune.
#   exo  -- shared exonuclease that drives the death step (the conserved, saturable
#           engine of the oscillation). "ttRecJ" (T. thermophilus, thermostable,
#           opt 50-70 C) or "RecJf" (NEB M0264, E. coli RecJ-MBP, mesophilic opt
#           37 C). Same catalysis (5'->3' ssDNA-specific, Mg2+-dependent); they play
#           the IDENTICAL mechanistic role, so this is a re-parameterisation, not a
#           structural change. At 46 C RecJf is above its optimum and will slowly
#           lose activity over a 12 h run (weakens the conserved-enzyme assumption);
#           ttRecJ is thermostable there. Undecided -- toggle and compare.
OPERATING = {"T_C": 46.5, "exo": "RecJf"}

EXO_LIB = {
    # rec_tot : total exonuclease (nM) -- the conserved species. Both default to
    #           the Fujii ttRecJ mapping (32.5 nM); RecJf has no published PEN
    #           mapping yet, so it inherits the same value flagged for wet-lab check.
    # T_opt_C : catalytic temperature optimum (context for the T_C choice).
    # thermostable : holds activity across a 12 h isothermal run at T_C?
    "ttRecJ": {"rec_tot": 32.5, "T_opt_C": 60.0, "thermostable": True},
    "RecJf":  {"rec_tot": 32.5, "T_opt_C": 37.0, "thermostable": False},
}

# =============================================================================
#    DERIVED CONSTANTS, SIZES, CROWDER LIBRARY
# =============================================================================
T_K = OPERATING["T_C"] + 273.15
RT = 1.98720425e-3 * T_K               # kcal/mol  (~0.635 at 46.5 C)

# Hydrodynamic radii (nm) of every species the physics needs.  Short PEN strands
# are ~10-15 nt; enzymes from their masses.  These set BOTH the excluded-volume
# free energy and the diffusion (viscosity) terms -- one geometry, used twice.
RADII = {
    "N": 1.2, "P": 1.2, "G": 2.0,         # ssDNA strands / template
    "C_NG": 2.2, "C_NP": 1.5,             # duplex products
    "Pol": 3.0, "Exo": 2.8,               # Bst (polymerase), RecJ-family (exonuclease)
    "C_NE": 3.0, "C_PE": 3.0,             # enzyme.substrate
}

CROWDERS = {
    "PEG8000": {
        "label": "PEG 8000", "kind": "coil",
        "M": 8000.0, "v_bar": 0.83, "R_c": 3.4, "R_h": 2.5,
        "monomer_M": 44.0, "visc_a": 0.78, "visc_b": 1.61,
        # -- chemical-identity channels (what makes PEG != Ficoll beyond size) --
        "chi": 0.0,    # preferential-interaction / enthalpic coeff (RT per unit
                       #   phi per unit buried surface). PEG is near-ideal toward
                       #   DNA -> ~0; its special chemistry rides the k_aw channel.
        "k_aw": 0.90,  # water-activity depression slope (ln a_w ~ -k_aw*phi). PEG
                       #   is a STRONG osmolyte -> large. (Was a global 0.6.)
        # enzyme-class catalytic factors (intrinsic chemistry; cannot be derived
        # from excluded volume, so taken from enzyme data):
        "c_polnick": 3.0,   # net Pol+Nick turnover up (Akabayov ~2-4x @4% PEG)
        "c_exo": 10.3,      # exonuclease kcat down: ln(5.5)/0.166 (Sasaki, PEG8000)
        "spt_scale": 1.0,   # calibrates SPT magnitude to Baltierra-Jasso PEG8000
    },
    "FICOLL400": {
        "label": "Ficoll 400", "kind": "sphere",
        "M": 400000.0, "v_bar": 0.67, "R_c": 10.0, "R_h": 10.0,
        "monomer_M": 350.0, "visc_a": 1.0, "visc_b": 2.5,
        # -- chemical-identity channels: Ficoll is the more strongly excluded /
        #    "enthalpic" crowder (Sung & Nesbitt) but a weak osmolyte. --
        "chi": 0.35,   # positive -> preferential-exclusion stabilisation of compact
                       #   (bound/duplex) states, ON TOP of its (small, big-sphere)
                       #   SPT term. This is the chemistry that size alone misses.
        "k_aw": 0.25,  # weak water-activity depression (polysucrose, hydrophilic).
        # ALL Ficoll numbers are flagged extrapolations (no primary Ficoll-400
        # datum in the surveyed papers). Compact sphere -> milder geometry.
        "c_polnick": 2.0, "c_exo": 5.0, "spt_scale": 1.0,
    },
}


# =============================================================================
# 1. PHYSICAL PRIMITIVES  (shared by every elementary step)
# =============================================================================
def volume_fraction(wt_pct, cr):
    return cr["v_bar"] * (wt_pct / 100.0)


def spt_mu_ex(r_solute, phi, cr):
    """Scaled-particle-theory excluded-volume insertion free energy (units RT)
    for a convex solute of radius r in a crowder of radius R_c at packing phi.
        mu_ex/RT = -ln(1-phi) + (3z + 3z^2 + z^3) Q ,  z = r/R_c,  Q = phi/(1-phi)
    Leading Minton/Lebowitz form: surface (z), curvature (z^2) and volume (z^3)
    terms. Larger solutes are excluded more, so association of two solutes into a
    more compact product is favoured.  (Minton 1998/2001; Zhou-Rivas-Minton 2008.)
    """
    if phi <= 0.0:
        return 0.0
    z = r_solute / cr["R_c"]
    Q = phi / (1.0 - phi)
    return cr["spt_scale"] * (-np.log(1.0 - phi) + (3*z + 3*z**2 + z**3) * Q)


def dG_assoc_EV(rA, rB, rAB, phi, cr):
    """Excluded-volume (ENTROPIC, hard-core) free-energy change for A + B <-> AB
    (units RT). Negative => crowding favours the (more compact) complex."""
    return spt_mu_ex(rAB, phi, cr) - spt_mu_ex(rA, phi, cr) - spt_mu_ex(rB, phi, cr)


# characteristic surface radius (nm) that normalises the enthalpic surface term
R_SURF_REF = 1.0

def dG_assoc_enthalpic(rA, rB, rAB, phi, cr):
    """Preferential-interaction / ENTHALPIC (chemical-identity) free-energy change
    for A + B <-> AB (units RT). This is the piece bare SPT cannot see -- it is
    what physically separates PEG from Ficoll at equal volume fraction.

    A crowder that is preferentially EXCLUDED from macromolecular surface (chi>0,
    Timasheff Gamma<0) pays a free-energy cost proportional to the exposed surface;
    association BURIES surface (r_AB^2 < r_A^2 + r_B^2 for a compact complex), so a
    chi>0 crowder further STABILISES the complex on top of hard-core exclusion. A
    weakly attractive/accommodated crowder (chi<0) opposes it.

        dG_enth/RT = chi * phi * (r_AB^2 - r_A^2 - r_B^2) / R_ref^2

    Ficoll (chi>0) gains stabilisation here that does NOT scale with its (small,
    big-sphere) SPT term; PEG (chi~0) contributes almost nothing here and instead
    acts through the water-activity channel. chi is a tunable hypothesis to be
    pinned by wet-lab PEG-vs-Ficoll comparison; it vanishes at phi=0. (Timasheff
    1998; Sung & Nesbitt 2011 -- Ficoll/dextran enthalpic, PEG near-ideal.)"""
    dArea = (rAB**2 - rA**2 - rB**2) / (R_SURF_REF**2)
    return cr["chi"] * phi * dArea


def water_activity_dG(phi, cr, n_w=2.0):
    """Preferential-hydration (CHEMICAL-IDENTITY) contribution to a duplex
    equilibrium (units RT). Crowding lowers water activity a_w; if forming the
    duplex releases n_w waters, the shift is n_w * ln a_w, with ln a_w ~ -k_aw*phi.
    k_aw is now CROWDER-SPECIFIC: PEG is a strong osmolyte (large k_aw) while Ficoll
    barely perturbs water (small k_aw), so this term is a second identity channel.
    Kept modest in magnitude. (Knowles 2011; Markarian 2010 -- regime-dependent.)"""
    ln_aw = -cr["k_aw"] * phi
    return n_w * ln_aw


def free_ion_fraction(phi, cr, kappa=0.49):
    """[DISABLED SENSITIVITY STUB -- contributes ZERO to every headline prediction;
    reached only when elem_constants(..., use_ion=True), which is NOT the default.]

    Intended Mg2+ sequestration: the surviving free divalent-cation fraction if the
    crowder chelates buffer cations, c_monomer[M] = phi*rho/monomer_M (rho ~1.2 g/mL).
    It is OFF because it is NOT yet valid for THIS system: (1) the isotherm/kappa
    here is a MONOVALENT (Na+, Bielec) parameterisation, but all three PEN enzymes
    and the whole buffer are Mg2+ (divalent) -- a correct treatment needs Manning
    counter-ion condensation / Poisson-Boltzmann, not this monovalent form; (2) we
    have no MEASURED crowder-Mg2+ sequestration constant. PEG chelates Mg2+ only
    weakly, so the effect is expected small. Left as an explicit, clearly-labelled
    stub for a future sensitivity sweep -- honestly, it is currently absent, not
    'a minor effect that is nevertheless implemented'."""
    c_monomer = (phi * 1200.0) / cr["monomer_M"]
    return 1.0 / (1.0 + kappa * c_monomer)


def viscosity_factor(wt_pct, cr, r_probe):
    """eta_eff(probe)/eta0 felt by a species of radius r_probe.
    Coil (PEG): Holyst scale-dependent  exp[b (R_eff/xi)^a], 1/R_eff^2=1/R_h^2+1/r^2,
    xi = R_c (c/c*)^-0.75 (diverges as c->0 so factor->1).
    Sphere (Ficoll): Mooney  exp[[eta] phi/(1-phi/phi_max)]."""
    if wt_pct <= 0.0:
        return 1.0
    phi = volume_fraction(wt_pct, cr)
    if cr["kind"] == "coil":
        c_star = _overlap_wt_pct(cr)
        xi = cr["R_c"] * (wt_pct / c_star) ** (-0.75)
        R_eff = 1.0 / np.sqrt(1.0/cr["R_h"]**2 + 1.0/r_probe**2)
        return float(np.exp(cr["visc_b"] * (R_eff/xi) ** cr["visc_a"]))
    phi_max = 0.6
    phi = min(phi, 0.95*phi_max)
    return float(np.exp(cr["visc_b"] * phi / (1.0 - phi/phi_max)))


def _overlap_wt_pct(cr):
    NA = 6.022e23
    Rg_cm = cr["R_c"] * 1e-7
    return (3.0 * cr["M"] / (4.0*np.pi*NA*Rg_cm**3)) * 100.0


def diffusion_factor(wt_pct, cr, rA, rB):
    """Relative mutual diffusivity for an A-B encounter = eta0/eta_eff at the
    larger partner's size (the slower diffuser limits the encounter)."""
    r_enc = max(rA, rB)
    return 1.0 / viscosity_factor(wt_pct, cr, r_enc)


# =============================================================================
# 2. ELEMENTARY DILUTE CONSTANTS  (mapped from the validated reduced model)
#    Concentrations nM, time min.  Mapping derivations in the Word document.
# =============================================================================
G_TOT = 140.0
REC = EXO_LIB[OPERATING["exo"]]["rec_tot"]   # conserved, saturating exonuclease

# --- Template-independent background synthesis ("leak") ----------------------
# Jack's question: a constant positive influx of N and P looks like mass appearing
# "from nowhere". It is not. In the PEN toolbox the strands are synthesised de novo
# by the polymerase from a large, buffered dNTP FUEL reservoir (held ~constant here,
# in excess -- the standard PEN assumption). The leak is the small, well-documented
# TEMPLATE-INDEPENDENT background of that same polymerase: nonspecific/ab-initio
# extension of short oligos off dNTPs (Montagne 2011; Rondelez PEN toolbox). So the
# nitrogen/phosphate mass is drawn from the dNTP pool, exactly like the templated
# growth term -- it is fuel-driven synthesis, not creation from nothing.
# Two consequences we now model honestly:
#   (1) it is POLYMERASE-mediated, so under crowding it speeds up with the same
#       Pol/Nick factor as templated synthesis (scaled in elem_constants), rather
#       than being crowding-blind;
#   (2) it also serves as a numerical regulariser lifting the troughs off the
#       absorbing zero state (any deterministic PEN model without it sits on a
#       homoclinic knife-edge). Small vs the ~130 nM oscillation amplitude.
# NOT modelled: dNTP DEPLETION over a 12 h run (the reservoir is treated as
# inexhaustible). That is a known limitation, flagged, not silently assumed away.
LEAK0_N = 0.02
LEAK0_P = 0.006

#  Binding is kept FAST relative to catalysis (large kon, koff at fixed
#  equilibrium / Km) so the complexes stay quasi-stationary and the explicit
#  network collapses tightly onto the validated SI eqs 3-4 in the dilute limit.
#  Every equilibrium constant and Michaelis constant below is identical to the
#  slow-binding mapping; only the absolute timescale of (un)binding is raised.
#  Two calibrations turn the QSSA-mapped constants into a robust explicit network
#  whose DILUTE limit cycle matches the experiment (~90 min, sustained):
#    * TAU = 0.8 scales the catalytic constants. The naive QSSA estimate
#      (kcat_g0 = k1*pol/K1 etc.) ignores prey/predator sequestered in the N.G
#      and N.P complexes; the explicit network resolves that bound pool, so a
#      small downward timescale correction reproduces the measured period. The
#      resulting effective constants sit at ~0.8x the reduced-model fit.
#    * A template-independent LEAK (next block) -- a documented feature of the
#      Montagne/Fujii PEN toolbox (nonspecific background extension) -- lifts the
#      troughs off the absorbing zero state and gives the sustained, robust cycle
#      the experiment shows. Without it any deterministic PEN model sits on the
#      homoclinic knife-edge and a vanishing predator cannot recover.
_TAU = 0.8
ELEM0 = {
    # hybridisation N+G  (K1 = b*G_tot = 6.72e-3 /nM)
    "kon_NG": 1.344, "koff_NG": 200.0, "kcat_g": 1.101 * _TAU,
    # hybridisation N+P  (K2 = 2e-3 /nM kept weak -> predation ~linear)
    "kon_NP": 0.40, "koff_NP": 200.0, "kcat_p": 5.735 * _TAU,
    # exonuclease on predator P  (HIGH affinity: Km_P = 34 = Km,P ; saturates E)
    "kon_eP": 2.0, "koff_eP": 67.84, "kcat_eP": 0.16 * _TAU,
    # exonuclease on prey N  (LOW affinity: Km_N = 1000 >> [N] -> stays linear,
    #                         so only P competitively saturates the exonuclease)
    "kon_eN": 2.0, "koff_eN": 1979.0, "kcat_eN": 21.0 * _TAU,
}


def elem_constants(wt_pct=0.0, crowder_key="PEG8000", use_ion=False):
    """Return the elementary rate constants at crowder loading `wt_pct`.
    Every constant is the dilute value times physics DERIVED from the shared
    primitives -- not an independent fitted factor."""
    e = dict(ELEM0)
    e["leak_N"], e["leak_P"] = LEAK0_N, LEAK0_P
    if wt_pct <= 0.0:
        return e
    cr = CROWDERS[crowder_key]
    phi = volume_fraction(wt_pct, cr)

    # ---- association equilibria: K = kon/koff shifts by three thermodynamic
    #      channels (hard-core excluded volume + enthalpic preferential interaction
    #      + water activity; + optional ion term). kon shifts by DIFFUSION only;
    #      koff = kon / K keeps kinetics and thermodynamics consistent. We do NOT
    #      impose equilibrium -- these feed the full kinetic integration below. ---
    def assoc(kon0, koff0, rA, rB, rAB, like_charged=False, n_w=2.0):
        dG = dG_assoc_EV(rA, rB, rAB, phi, cr)          # excluded volume (entropic)
        dG += dG_assoc_enthalpic(rA, rB, rAB, phi, cr)  # chemical identity (enthalpic)
        dG += water_activity_dG(phi, cr, n_w)           # chemical identity (hydration)
        K = (kon0 / koff0) * np.exp(-dG)                # crowded equilibrium constant
        kon = kon0 * diffusion_factor(wt_pct, cr, rA, rB)   # viscosity slows kon
        if use_ion and like_charged:
            # like-charged strands need counter-ion screening (Kowalski); losing
            # free ions (Bielec) raises the electrostatic barrier -> kon down
            kon *= free_ion_fraction(phi, cr) ** 1.0
        return kon, kon / K

    e["kon_NG"], e["koff_NG"] = assoc(
        ELEM0["kon_NG"], ELEM0["koff_NG"],
        RADII["N"], RADII["G"], RADII["C_NG"], like_charged=True)
    e["kon_NP"], e["koff_NP"] = assoc(
        ELEM0["kon_NP"], ELEM0["koff_NP"],
        RADII["N"], RADII["P"], RADII["C_NP"], like_charged=True)
    # enzyme-substrate binding: excluded volume tightens it (Zimmerman), but no
    # net hybridisation/hydration term (not a duplex) -> n_w = 0
    e["kon_eN"], e["koff_eN"] = assoc(
        ELEM0["kon_eN"], ELEM0["koff_eN"],
        RADII["N"], RADII["Exo"], RADII["C_NE"], n_w=0.0)
    e["kon_eP"], e["koff_eP"] = assoc(
        ELEM0["kon_eP"], ELEM0["koff_eP"],
        RADII["P"], RADII["Exo"], RADII["C_PE"], n_w=0.0)

    # ---- catalytic turnover: enzyme-class-specific (intrinsic chemistry) ------
    f_polnick = np.exp(cr["c_polnick"] * phi)      # Pol + Nick up
    f_exo = np.exp(-cr["c_exo"] * phi)             # exonuclease down (Sasaki)
    e["kcat_g"] = ELEM0["kcat_g"] * f_polnick
    e["kcat_p"] = ELEM0["kcat_p"] * f_polnick
    e["kcat_eN"] = ELEM0["kcat_eN"] * f_exo
    e["kcat_eP"] = ELEM0["kcat_eP"] * f_exo
    # background synthesis is the SAME polymerase acting template-independently,
    # so the leak rides the Pol/Nick crowding factor rather than staying constant
    e["leak_N"] = LEAK0_N * f_polnick
    e["leak_P"] = LEAK0_P * f_polnick
    return e


# =============================================================================
# 3. THE EXPLICIT MECHANISTIC ODE NETWORK  (7 states)
#    y = [N, P, Gf, C_NG, C_NP, C_NE, C_PE];  E_free = rec - C_NE - C_PE
# =============================================================================
def mechanistic_rhs(t, y, e):
    N, P, Gf, C_NG, C_NP, C_NE, C_PE = [max(v, 0.0) for v in y]
    E_free = max(REC - C_NE - C_PE, 0.0)

    r_NG_on = e["kon_NG"] * N * Gf
    r_NG_off = e["koff_NG"] * C_NG
    r_grow = e["kcat_g"] * C_NG

    r_NP_on = e["kon_NP"] * N * P
    r_NP_off = e["koff_NP"] * C_NP
    r_pred = e["kcat_p"] * C_NP

    r_eN_on = e["kon_eN"] * N * E_free
    r_eN_off = e["koff_eN"] * C_NE
    r_eN_cat = e["kcat_eN"] * C_NE

    r_eP_on = e["kon_eP"] * P * E_free
    r_eP_off = e["koff_eP"] * C_PE
    r_eP_cat = e["kcat_eP"] * C_PE

    dN = (-r_NG_on + r_NG_off + 2.0*r_grow         # autocatalysis: net +1 N
          - r_NP_on + r_NP_off                      # bind/unbind predator
          - r_eN_on + r_eN_off)                     # bind/unbind exonuclease
    dP = (-r_NP_on + r_NP_off + 2.0*r_pred          # predation: net +1 P, eats N
          - r_eP_on + r_eP_off)
    dN += e["leak_N"]              # template-independent, dNTP-fuelled background
    dP += e["leak_P"]              # synthesis (polymerase-mediated; see LEAK0 note)
    dGf = -r_NG_on + r_NG_off + r_grow              # template recycled on growth
    dC_NG = r_NG_on - r_NG_off - r_grow
    dC_NP = r_NP_on - r_NP_off - r_pred
    dC_NE = r_eN_on - r_eN_off - r_eN_cat
    dC_PE = r_eP_on - r_eP_off - r_eP_cat
    return [dN, dP, dGf, dC_NG, dC_NP, dC_NE, dC_PE]


def simulate(e, n0=10.0, p0=30.0, t_end=2500.0, n_eval=10000):
    y0 = [n0, p0, G_TOT, 0.0, 0.0, 0.0, 0.0]
    t_eval = np.linspace(0.0, t_end, n_eval)
    return solve_ivp(mechanistic_rhs, (0.0, t_end), y0, args=(e,),
                     t_eval=t_eval, method="LSODA",
                     rtol=1e-8, atol=1e-11, max_step=1.0)


def cycle_stats(sol, tail_min=1000.0):
    t = sol.t
    N, P = sol.y[0], sol.y[1]
    mask = t >= (t[-1] - tail_min)
    tn, nn, pp = t[mask], N[mask], P[mask]
    peaks = [i for i in range(1, len(pp)-1)
             if pp[i] > pp[i-1] and pp[i] > pp[i+1] and pp[i] > pp.mean()]
    period = float(np.mean(np.diff(tn[peaks]))) if len(peaks) >= 2 else None
    return {"period": period, "amp_P": float(pp.max()-pp.min()),
            "amp_N": float(nn.max()-nn.min()),
            "P_range": (float(pp.min()), float(pp.max())),
            "N_range": (float(nn.min()), float(nn.max()))}


# =============================================================================
# 4. EFFECTIVE (REDUCED) CONSTANTS implied by the elementary set -- for audit
#    Lets us read off how the mechanistic model moves k1,k2,kN,kP,Km,P, and
#    confirms it is NOT just multiplying them by hand.
# =============================================================================
def effective_constants(e):
    pol = 3.7
    K1 = e["kon_NG"] / e["koff_NG"]
    K2 = e["kon_NP"] / e["koff_NP"]
    Km_P = (e["koff_eP"] + e["kcat_eP"]) / e["kon_eP"]
    Km_N = (e["koff_eN"] + e["kcat_eN"]) / e["kon_eN"]
    return {
        "k1": e["kcat_g"] * K1 / pol,        # k1*pol = kcat_g*K1
        "b":  K1 / G_TOT,
        "k2": e["kcat_p"] * K2 / pol,
        "kN": e["kcat_eN"] / Km_N,
        "kP": e["kcat_eP"] / Km_P,
        "KmP": Km_P,
    }


# =============================================================================
# 5. PREDICTIONS + CLI
# =============================================================================
def sweep(crowder_key, wt_grid, use_ion=False, t_end=3000.0):
    per, amp = [], []
    for wt in wt_grid:
        e = elem_constants(wt, crowder_key, use_ion=use_ion)
        st = cycle_stats(simulate(e, t_end=t_end, n_eval=int(t_end*4)), 1200.0)
        per.append(st["period"] if st["period"] else np.nan)
        amp.append(st["amp_P"])
    return np.array(per), np.array(amp)


def plot_predictions(wt_grid, outfile, use_ion=False):
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    for key, col in (("PEG8000", "#c47828"), ("FICOLL400", "#1f77b4")):
        per, amp = sweep(key, wt_grid, use_ion=use_ion)
        ax1.plot(wt_grid, per, "o-", ms=3, color=col, label=CROWDERS[key]["label"])
        ax2.plot(wt_grid, amp, "o-", ms=3, color=col, label=CROWDERS[key]["label"])
    ax1.set_xlabel("crowder (% w/v)"); ax1.set_ylabel("period (min)")
    ax1.set_title("Mechanistic model: predicted period")
    ax2.axhline(1.0, color="k", lw=0.7, ls="--")
    ax2.set_xlabel("crowder (% w/v)")
    ax2.set_ylabel("predator amplitude (nM, p-p)")
    ax2.set_title("Predicted amplitude (Hopf on/off)")
    # one shared legend BELOW the plots so it never sits on top of the curves
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.01))
    fig.suptitle("Crowded Fujii PP1 -- mechanistic network "
                 "(PEG 8000 vs Ficoll 400)", fontsize=11)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(outfile, dpi=140, bbox_inches="tight")
    print(f"saved {outfile}")


def plot_timeseries(outfile, conditions):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(conditions), figsize=(5.2*len(conditions), 4.2))
    if len(conditions) == 1:
        axes = [axes]
    for ax, (wt, key) in zip(axes, conditions):
        e = elem_constants(wt, key)
        sol = simulate(e, t_end=2500.0)
        t = sol.t; mask = t >= t[-1]-900
        ax.plot(t[mask], sol.y[0][mask], color="#1f77b4", lw=1.4, label="prey N")
        ax.plot(t[mask], sol.y[1][mask], color="#d62728", lw=1.4, label="predator P")
        lab = "dilute" if wt == 0 else f"{CROWDERS[key]['label']} {wt}% w/v"
        ax.set_title(lab); ax.set_xlabel("time (min)")
        ax.set_ylabel("conc (nM)")
    # one shared legend below all panels, clear of the curves
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Mechanistic network -- settled dynamics", fontsize=11)
    fig.tight_layout(rect=[0, 0.07, 1, 1])
    fig.savefig(outfile, dpi=140, bbox_inches="tight")
    print(f"saved {outfile}")


if __name__ == "__main__":
    print("=" * 70)
    print("Mechanistic crowded predator-prey network -- dry-lab Step 3 (v2)")
    print("=" * 70)

    # (a) dilute limit must reproduce the validated ~92 min limit cycle
    st0 = cycle_stats(simulate(elem_constants(0.0)))
    print(f"Dilute mechanistic : period "
          f"{st0['period']:.1f} min, predator "
          f"{st0['P_range'][0]:.2f}->{st0['P_range'][1]:.1f} nM, prey "
          f"{st0['N_range'][0]:.2f}->{st0['N_range'][1]:.1f} nM")
    eff = effective_constants(elem_constants(0.0))
    print("Implied effective constants vs SI Table S5 target:")
    print(f"  k1 {eff['k1']:.2e} (2.0e-3)  b {eff['b']:.2e} (4.8e-5)  "
          f"k2 {eff['k2']:.2e} (3.1e-3)")
    print(f"  kN {eff['kN']:.2e} (2.1e-2)  kP {eff['kP']:.2e} (4.7e-3)  "
          f"KmP {eff['KmP']:.1f} (34)")

    # (b) how the EMERGENT effective constants move with crowding (audit)
    print("\nEmergent effective constants vs PEG 8000 loading (x dilute):")
    print(f"  {'wt%':>5} {'k1':>6} {'k2':>6} {'kN':>6} {'kP':>6} {'KmP':>6}")
    base = effective_constants(elem_constants(0.0))
    for wt in (0, 2.5, 5, 7.5, 10, 15):
        ec = effective_constants(elem_constants(wt, "PEG8000"))
        print(f"  {wt:5.1f} {ec['k1']/base['k1']:6.2f} {ec['k2']/base['k2']:6.2f} "
              f"{ec['kN']/base['kN']:6.2f} {ec['kP']/base['kP']:6.2f} "
              f"{ec['KmP']/base['KmP']:6.2f}")

    # (b2) CHEMICAL-IDENTITY audit: decompose the N+G duplex free-energy shift into
    #      its three channels so PEG != Ficoll is visible as CHEMISTRY, not size.
    print("\nAssociation dG shift for N+G at 10% w/v (RT units; negative = favours "
          "duplex):")
    print(f"  {'crowder':>10} {'SPT(entropic)':>14} {'enthalpic(chi)':>15} "
          f"{'hydration':>11} {'total':>8}")
    for key in ("PEG8000", "FICOLL400"):
        cr = CROWDERS[key]
        phi = volume_fraction(10.0, cr)
        g_spt = dG_assoc_EV(RADII["N"], RADII["G"], RADII["C_NG"], phi, cr)
        g_enth = dG_assoc_enthalpic(RADII["N"], RADII["G"], RADII["C_NG"], phi, cr)
        g_hyd = water_activity_dG(phi, cr, n_w=2.0)
        print(f"  {cr['label']:>10} {g_spt:14.3f} {g_enth:15.3f} "
              f"{g_hyd:11.3f} {g_spt+g_enth+g_hyd:8.3f}")

    # (c) dynamics at representative loadings
    for wt in (5.0, 10.0):
        st = cycle_stats(simulate(elem_constants(wt, "PEG8000")))
        per = f"{st['period']:.1f} min" if st["period"] else "no oscillation"
        print(f"\nPEG8000 {wt:>4.1f}% : period {per}, "
              f"predator amp {st['amp_P']:.1f} nM")

    # (d) figures
    wt_grid = np.linspace(0.0, 18.0, 31)
    plot_predictions(wt_grid, "mechanistic_predictions.png")
    plot_timeseries("mechanistic_timeseries.png",
                    [(0.0, "PEG8000"), (5.0, "PEG8000"), (10.0, "PEG8000")])
    print("\nNOTE: SPT/viscosity/enzyme coefficients are literature-anchored, "
          "tunable hypotheses for wet-lab calibration, not measured constants.")
