"""
sensitivity_analysis.py
=======================
STEP 2 of the dry-lab plan: figure out WHICH parameters control the
oscillation, so you know which knobs molecular crowding has to turn to matter.

Two analyses, both runnable before any wet-lab work:

  (A) One-at-a-time parameter sweeps -> how period & amplitude respond to each
      rate constant. Identifies the "sensitive" parameters.

  (B) Phase-plane / nullclines -> shows the limit cycle and the fixed point,
      the geometric picture of why it oscillates.

These reuse the paper-exact model in fujii_pp_model.py (SI eqs 3-4, measured
Table S5 parameters), so any change there flows through automatically.
"""

import numpy as np
import matplotlib.pyplot as plt

from fujii_pp_model import PARAMS, simulate, fujii_rhs


# -----------------------------------------------------------------------------
# (A) One-at-a-time sensitivity: period & amplitude vs each parameter
# -----------------------------------------------------------------------------
def oscillation_metrics(sol):
    """Return (period, prey_amplitude) from the post-transient tail."""
    t, (n, _) = sol.t, sol.y
    half = len(t) // 2
    tn, nn = t[half:], n[half:]
    amp = nn.max() - nn.min()
    peaks = [i for i in range(1, len(nn) - 1)
             if nn[i] > nn[i - 1] and nn[i] > nn[i + 1] and nn[i] > nn.mean()]
    period = float(np.mean(np.diff(tn[peaks]))) if len(peaks) >= 2 else np.nan
    return period, amp


def sweep(param_name, factors=np.linspace(0.5, 1.5, 11)):
    base = PARAMS[param_name]
    periods, amps = [], []
    for f in factors:
        p = dict(PARAMS)
        p[param_name] = base * f
        per, amp = oscillation_metrics(simulate(params=p))
        periods.append(per)
        amps.append(amp)
    return factors, np.array(periods), np.array(amps)


def run_sensitivity(outfile="sensitivity.png"):
    names = list(PARAMS.keys())
    fig, axes = plt.subplots(2, len(names), figsize=(3.2 * len(names), 6.5),
                             sharex=True)
    print("Sensitivity sweep (+/-50% around SI Table S5 values):")
    for j, name in enumerate(names):
        factors, periods, amps = sweep(name)
        axes[0, j].plot(factors, periods, "o-", color="#1f77b4")
        axes[0, j].set_title(name)
        axes[1, j].plot(factors, amps, "o-", color="#d62728")
        axes[1, j].set_xlabel(f"{name} / base")
        # crude sensitivity score: fractional change in period across the sweep
        finite = periods[np.isfinite(periods)]
        score = (np.nanmax(periods) - np.nanmin(periods)) / np.nanmean(periods) \
            if finite.size else np.nan
        print(f"  {name:8s}  period sensitivity index = {score:.2f}")
    axes[0, 0].set_ylabel("period (min)")
    axes[1, 0].set_ylabel("prey amplitude (nM)")
    fig.suptitle("One-at-a-time sensitivity — which knobs matter "
                 "(target these for crowding)", fontsize=11)
    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    print(f"saved {outfile}")


# -----------------------------------------------------------------------------
# (B) Phase plane with nullclines + vector field
# -----------------------------------------------------------------------------
def run_phase_plane(outfile="phase_plane.png", nmax=120, pmax=120):
    sol = simulate()
    n, pred = sol.y

    N, P = np.meshgrid(np.linspace(0.1, nmax, 26), np.linspace(0.1, pmax, 26))
    dN = np.zeros_like(N)
    dP = np.zeros_like(P)
    for i in range(N.shape[0]):
        for k in range(N.shape[1]):
            d = fujii_rhs(0.0, [N[i, k], P[i, k]], PARAMS)
            dN[i, k], dP[i, k] = d
    speed = np.hypot(dN, dP)

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.streamplot(N, P, dN, dP, color=speed, cmap="Greys", density=1.2,
                  linewidth=0.7, arrowsize=0.8)
    # nullclines (where dN=0 and dP=0) via contour of the RHS components
    ax.contour(N, P, dN, levels=[0], colors="#1f77b4", linewidths=2)
    ax.contour(N, P, dP, levels=[0], colors="#d62728", linewidths=2)
    ax.plot(n, pred, color="#2ca02c", lw=1.4, label="limit cycle")
    ax.set_xlabel("Prey  N (nM)")
    ax.set_ylabel("Predator  P (nM)")
    ax.set_title("Phase plane: nullclines (blue dN=0, red dP=0) + limit cycle")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    print(f"saved {outfile}")


if __name__ == "__main__":
    run_sensitivity()
    run_phase_plane()
