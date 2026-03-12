"""
Test L2 for double-log with alpha=1.5, lam=-1/20 at extreme points using mpmath.
"""
import mpmath
mpmath.mp.dps = 80

def eval_L2_full(x_v, t_v, c_v, N, s_v, alpha_v):
    """Evaluate L2 for double-log with general alpha."""
    x_v = mpmath.mpf(x_v)
    t_v = mpmath.mpf(t_v)
    c_v = mpmath.mpf(c_v)
    N_v = mpmath.mpf(N)
    s_v = mpmath.mpf(s_v)
    alpha_v = mpmath.mpf(alpha_v)
    lam_v = -1/N_v
    
    T = 1 + t_v
    X = 1 + x_v
    
    phi = (T * X)**(1/N_v)
    
    psi_t = -1/T
    psi_x = -1/X
    psi_tt = 1/T**2
    psi_xx = 1/X**2
    
    box_psi = psi_tt - c_v**2 * psi_xx  # = 1/T^2 - c^2/X^2
    tilde_psi = psi_t**2 - c_v**2 * psi_x**2  # = 1/T^2 - c^2/X^2
    # For the double-log: box = tilde
    
    # phi derivatives
    phi_t = phi / (N_v * T)
    phi_x = phi / (N_v * X)
    phi_tt = phi / T**2 * (1 - N_v) / N_v**2
    phi_xx = phi / X**2 * (1 - N_v) / N_v**2
    
    # tilde_psi derivatives  
    tilde_psi_t = -2/T**3
    tilde_psi_x = 2*c_v**2/X**3
    tilde_psi_tt = 6/T**4
    tilde_psi_xx = -6*c_v**2/X**4
    
    # box_psi derivatives (same as tilde for double-log)
    box_psi_t = tilde_psi_t
    box_psi_x = tilde_psi_x
    box_psi_tt = tilde_psi_tt
    box_psi_xx = tilde_psi_xx
    
    # phi*tilde_psi second derivatives
    pt_tt = phi_tt*tilde_psi + 2*phi_t*tilde_psi_t + phi*tilde_psi_tt
    pt_xx = phi_xx*tilde_psi + 2*phi_x*tilde_psi_x + phi*tilde_psi_xx
    sq_pt = pt_tt - c_v**2 * pt_xx
    
    # phi*box_psi second derivatives (same as above for double-log)
    pb_tt = pt_tt  # same as above since box = tilde
    pb_xx = pt_xx
    sq_pb = sq_pt
    
    # Term 1: (1/2)*((alpha-1)*s*lam*sq_pb - s*lam^2*sq_pt)
    term1 = mpmath.mpf('0.5') * ((alpha_v - 1)*s_v*lam_v*sq_pb - s_v*lam_v**2*sq_pt)
    # = (1/2)*s*lam*(alpha-1-lam)*sq_pt  (since sq_pb = sq_pt)
    
    # Term 2
    phi3 = phi**3
    term2a = s_v**3 * lam_v**3 * (alpha_v - 1) * phi3 * tilde_psi * box_psi
    term2b = -s_v**3 * lam_v**4 * phi3 * tilde_psi**2
    term2 = term2a + term2b
    # = s^3*lam^3*(alpha-1-lam)*phi^3*tilde^2  (since box=tilde)
    
    # Term 3: s^3*lam^3*(d/dt(phi^3*tilde*psi_t) + c^2*d/dx(phi^3*tilde*psi_x))
    phi3_t = 3*phi**2 * phi_t
    phi3_x = 3*phi**2 * phi_x
    
    dA_dt = phi3_t*tilde_psi*psi_t + phi3*tilde_psi_t*psi_t + phi3*tilde_psi*psi_tt
    dB_dx = phi3_x*tilde_psi*psi_x + phi3*tilde_psi_x*psi_x + phi3*tilde_psi*psi_xx
    
    term3 = s_v**3 * lam_v**3 * (dA_dt + c_v**2 * dB_dx)
    
    L2_val = term1 + term2 + term3
    return float(L2_val)

# Test with alpha = 1.5
print("Testing psi = -log(1+t) - log(1+x), alpha=1.5, lam=-1/20")
print()

# First, the critical regime from Round 2-6: large (1+t)*(1+x)
# With s=-1/100:
print("=== s = -1/100, alpha = 1.5 ===")
test_points = [
    # (x, t, c)
    (0, 0, 1),
    (0, 1e10, 1),
    (0, 1e20, 1),
    (0, 1e50, 1),
    (0, 1e100, 1),
    (0, 1e200, 1),
    (1e10, 0, 1),
    (1e20, 0, 1),
    (1e50, 0, 1),
    (1e100, 0, 1),
    (1e10, 1e10, 1),
    (1e20, 1e20, 1),
    (0, 0, 100),
    (0, 0, 1e6),
    (0, 0, 1e10),
    (0, 1e10, 100),
    (0, 1e20, 100),
    (1e10, 0, 100),
    (1e20, 0, 100),
    (0, 0, 0.01),
    (0, 0, 0.001),
    (0, 1e10, 0.01),
    (1e10, 0, 0.01),
]

for x_v, t_v, c_v in test_points:
    L2_v = eval_L2_full(x_v, t_v, c_v, 20, -0.01, 1.5)
    status = "POSITIVE" if L2_v > 0 else "NEGATIVE" if L2_v < 0 else "ZERO"
    print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.2e}: L2 = {L2_v:.6e} [{status}]")

# Hmm, let me also check: does alpha=1.5 change the STRUCTURE of the L2 failure?
# With alpha=1: L2_num = A(z) - B(z)*R where A is polynomial, B*R has fractional power growth
# With alpha=1.5: there are additional (alpha-1) terms that add to the polynomial part
# The question is whether these new terms grow fast enough to beat R.

# The key term that was causing failure: -s^3*lam^4*phi^3*tilde^2
# With alpha != 1: we also get s^3*lam^3*(alpha-1)*phi^3*tilde*box = s^3*lam^3*(alpha-1)*phi^3*tilde^2
# Combined: s^3*lam^3*(alpha-1-lam)*phi^3*tilde^2
# With alpha=1.5, lam=-1/20: alpha-1-lam = 0.5+1/20 = 11/20
# With alpha=1, lam=-1/20: alpha-1-lam = 0+1/20 = 1/20
# So the coefficient changes from 1/20 to 11/20 — a factor of 11x.
# But the SIGN doesn't change: it's still positive (remember s^3 < 0, lam^3 < 0, so s^3*lam^3 > 0).
# Wait: s^3 = (-0.01)^3 = -10^{-6}, lam^3 = (-1/20)^3 = -1/8000
# s^3*lam^3 = (-10^{-6})*(-1/8000) = 1.25e-10 > 0
# alpha-1-lam = 11/20 > 0
# phi^3 > 0, tilde^2 >= 0
# So this combined term is POSITIVE.

# The term1: (1/2)*s*lam*(alpha-1-lam)*sq_pt
# s*lam = (-0.01)*(-1/20) = 5e-4 > 0
# alpha-1-lam = 11/20
# sq_pt is the wave operator applied to phi*tilde
# This was shown to be positive for the double-log. So term1 is also POSITIVE.

# Wait... if BOTH the new terms are positive, and term3 (the div terms) was the only
# potential issue... let me re-examine.

# Actually, let me go back to the analysis. For alpha=1:
# L2 = -(s/2)*lam^2*sq_pt - s^3*lam^4*phi^3*tilde^2 + s^3*lam^3*(div terms)
# = |s|/2 * lam^2 * sq_pt + |s|^3 * lam^4 * phi^3 * tilde^2 + s^3*lam^3*(div terms)
# The first two terms are positive. The div terms have mixed signs.

# For alpha=1.5:  
# L2 = (s/2)*lam*(alpha-1-lam)*sq_pt + s^3*lam^3*(alpha-1-lam)*phi^3*tilde^2 + s^3*lam^3*(div terms)
# = |s|/2 * |lam| * (11/20) * sq_pt + |s|^3 * |lam|^3 * (11/20) * phi^3 * tilde^2 + s^3*lam^3*(div terms)
# The coefficient changes but the div terms are THE SAME (they don't depend on alpha).

# So alpha only changes the coefficients of the manifestly positive terms, not the problematic div terms.
# This means alpha cannot fix the structural issue if the div terms dominate.

# BUT: let me check the div terms more carefully.
# Term3 = s^3*lam^3*(d/dt(phi^3*tilde*psi_t) + c^2*d/dx(phi^3*tilde*psi_x))
# Let me expand this:
# d/dt(phi^3*tilde*psi_t) = phi3_t*tilde*psi_t + phi3*tilde_t*psi_t + phi3*tilde*psi_tt
# For the double-log at x=0, large t:
# phi3 ~ T^(3/N), tilde ~ 1/T^2 - c^2, psi_t = -1/T, psi_tt = 1/T^2
# phi3_t = 3/N * phi3/T
# tilde_t = -2/T^3
# Term by term:
# phi3_t*tilde*psi_t = (3/N)*phi3/T * (1/T^2 - c^2) * (-1/T) = -(3/N)*phi3*(1/T^2-c^2)/T^2
# phi3*tilde_t*psi_t = phi3*(-2/T^3)*(-1/T) = 2*phi3/T^4
# phi3*tilde*psi_tt = phi3*(1/T^2-c^2)*1/T^2
# Sum = phi3*[(-(3/N))*(1/T^2-c^2)/T^2 + 2/T^4 + (1/T^2-c^2)/T^2]
# = phi3*[(1-3/N)*(1/T^2-c^2)/T^2 + 2/T^4]
# For large T: ~ phi3*[(1-3/N)*(-c^2)/T^2 + 2/T^4]
# ~ phi3 * (-c^2*(1-3/N)/T^2)  (for T large)

# The c^2 part: dB_dx at x=0 = phi3_x*tilde*psi_x + phi3*tilde_x*psi_x + phi3*tilde*psi_xx
# At x=0: X=1, psi_x = -1, psi_xx = 1
# phi3_x at x=0: need to compute... phi3 = (TX)^(3/N), phi3_x = (3/N)*phi3/X = (3/N)*phi3
# tilde_x = 2c^2/X^3 = 2c^2
# = phi3*(3/N)*(1/T^2-c^2)*(-1) + phi3*2c^2*(-1) + phi3*(1/T^2-c^2)*1
# = phi3*[-(3/N)*(1/T^2-c^2) - 2c^2 + (1/T^2-c^2)]
# = phi3*[(1-3/N)*(1/T^2-c^2) - 2c^2]
# ~ phi3*[(1-3/N)*(-c^2) - 2c^2] = phi3*c^2*[-(1-3/N) - 2] = phi3*c^2*(-3+3/N)
# = phi3*c^2*3*(1/N-1)

# So dA_dt + c^2*dB_dx at (x=0, large T) ~
# phi3*(-c^2*(1-3/N)/T^2) + c^2*phi3*c^2*3*(1/N-1)
# = phi3*c^2*[(-(1-3/N)/T^2 + 3c^2*(1/N-1)]
# = phi3*c^2*[-((N-3)/N)/T^2 - 3c^2*(N-1)/N]
# For large T: ~ phi3*c^2*(-3c^2*(N-1)/N) < 0

# So the div term at x=0, large T is:
# s^3*lam^3 * (NEGATIVE) = |s|^3*|lam|^3 * (NEGATIVE)... wait
# s^3 = (-|s|)^3 = -|s|^3, lam^3 = (-|lam|)^3 = -|lam|^3
# s^3*lam^3 = |s|^3*|lam|^3 > 0
# So term3 = |s|^3*|lam|^3 * (NEGATIVE) < 0

# The negative contribution from term3 grows as phi3 = T^(3/N) for large T.
# The positive term1 grows as T^{something involving derivatives of phi*tilde}.
# Let me compute term1's T-dependence at x=0, large T:
# sq_pt = d^2/dt^2(phi*tilde) - c^2*d^2/dx^2(phi*tilde) at x=0
# phi*tilde = T^(1/N)*(1/T^2-c^2)
# d/dt(phi*tilde) = (1/N)*T^(1/N-1)*(1/T^2-c^2) + T^(1/N)*(-2/T^3)
# For large T: ~ (1/N)*T^(1/N-1)*(-c^2) = -c^2*T^(1/N-1)/N
# d^2/dt^2 ~ -c^2*(1/N-1)/N * T^(1/N-2) for large T
# So sq_pt ~ T^(1/N-2) type terms
# term1 ~ T^(1/N-2) (since |s|*|lam|*...)
# term3 ~ T^(3/N) (since |s|^3*|lam|^3*phi^3*...)

# Ratio term3/term1 ~ T^(3/N - (1/N-2)) = T^(2/N + 2) → ∞
# So term3 ALWAYS dominates for large T, making L2 < 0 eventually.
# This is INDEPENDENT of alpha!

print("\n\n=== CONCLUSION ===")
print("For the double-log ansatz with ANY alpha:")
print("  term1 (positive, O(s)) ~ T^(1/N - 2)")
print("  term3 (negative div, O(s^3)) ~ T^(3/N)")
print("  Ratio term3/term1 ~ T^(2/N + 2) -> infinity")
print("  So L2 ALWAYS becomes negative for large enough T, regardless of alpha or s.")
print()
print("The ONLY way to make L2 > 0 globally is to use an ansatz where")
print("the problematic T^(3/N) growth does not occur.")
print()
print("The traveling wave psi = -log(1+x+ct) achieves this: tilde(psi) = box(psi) = 0,")
print("so ALL terms in L2 vanish. But this gives L2 = 0, not L2 > 0.")
print()
print("KEY QUESTION: Is there an ansatz where L2 is STRICTLY positive")
print("and all other conditions also hold?")

# Try the quadratic ansatz that was suggested at the beginning
print("\n\n=== Testing quadratic ansatz psi = beta*t - (x+x0)^2 ===")
# With lam < 0 and s < 0:
# phi = exp(lam*psi) = exp(lam*beta*t - lam*(x+x0)^2)
# = exp(lam*beta*t) * exp(-lam*(x+x0)^2)
# Since lam < 0: exp(-lam*(x+x0)^2) = exp(|lam|*(x+x0)^2) -> infinity as x -> infinity
# lam*psi = lam*beta*t - lam*(x+x0)^2 = -|lam|*beta*t + |lam|*(x+x0)^2 -> +infinity as x -> infinity ✓ (condition 2)

# L1/phi = lam^2*(beta^2 + 4c^2*(x+x0)^2) + lam*(-2c^2)
# = lam^2*(beta^2 + 4c^2*(x+x0)^2) - 2c^2*|lam|
# For L1 <= 0: |lam|(beta^2 + 4c^2*(x+x0)^2) <= 2c^2
# At x+x0 = 0: |lam|*beta^2 <= 2c^2, i.e., beta^2 <= 2c^2/|lam|
# As x -> infinity: the LHS grows, so this FAILS.

# But wait - maybe a different approach to the quadratic.
# What about psi = beta*t - (x+x0)^2 with alpha chosen to make L work?
# L = lam^2*phi*tilde(psi) - (alpha-1)*lam*phi*box(psi)
# tilde(psi) = beta^2 - c^2*4*(x+x0)^2
# box(psi) = 0 - c^2*(-2) = 2c^2
# L = phi*[lam^2*(beta^2 - 4c^2*(x+x0)^2) - (alpha-1)*lam*2c^2]

# For condition 1: L1 < L < -L1
# L1 = phi*[lam^2*(beta^2 + 4c^2*(x+x0)^2) - 2c^2*|lam|]
# Since L1 must be < 0: lam^2*(beta^2 + 4c^2*(x+x0)^2) < 2c^2*|lam|
# This FAILS at large x regardless.

print("Quadratic ansatz psi = beta*t - (x+x0)^2 fails condition 1 at large x")
print("because the gradient (psi_x)^2 = 4(x+x0)^2 grows without bound.")

# What about making psi bounded in x? Like psi = beta*t - arctan(x)^2?
# Then psi_x = -2*arctan(x)/(1+x^2), bounded.
# psi_xx: complicated but bounded.
# (psi_x)^2: bounded.
# psi_tt = 0, psi_xx: bounded.
# L1/phi = lam^2*(beta^2 + c^2*(bounded)) + lam*(c^2*bounded_xx)
# = lam^2*P + lam*Q where P is bounded and Q is bounded.
# For L1 <= 0: need Q to dominate P/|lam|. Since both are bounded, this works for |lam| small.
# BUT: condition 2 requires lam*psi -> +infinity as x -> infinity.
# lam*psi = lam*beta*t - lam*arctan(x)^2.
# As x -> infinity: arctan(x) -> pi/2, so lam*psi -> lam*beta*t - lam*(pi/2)^2 = bounded.
# This does NOT go to +infinity! FAILS condition 2.

print("\npsi = beta*t - arctan(x)^2 fails condition 2: lam*psi is bounded as x -> infinity")

# Condition 2 requires lam*psi -> +infinity.
# With lam < 0: need psi -> -infinity as x -> infinity.
# So psi must decrease to -infinity as x grows.
# But if |psi_x| must be bounded (for L1 <= 0), psi can decrease at most linearly.
# psi ~ -a*x for large x, psi_x ~ -a, (psi_x)^2 ~ a^2 (constant).
# Then L1/phi ~ lam^2*(beta^2 + c^2*a^2) - something. The lam^2 term is constant,
# and the something must dominate. But psi_xx ~ 0 for linear growth, so
# lam*psi_xx ~ 0. Then L1/phi ~ lam^2*constant > 0. FAILS.

# UNLESS psi_xx is negative enough. For L1 <= 0: lam*(psi_tt + c^2*psi_xx) must dominate.
# With lam < 0: lam*(psi_xx) contributes positively if psi_xx > 0, negatively if psi_xx < 0.
# We need the positive contribution lam*(psi_tt + c^2*psi_xx) < 0, i.e., psi_tt + c^2*psi_xx > 0.
# Wait: L1/phi = lam^2*P + lam*Q where Q = psi_tt + c^2*psi_xx.
# For L1 < 0: lam*Q < -lam^2*P, i.e., -|lam|*Q < -|lam|^2*P, i.e., Q > |lam|*P.
# So we need Q = psi_tt + c^2*psi_xx > |lam|*(psi_t^2 + c^2*psi_x^2).
# With psi_x ~ -a (constant), psi_xx ~ 0 (at large x):
# Q ~ psi_tt + 0 = psi_tt. And P ~ beta^2 + c^2*a^2.
# So we need psi_tt > |lam|*(beta^2 + c^2*a^2) > 0 for all t.
# But psi_tt being bounded below by a positive constant means psi_t is increasing,
# which means psi_t -> infinity. But then psi_t^2 grows, making P grow, requiring
# even larger psi_tt. This leads to exponential growth: psi ~ e^{|lam|^{1/2}*t},
# which conflicts with the problem setup (bounded domain in t).

# Actually, the problem says t in [0,T] for fixed T. So psi_t can grow with t.
# But the conditions must hold for ALL t in [0,T], and T is arbitrary.
# So effectively, we need conditions to hold for all t >= 0.

print("\n\nThe key constraint: for L1 < 0, we need psi_tt + c^2*psi_xx > |lam|*(psi_t^2 + c^2*psi_x^2)")
print("This means the 'Laplacian' must dominate the gradient-squared.")
print("For log functions: (log)'' = -1/u^2, ((log)')^2 = 1/u^2. Ratio = 1.")
print("For power functions: (u^q)'' = q(q-1)*u^{q-2}, ((u^q)')^2 = q^2*u^{2q-2}. Ratio = (q-1)/q * u^{-q}.")
print("Only log has the ratio exactly 1 (self-similar property).")
print()
print("FUNDAMENTAL INSIGHT: The log function is the UNIQUE ansatz (up to affine transformations)")
print("where L1 < 0 can hold globally. Any other function class fails at infinity.")
print("The traveling wave log(1+x+ct) satisfies L1 but gives L2 = 0 (not > 0).")
print("The separated log gives L2 > 0 at moderate scales but fails asymptotically.")
print()
print("REMAINING HOPE: A perturbation of the traveling wave that creates L2 > 0")
print("WITHOUT introducing the asymptotic failure. The perturbation must create")
print("a POSITIVE contribution to L2 that doesn't grow with phi^3.")

