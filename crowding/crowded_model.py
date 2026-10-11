"""
crowded_model.py
================
STEP 3 of the BIOMOD dry-lab plan: a mechanistic, bottom-up model of how
macromolecular crowding (PEG 8000 and Ficoll 400) reshapes the dynamics of the
Fujii & Rondelez (2013) DNA predator-prey oscillator.

DESIGN PRINCIPLE (do not violate)
---------------------------------
We do NOT change the equation *structure*. The dilute SI eqs 3-4 -- and in
particular the saturable-exonuclease term that is the verified oscillation
engine -- stay exactly as validated in `fujii_pp_model.py`. Crowding enters ONLY
by renormalizing the rate constants:

        k_i  ->  k_i * F_i(phi, M, identity)

Each crowding factor F_i is a product of dimensionless "channels", and each
channel is a function of a physical intermediate (volume fraction phi, mesh
size xi, scale-dependent viscosity, free-ion activity) taken from the
literature. This is the renormalization route the Undermind report identifies
as the only viable path: no paper models crowding in this oscillator directly,
so we take the PEN kinetic backbone and let crowding move specific parameters.

LITERATURE ANCHORS (see the companion Word document for full discussion)
-----------------------------------------------------------------------
  * Hybridization (PEG 8000): Baltierra-Jasso 2015 JACS -- k_close +4x, ddG
    -1.73 kcal/mol at 10% w/w PEG 8000 (STABILIZES duplex). Knowles 2011 PNAS
    -- large-PEG duplex m-value +0.156 kcal/molal, excluded-volume term on a
    bimolecular duplex ~12x that on a unimolecular hairpin.
  * Excluded volume / association: Minton SPT  ln(gamma) ~ phi/(1-phi);
    rate enhancement k/k0 = gamma_A gamma_B / gamma_TS ~ exp(alpha phi/(1-phi));
    Berezhkovskii-Szabo 2016 -- depletion Boltzmann factor exp(beta dU).
  * Polymerase/nickase processivity: Akabayov 2013 Nat Commun ~2-4x net
    replication at 4% PEG (compaction + salt-resistance). Sasaki 2006 -- Pol
    binding up, intrinsic kcat down. Sasaki 2007 -- ENDOnucleases (the Nb.BsmI
    nicking arm) enhanced.
  * Exonuclease catalysis (ttRecJ): Sasaki 2007 NAR -- the exonuclease Exo I
    inhibited ~5.5x in Vmax (not Km) at 20% w/w PEG 8000. Direct class+crowder
    match for ttRecJ. NOTE: Km ~ unchanged for nucleases (Vmax effect only).
  * Viscosity / diffusion: Holyst 2009 PCCP scale-dependent viscosity
    eta_eff/eta0 = exp[b (R_eff/xi)^a], R_eff^-2 = R_h^-2 + r_probe^-2, a~0.78,
    b~1.61 (PEG); xi = Rg (c/c*)^-0.75. (a,b are Holyst-family values, PEG 8000
    not directly fit -- flagged.)
  * Ion sequestration (optional channel): Bielec 2021 JPCL -- nonionic crowder
    sequesters cations (kappa ~0.49 /M), K_hyb ~ [Na+]^2.51. Parameterized for
    Na+, NOT Mg2+ -- OFF by default, exposed for exploration.
  * Identity (PEG vs Ficoll): Sung & Nesbitt 2021 + Homchaudhuri 2006 -- PEG is
    a flexible coil (de Gennes mesh + depletion, near-ideal toward DNA folding,
    enthalpic toward enzymes); Ficoll 400 is compact/quasi-spherical (hard-
    sphere excluded volume, NO mesh, milder). No primary Ficoll-400 datum exists
    in the surveyed set -- ALL Ficoll numbers are flagged extrapolations.

Every coefficient below is a documented, TUNABLE hypothesis to be fitted to
wet-lab calibration runs, not a measured constant. Defaults are deliberately
conservative.
------------------------------------------------------------------------------
"""

import numpy as np
from scipy.integrate import solve_ivp


# =============================================================================
# 0. DILUTE BASELINE  (mirrors the validated fujii_pp_model.py, SI Table S5 PP1)
#    Concentrations nM, time min. Self-contained so this file runs standalone.
# =============================================================================
BASELINE = {
    "k1":  2.0e-3,   # prey-growth rate constant   (nM^-2 min^-1)
    "b":   4.8e-5,   # prey-growth saturation       (nM^-2)
    "k2":  3.1e-3,   # predation rate constant      (nM^-2 min^-1)
    "kN":  2.1e-2,   # prey exonuclease decay       (nM^-1 min^-1)
    "kP":  4.7e-3,   # predator exonuclease decay   (nM^-1 min^-1)
    "KmP": 34.0,     # exonuclease M-M constant, P  (nM)
    "pol": 3.7,      # Bst polymerase               (nM)
    "rec": 32.5,     # ttRecJ exonuclease           (nM)
    "G":   140.0,    # template G1 (oscillation window ~80-200 nM)
}

T_CELSIUS = 46.5                      # Fujii PP1 operating temperature
RT_KCAL = 1.98720425e-3 * (T_CELSIUS + 273.15)   # kcal/mol, ~0.635 at 46.5 C


def fujii_rhs(t, y, p):
    """SI eqs 3-4, exactly -- structure never changes under crowding."""
    n, pred = max(y[0], 0.0), max(y[1], 0.0)
    pol, rec = p["pol"], p["rec"]
    growth = p["k1"] * pol * p["G"] * n / (1.0 + p["b"] * p["G"] * n)
    predation = p["k2"] * pol * n * pred
    sat = 1.0 + pred / p["KmP"]            # saturable ttRecJ sink = the engine
    decay_n = rec * p["kN"] * n / sat
    decay_p = rec * p["kP"] * pred / sat
    return [growth - predation - decay_n, predation - decay_p]


def simulate(params, n0=10.0, p0=30.0, t_end=2500.0, n_eval=10000):
    t_eval = np.linspace(0.0, t_end, n_eval)
    return solve_ivp(fujii_rhs, (0.0, t_end), [n0, p0], args=(params,),
                     t_eval=t_eval, method="LSODA",
                     rtol=1e-9, atol=1e-12, max_step=2.0)


def cycle_stats(sol, tail_min=1000.0):
    """Period (min) and peak-to-peak amplitudes of the settled cycle."""
    t, (n, pred) = sol.t, sol.y
    mask = t >= (t[-1] - tail_min)
    tn, nn, pp = t[mask], n[mask], pred[mask]
    peaks = [i for i in range(1, len(pp) - 1)
             if pp[i] > pp[i - 1] and pp[i] > pp[i + 1] and pp[i] > pp.mean()]
    period = float(np.mean(np.diff(tn[peaks]))) if len(peaks) >= 2 else None
    return {
        "period": period,
        "amp_P": float(pp.max() - pp.min()),
        "amp_N": float(nn.max() - nn.min()),
        "P_range": (float(pp.min()), float(pp.max())),
        "N_range": (float(nn.min()), float(nn.max())),
    }


# =============================================================================
# 1. CROWDER LIBRARY  --  Layer-0 identity + geometry
#    All radii in nm. v_bar = partial specific volume (mL/g) -> phi = v_bar * c.
# =============================================================================
CROWDERS = {
    "PEG8000": {
        "label": "PEG 8000",
        "kind": "coil",          # flexible random coil -> de Gennes mesh
        "M": 8000.0,             # g/mol
        "v_bar": 0.83,           # mL/g  (PEG partial specific volume)
        "R_h": 2.5,              # nm    hydrodynamic radius of PEG 8000
        "R_g": 3.4,              # nm    radius of gyration (R_g ~ 1.3-1.5 R_h coil)
        "monomer_M": 44.0,       # g/mol ethylene-oxide repeat (for ion channel)
        # --- channel strengths (per unit phi unless noted); tunable hypotheses
        "s_hyb": 16.7,           # hybridization: ln(4)/0.083 from Baltierra-Jasso
        "alpha_EV": 3.0,         # excluded-volume/depletion association enhancer
        "rho_proc": 4.0,         # polymerase+nickase processivity (Akabayov-scale)
        "e_exo": 10.3,           # exonuclease inhibition: ln(5.5)/0.166, Sasaki
        "visc_a": 0.78,          # Holyst exponent (semidilute)
        "visc_b": 1.61,          # Holyst PEG-family prefactor
    },
    "FICOLL400": {
        "label": "Ficoll 400",
        "kind": "sphere",        # compact quasi-sphere -> hard-sphere, NO mesh
        "M": 400000.0,
        "v_bar": 0.67,           # mL/g
        "R_h": 10.0,             # nm    Ficoll 400 hydrodynamic radius
        "R_g": 10.0,             # nm    (compact -> R_g ~ R_h)
        "monomer_M": 350.0,      # sucrose/epichlorohydrin repeat (rough)
        # ALL Ficoll channel strengths are FLAGGED EXTRAPOLATIONS (no primary
        # Ficoll-400 datum in the surveyed papers). Set milder than PEG: compact
        # excluded-volume crowder, near-ideal toward DNA, weaker enzyme effects.
        "s_hyb": 6.0,            # excluded-volume-only stabilization (Ghosh 2019)
        "alpha_EV": 2.0,         # milder (Homchaudhuri: Ficoll < dextran)
        "rho_proc": 3.0,
        "e_exo": 5.0,            # extrapolated, weaker exonuclease inhibition
        "visc_a": 1.0,           # not a coil -> Mooney hard-sphere law used instead
        "visc_b": 2.5,           # intrinsic viscosity of spheres
    },
}

# Probe (reactant/enzyme) sizes felt by the viscosity channel, nm.
PROBE_RADII = {
    "pol": 3.0,    # Bst polymerase  (~67 kDa)
    "exo": 2.8,    # ttRecJ          (~50 kDa)
    "dna": 1.2,    # short ssDNA species N / P
}


# =============================================================================
# 2. PHYSICAL INTERMEDIATES  --  Layer 1
# =============================================================================
def volume_fraction(wt_pct, cr):
    """phi = v_bar[mL/g] * c[g/mL];  c[g/mL] = wt_pct/100  (w/v)."""
    return cr["v_bar"] * (wt_pct / 100.0)


def overlap_wt_pct(cr):
    """Overlap concentration c* expressed as w/v %.  c* ~ 3M / (4 pi NA Rg^3)."""
    NA = 6.022e23
    Rg_cm = cr["R_g"] * 1e-7
    c_star_g_per_cm3 = 3.0 * cr["M"] / (4.0 * np.pi * NA * Rg_cm**3)
    return c_star_g_per_cm3 * 100.0          # g/cm^3 -> w/v %


def correlation_length(wt_pct, cr):
    """de Gennes semidilute mesh for coils:  xi = Rg (c/c*)^-0.75.

    The screening length diverges as c -> 0 (chains far apart, no mesh), so we
    do NOT clamp to R_g: that divergence is exactly what makes the viscosity
    factor relax to 1 in the dilute limit. At c = c* we recover xi = R_g; above
    c* the mesh shrinks below R_g (true semidilute). For compact spheres the
    mesh concept does not apply and R_g is the only length scale."""
    if cr["kind"] != "coil" or wt_pct <= 0.0:
        return cr["R_g"]
    c_star = overlap_wt_pct(cr)
    return cr["R_g"] * (wt_pct / c_star) ** (-0.75)


def viscosity_factor(wt_pct, cr, probe_radius):
    """eta_eff(probe)/eta0 felt by a species of radius `probe_radius` (nm).

    Coils (PEG): Holyst scale-dependent form  exp[b (R_eff/xi)^a],
                 R_eff^-2 = R_h^-2 + r_probe^-2  -> small species ~ solvent,
                 big enzymes ~ macroviscosity.
    Spheres (Ficoll): Mooney hard-sphere law   exp[ [eta] phi / (1 - phi/phi_max) ].
    """
    if wt_pct <= 0.0:
        return 1.0                             # dilute limit: no enhancement
    phi = volume_fraction(wt_pct, cr)
    if cr["kind"] == "coil":
        xi = correlation_length(wt_pct, cr)
        R_eff = 1.0 / np.sqrt(1.0 / cr["R_h"]**2 + 1.0 / probe_radius**2)
        return float(np.exp(cr["visc_b"] * (R_eff / xi) ** cr["visc_a"]))
    phi_max = 0.6                              # random close packing of spheres
    phi = min(phi, 0.95 * phi_max)
    return float(np.exp(cr["visc_b"] * phi / (1.0 - phi / phi_max)))


def free_ion_fraction(wt_pct, cr, kappa=0.49):
    """Bielec ion-sequestration: free [cation] / total after complexation by
    crowder monomers.  c_monomer[M] = (phi * rho_polymer) / monomer_M.
    rho_polymer ~ 1.2 g/mL.  Returns the surviving free-ion fraction in [0,1].
    (OFF by default; Na+-parameterized, Mg2+ extrapolation flagged.)"""
    phi = volume_fraction(wt_pct, cr)
    c_monomer = (phi * 1200.0) / cr["monomer_M"]      # mol/L
    return 1.0 / (1.0 + kappa * c_monomer)


# =============================================================================
# 3. CROWDING CHANNELS  --  Layer 2 (log-space contributions at given wt%)
#    Each channel returns a *log* multiplier; the per-parameter factor is
#    exp(sum of weighted channel logs).  Weights encode how strongly each
#    reaction step couples to each physical channel (0, 0.5, 1).
# =============================================================================
def channel_logs(wt_pct, cr, use_ion=False):
    """Return the log-contribution of every crowding channel at `wt_pct`."""
    phi = volume_fraction(wt_pct, cr)
    Q = phi / (1.0 - phi)                      # SPT variable phi/(1-phi)

    logs = {
        # thermodynamic: net DNA hybridization stabilization (PEG large -> +)
        "HYB": cr["s_hyb"] * phi,
        # excluded-volume / depletion enhancement of association & binding (+)
        "EV": cr["alpha_EV"] * Q,
        # polymerase + nickase processivity / net replication boost (+)
        "PROC": cr["rho_proc"] * phi,
        # exonuclease (ttRecJ) catalytic inhibition -- Vmax down (-)
        "EXO": -cr["e_exo"] * phi,
        # viscosity / diffusion slowdown at the relevant probe size (-),
        # filled per-parameter below because the probe differs by enzyme
        "ION": 0.0,
    }
    if use_ion:
        # K_hyb ~ [cation]^2.51 ; destabilizes as free ions are sequestered (-)
        logs["ION"] = 2.51 * np.log(free_ion_fraction(wt_pct, cr))
    return logs


# Weight matrix: how strongly each rate constant couples to each channel.
# Rows = renormalized parameters; columns = channels. VISC handled separately
# (probe-size specific). Documented in the Word doc (Layer-2 table).
WEIGHTS = {
    #          HYB   EV   PROC  EXO   ION
    "k1":  {"HYB": 0.5, "EV": 0.5, "PROC": 1.0, "EXO": 0.0, "ION": 1.0},
    "k2":  {"HYB": 1.0, "EV": 1.0, "PROC": 0.5, "EXO": 0.0, "ION": 1.0},
    "kN":  {"HYB": 0.0, "EV": 0.2, "PROC": 0.0, "EXO": 1.0, "ION": 0.0},
    "kP":  {"HYB": 0.0, "EV": 0.2, "PROC": 0.0, "EXO": 1.0, "ION": 0.0},
    "KmP": {"HYB": 0.0, "EV": 0.0, "PROC": 0.0, "EXO": 0.0, "ION": 0.0},  # flat
    "b":   {"HYB": 0.0, "EV": 0.0, "PROC": 0.0, "EXO": 0.0, "ION": 0.0},
}

# Which probe's viscosity each parameter feels, and the VISC coupling weight.
VISC_COUPLING = {
    "k1":  ("pol", 1.0),
    "k2":  ("pol", 1.0),
    # Sasaki 2007 found the exonuclease crowding effect is on Vmax (catalysis),
    # NOT on diffusion -- so viscosity does NOT couple to the death terms. The
    # k_N/k_P suppression comes entirely from the EXO catalytic channel.
    "kN":  ("exo", 0.0),
    "kP":  ("exo", 0.0),
    "KmP": ("exo", 0.0),
    "b":   ("dna", 0.0),
}


def crowded_params(wt_pct, crowder_key, baseline=BASELINE, use_ion=False):
    """Return a NEW parameter dict with every rate constant renormalized for
    crowding at `wt_pct` of `crowder_key`. Baseline is never mutated."""
    cr = CROWDERS[crowder_key]
    logs = channel_logs(wt_pct, cr, use_ion=use_ion)
    out = dict(baseline)                      # immutable: copy, never mutate
    for param, w in WEIGHTS.items():
        log_factor = sum(w[ch] * logs[ch] for ch in logs)
        probe, wv = VISC_COUPLING[param]
        if wv > 0.0:
            log_factor -= wv * np.log(viscosity_factor(wt_pct, cr,
                                                        PROBE_RADII[probe]))
        out[param] = baseline[param] * float(np.exp(log_factor))
    return out


def crowding_factors(wt_pct, crowder_key, use_ion=False):
    """Convenience: the bare multiplicative factor F_i applied to each k_i."""
    base, cw = BASELINE, crowded_params(wt_pct, crowder_key, use_ion=use_ion)
    return {k: cw[k] / base[k] for k in ("k1", "k2", "kN", "kP", "KmP", "b")}


# =============================================================================
# 4. PREDICTIONS  --  Layer 3 (sweep -> period / amplitude / Hopf boundary)
# =============================================================================
def sweep_concentration(crowder_key, wt_grid, use_ion=False, t_end=3000.0):
    """Period & predator amplitude vs crowder wt% for one crowder."""
    periods, amps = [], []
    for wt in wt_grid:
        p = crowded_params(wt, crowder_key, use_ion=use_ion)
        st = cycle_stats(simulate(p, t_end=t_end, n_eval=int(t_end * 4)),
                         tail_min=1200.0)
        periods.append(st["period"] if st["period"] else np.nan)
        amps.append(st["amp_P"])
    return np.array(periods), np.array(amps)


def oscillation_window(crowder_key, wt_grid, amp_thresh=1.0, use_ion=False):
    """Range of wt% over which the system still oscillates (amp > threshold).
    Detecting whether crowding pushes the system across the Hopf boundary is the
    headline falsifiable prediction."""
    _, amps = sweep_concentration(crowder_key, wt_grid, use_ion=use_ion)
    osc = wt_grid[amps > amp_thresh]
    return (float(osc.min()), float(osc.max())) if len(osc) else None


# =============================================================================
# 5. PLOTS + CLI
# =============================================================================
def plot_factor_breakdown(crowder_key, wt_grid, outfile):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    labels = {"k1": "k1 prey growth", "k2": "k2 predation",
              "kN": "kN prey decay", "kP": "kP predator decay"}
    colors = {"k1": "#1f77b4", "k2": "#2ca02c",
              "kN": "#d62728", "kP": "#9467bd"}
    for k, lab in labels.items():
        F = [crowding_factors(wt, crowder_key)[k] for wt in wt_grid]
        ax.plot(wt_grid, F, "-", lw=1.8, color=colors[k], label=lab)
    ax.axhline(1.0, color="k", lw=0.7, ls="--")
    ax.set_xlabel(f"{CROWDERS[crowder_key]['label']} concentration (% w/v)")
    ax.set_ylabel("crowding factor  F_i  (x dilute value)")
    ax.set_yscale("log")
    ax.set_title(f"Rate-constant renormalization vs crowding -- "
                 f"{CROWDERS[crowder_key]['label']}")
    ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(outfile, dpi=140)
    print(f"saved {outfile}")


def plot_period_prediction(wt_grid, outfile, use_ion=False):
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    for key, col in (("PEG8000", "#c47828"), ("FICOLL400", "#1f77b4")):
        per, amp = sweep_concentration(key, wt_grid, use_ion=use_ion)
        ax1.plot(wt_grid, per, "o-", ms=3, color=col,
                 label=CROWDERS[key]["label"])
        ax2.plot(wt_grid, amp, "o-", ms=3, color=col,
                 label=CROWDERS[key]["label"])
    ax1.set_xlabel("crowder concentration (% w/v)")
    ax1.set_ylabel("oscillation period (min)")
    ax1.set_title("Predicted period vs crowding")
    ax1.legend(frameon=False)
    ax2.axhline(1.0, color="k", lw=0.7, ls="--")
    ax2.set_xlabel("crowder concentration (% w/v)")
    ax2.set_ylabel("predator amplitude (nM, peak-to-peak)")
    ax2.set_title("Predicted amplitude vs crowding (Hopf on/off)")
    ax2.legend(frameon=False)
    fig.suptitle("Crowded Fujii PP1 -- falsifiable predictions "
                 "(PEG 8000 vs Ficoll 400)", fontsize=11)
    fig.tight_layout(); fig.savefig(outfile, dpi=140)
    print(f"saved {outfile}")


def report_factor_table(crowder_key, wt_points):
    cr = CROWDERS[crowder_key]
    print(f"\nCrowding factors -- {cr['label']}  (x dilute value)")
    print(f"  {'wt%':>5} {'phi':>6} {'k1':>7} {'k2':>7} {'kN':>7} {'kP':>7}")
    for wt in wt_points:
        f = crowding_factors(wt, crowder_key)
        phi = volume_fraction(wt, cr)
        print(f"  {wt:5.1f} {phi:6.3f} {f['k1']:7.2f} {f['k2']:7.2f} "
              f"{f['kN']:7.2f} {f['kP']:7.2f}")


if __name__ == "__main__":
    print("=" * 70)
    print("Crowded Fujii predator-prey oscillator -- dry-lab Step 3")
    print("=" * 70)

    # (a) sanity: dilute limit must reproduce the validated baseline
    st0 = cycle_stats(simulate(BASELINE))
    print(f"Dilute baseline   : period {st0['period']:.1f} min, "
          f"predator {st0['P_range'][0]:.1f}->{st0['P_range'][1]:.1f} nM")
    f_dilute = crowding_factors(0.0, "PEG8000")
    assert all(abs(v - 1.0) < 1e-9 for v in f_dilute.values()), \
        "crowding factors must be 1.0 at zero crowder"
    print("Zero-crowder check: all F_i = 1.000  (reduces to dilute model) OK")

    # (b) how the rate constants move with crowding
    report_factor_table("PEG8000", [0, 2.5, 5, 7.5, 10, 15])
    report_factor_table("FICOLL400", [0, 2.5, 5, 7.5, 10, 15])

    # (c) dynamics at a representative PEG loading
    for wt in (5.0, 10.0):
        st = cycle_stats(simulate(crowded_params(wt, "PEG8000")))
        per = f"{st['period']:.1f} min" if st["period"] else "no oscillation"
        print(f"\nPEG8000 {wt:>4.1f}% w/v : period {per}, "
              f"predator amp {st['amp_P']:.1f} nM")

    # (d) figures + oscillation windows
    wt_grid = np.linspace(0.0, 18.0, 31)
    plot_factor_breakdown("PEG8000", wt_grid, "crowding_factors_peg.png")
    plot_period_prediction(wt_grid, "crowding_period_prediction.png")
    for key in ("PEG8000", "FICOLL400"):
        win = oscillation_window(key, wt_grid)
        msg = (f"{win[0]:.1f}-{win[1]:.1f}% w/v" if win else "none in range")
        print(f"oscillation window ({CROWDERS[key]['label']:>11}): {msg}")
    print("\nNOTE: every coefficient is a literature-anchored, tunable "
          "hypothesis to be fit to wet-lab calibration, not a measured value.")
