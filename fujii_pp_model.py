"""
fujii_pp_model.py
=================
STEP 1 of the dry-lab plan: reproduce the Fujii & Rondelez (2013, ACS Nano)
DNA predator-prey oscillator *in silico*.

>>> THIS IS THE PAPER-EXACT MODEL. <<<
It encodes the Supporting-Information model (SI eqs. 3-4) with the SI's
*measured* kinetic parameters (Table S5, PP1, standard conditions). It replaces
an earlier placeholder (Rosenzweig-MacArthur / Holling-II) version that
oscillated for the WRONG mechanistic reason. The differences matter:

  term        placeholder (old, WRONG)        Fujii SI (this file, eqs 3-4)
  ---------   -----------------------------   ---------------------------------
  prey growth logistic  r*N*(1-N/K)           saturating  k1*pol*G*N/(1+b*G*N)
  predation   Holling-II a*N*P/(1+a*h*N)      LINEAR mass action  k2*pol*N*P
  death       linear  -m*N , -m*P             SATURABLE Michaelis-Menten
                                              rec*kP*P/(1+P/Km,P)  (enzyme sink)

The crucial point the paper proves (SI Fig. S3 vs S5): with first-order
(linear) degradation the system can ONLY damp to a fixed point. It is the
SATURABLE exonuclease degradation -- ttRecJ being a limited catalytic resource
that the predator can swamp -- that creates the sustained limit cycle. The
predation functional response is LINEAR. So the oscillation engine here is the
saturable decay term, not the predation term.

Reference: Fujii & Rondelez, "Predator-Prey Molecular Ecosystems", ACS Nano
7(1):27-34 (2013), Supporting Information, sections S3-S4.
------------------------------------------------------------------------------
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# Measured kinetic parameters -- SI Table S5, PP1, "optimized" column for the
# standard-conditions experiments of Fig. 2 / S11 (rec = 32.5 nM).
# Units: concentrations nM, time min. Every value is from the paper.
# -----------------------------------------------------------------------------
PARAMS = {
    "k1":  2.0e-3,   # [SI S5] prey-growth rate constant   (nM^-2 min^-1)
    "b":   4.8e-5,   # [SI S5] prey-growth saturation       (nM^-2)
    "k2":  3.1e-3,   # [SI S5] predation rate constant      (nM^-2 min^-1)
    "kN":  2.1e-2,   # [SI S5] prey first-order decay       (nM^-1 min^-1)
    "kP":  4.7e-3,   # [SI S5] predator first-order decay   (nM^-1 min^-1)
    "KmP": 34.0,     # [SI S5] exonuclease M-M constant, P  (nM)
    # --- "standard conditions" enzyme levels (SI Methods) ---
    "pol": 3.7,      # [SI] Bst polymerase                  (nM)
    "rec": 32.5,     # [SI] ttRecJ exonuclease              (nM)
    # --- the experimental control knob: template concentration ---
    "G":   140.0,    # [SI] grass template G1; osc. window ~80-200 nM (Fig S11)
}

# Initial conditions (nM) -- a representative SI Fig. S2 start.
N0 = 10.0   # [SI] initial prey
P0 = 30.0   # [SI] initial predator

# The limit cycle is a sharp relaxation oscillation; integrate long to settle,
# then analyse / show only the settled tail.
T_END = 2500.0
N_EVAL = 12000
TAIL_MIN = 1000.0


# -----------------------------------------------------------------------------
# The ODE right-hand side -- SI eqs. (3) and (4), exactly.
# -----------------------------------------------------------------------------
def fujii_rhs(t, y, p):
    n, pred = max(y[0], 0.0), max(y[1], 0.0)
    pol, rec = p["pol"], p["rec"]

    # prey growth: saturating in G*N (Pol+Nic replication on template G)
    growth = p["k1"] * pol * p["G"] * n / (1.0 + p["b"] * p["G"] * n)
    # predation: LINEAR mass action (predator copies itself on prey, eats it)
    predation = p["k2"] * pol * n * pred
    # saturable exonuclease (ttRecJ) -- shared sink; prey decay is competitively
    # inhibited by predator (the 1/(1+P/Km,P) factor). This is the term that
    # makes the system oscillate (SI Fig. S5).
    sat = 1.0 + pred / p["KmP"]
    decay_n = rec * p["kN"] * n / sat
    decay_p = rec * p["kP"] * pred / sat

    dn = growth - predation - decay_n
    dp = predation - decay_p
    return [dn, dp]


def simulate(params=PARAMS, n0=N0, p0=P0, t_end=T_END, n_eval=N_EVAL):
    t_eval = np.linspace(0.0, t_end, n_eval)
    # LSODA auto-switches to a stiff solver across the sharp predator spikes.
    # Tight tolerances + a step cap keep the relaxation cycle from being faked
    # into a decay (the lesson from the old placeholder model still applies).
    sol = solve_ivp(
        fujii_rhs, (0.0, t_end), [n0, p0],
        args=(params,), t_eval=t_eval,
        method="LSODA", rtol=1e-9, atol=1e-12, max_step=2.0,
    )
    return sol


# -----------------------------------------------------------------------------
# Nondimensionalisation -- SELF-CHECK against the paper.
# Reproduces SI definitions and must match SI Table S3 (PP1):
#   beta = 8.7e-2,  lambda = 4.5,  delta = 0.39,  G0 = 53 nM,  tc = 2.6 min
# -----------------------------------------------------------------------------
def nondimensional(p=PARAMS):
    G0 = p["k2"] * p["KmP"] / p["k1"]
    tc = 1.0 / (p["k2"] * p["pol"] * p["KmP"])
    beta = p["b"] * p["k2"] * p["KmP"] ** 2 / p["k1"]
    lam = p["kN"] / p["kP"]
    delta = (p["rec"] / p["pol"]) * (p["kP"] / (p["k2"] * p["KmP"]))
    g = p["G"] / G0
    return dict(beta=beta, lam=lam, delta=delta, G0=G0, tc=tc, g=g)


def check_against_paper(p=PARAMS):
    nd = nondimensional(p)
    ref = dict(beta=8.7e-2, lam=4.5, delta=0.39, G0=53.0, tc=2.6)  # SI Table S3
    print("Nondimensional self-check vs SI Table S3 (PP1):")
    print(f"  beta   = {nd['beta']:.3e}   (paper 8.7e-2)")
    print(f"  lambda = {nd['lam']:.3f}      (paper 4.5)")
    print(f"  delta  = {nd['delta']:.3f}      (paper 0.39)")
    print(f"  G0     = {nd['G0']:.1f} nM    (paper 53)")
    print(f"  tc     = {nd['tc']:.2f} min   (paper 2.6)")
    print(f"  -> g = G/G0 = {p['G']:.0f}/{nd['G0']:.0f} = {nd['g']:.2f}  "
          f"(oscillation window roughly g in [1.5, 4])")
    ok = (abs(nd["beta"] - ref["beta"]) / ref["beta"] < 0.1 and
          abs(nd["lam"] - ref["lam"]) / ref["lam"] < 0.1 and
          abs(nd["delta"] - ref["delta"]) / ref["delta"] < 0.1)
    print("  RESULT:", "MATCH -- implementation is faithful to the SI."
          if ok else "MISMATCH -- check the parameters/derivation.")
    return ok


# -----------------------------------------------------------------------------
# Period / amplitude of the settled cycle
# -----------------------------------------------------------------------------
def cycle_stats(sol, tail_min=TAIL_MIN):
    t, (n, pred) = sol.t, sol.y
    mask = t >= (t[-1] - tail_min)
    tn, nn, pp = t[mask], n[mask], pred[mask]
    peaks = [i for i in range(1, len(pp) - 1)
             if pp[i] > pp[i - 1] and pp[i] > pp[i + 1] and pp[i] > pp.mean()]
    period = None
    if len(peaks) >= 2:
        period = float(np.mean(np.diff(tn[peaks])))
    return dict(period=period,
                n_range=(float(nn.min()), float(nn.max())),
                p_range=(float(pp.min()), float(pp.max())))


# -----------------------------------------------------------------------------
# Bifurcation sweep over template G -- reproduces the onset of oscillations
# (SI Fig. S11): fixed point -> oscillation -> damped, as G increases.
# -----------------------------------------------------------------------------
def bifurcation_over_G(g_values, params=PARAMS, t_end=3000.0, tail_min=1200.0):
    amp = []
    for G in g_values:
        p = dict(params, G=float(G))
        sol = simulate(p, t_end=t_end, n_eval=int(t_end * 4))
        st = cycle_stats(sol, tail_min=tail_min)
        amp.append(st["p_range"][1] - st["p_range"][0])  # predator peak-to-peak
    return np.array(amp)


# -----------------------------------------------------------------------------
# Plots
# -----------------------------------------------------------------------------
def plot_reproduction(sol, outfile="fujii_reproduction.png"):
    t, (n, pred) = sol.t, sol.y
    mask = t >= (t[-1] - TAIL_MIN)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    ax1.plot(t[mask], n[mask], label="Prey  N", color="#1f77b4", lw=1.6)
    ax1.plot(t[mask], pred[mask], label="Predator  P", color="#d62728", lw=1.6)
    ax1.set_xlabel("time (min)")
    ax1.set_ylabel("concentration (nM)")
    ax1.set_title(f"Settled oscillation (last {TAIL_MIN:.0f} min)")
    ax1.legend(frameon=False)

    ax2.plot(n, pred, color="#2ca02c", lw=0.9)
    ax2.plot(n[0], pred[0], "ko", ms=5, label="start")
    ax2.set_xlabel("Prey  N (nM)")
    ax2.set_ylabel("Predator  P (nM)")
    ax2.set_title("Phase portrait (limit cycle)")
    ax2.legend(frameon=False)

    fig.suptitle("Fujii & Rondelez PP1 -- in-silico reproduction "
                 "(SI eqs 3-4, Table S5 measured parameters)", fontsize=11)
    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    print(f"saved {outfile}")


def plot_bifurcation(g_values, amp, outfile="bifurcation_G.png"):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(g_values, amp, "o-", color="#9467bd", ms=4, lw=1.2)
    ax.set_xlabel("template G1 (nM)")
    ax.set_ylabel("predator oscillation amplitude (nM, peak-to-peak)")
    ax.set_title("Onset of oscillations vs template (cf. SI Fig. S11)")
    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    print(f"saved {outfile}")


def report(sol):
    st = cycle_stats(sol)
    if st["period"]:
        print(f"  measured predator period : {st['period']:.1f} min")
    print(f"  settled prey   range (nM) : "
          f"{st['n_range'][0]:.1f} -> {st['n_range'][1]:.1f}")
    print(f"  settled predator range(nM): "
          f"{st['p_range'][0]:.1f} -> {st['p_range'][1]:.1f}")


if __name__ == "__main__":
    print("=" * 64)
    ok = check_against_paper()
    print("=" * 64)
    sol = simulate()
    print("Simulation status:", sol.message)
    report(sol)
    plot_reproduction(sol)

    print("-" * 64)
    print("Bifurcation sweep over template G1 (this takes a moment)...")
    g_values = np.arange(40.0, 261.0, 10.0)
    amp = bifurcation_over_G(g_values)
    plot_bifurcation(g_values, amp)
    osc = g_values[amp > 1.0]
    if len(osc):
        print(f"  oscillations for G1 ~ {osc.min():.0f}-{osc.max():.0f} nM "
              f"(paper: ~80-200 nM, Fig S11)")
