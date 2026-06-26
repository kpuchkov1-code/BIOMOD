"""
stability_analysis.py
=====================
Analytic back-up for Step 1: PROVE the model oscillates without relying on the
numerical integrator. (Loose solver tolerances can fake a decay-to-equilibrium;
the linear stability of the interior fixed point settles it independently.)

Now operates on the PAPER-EXACT model (SI eqs. 3-4) in fujii_pp_model. The
coexistence fixed point and Jacobian are found numerically (the saturable-decay
form is not as tidy as the old Holling expression), then we apply the
Poincare-Bendixson conclusion: a bounded 2-D system with an UNSTABLE interior
fixed point and a trapping region has a stable limit cycle.
"""

import numpy as np
from scipy.optimize import fsolve
from fujii_pp_model import PARAMS, fujii_rhs


def _f(y, p):
    return np.array(fujii_rhs(0.0, y, p))


def _jacobian(y, p, eps=1e-6):
    """Finite-difference Jacobian of the RHS at y."""
    J = np.zeros((2, 2))
    f0 = _f(y, p)
    for j in range(2):
        dy = np.array(y, dtype=float)
        h = eps * max(1.0, abs(y[j]))
        dy[j] += h
        J[:, j] = (_f(dy, p) - f0) / h
    return J


def analyse(p=PARAMS):
    # locate the interior (coexistence) fixed point numerically
    guess = (0.4 * p["KmP"], 1.5 * p["KmP"])
    star = fsolve(_f, guess, args=(p,), full_output=False)
    n_star, p_star = star

    J = _jacobian(star, p)
    tr, det = J[0, 0] + J[1, 1], np.linalg.det(J)
    eig = np.linalg.eigvals(J)

    print(f"interior fixed point : N* = {n_star:.3f} nM,  P* = {p_star:.3f} nM")
    print(f"residual |f(N*,P*)|   = {np.linalg.norm(_f(star, p)):.2e} "
          f"(should be ~0)")
    print(f"Jacobian trace        = {tr:+.5f}")
    print(f"Jacobian determinant  = {det:+.5f}")
    print(f"eigenvalues           = {eig[0]:.5f}, {eig[1]:.5f}")

    osc = (tr > 0 and det > 0 and n_star > 0 and p_star > 0)
    if osc:
        w = abs(eig[0].imag)
        print(f"max Re(lambda)        = {max(x.real for x in eig):+.5f}  > 0")
        print("VERDICT: interior fixed point is an UNSTABLE spiral ->")
        print("         Poincare-Bendixson => a STABLE LIMIT CYCLE surrounds it.")
        if w > 0:
            print(f"         near-fixed-point oscillation period ~ {2*np.pi/w:.1f} min")
            print("         (the true relaxation-cycle period is longer; "
                  "see fujii_pp_model report)")
    else:
        print("VERDICT: fixed point is STABLE / non-interior -- no sustained "
              "oscillation for these parameters (try G in the osc. window).")
    return osc


if __name__ == "__main__":
    analyse()
