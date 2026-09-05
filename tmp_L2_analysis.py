import sympy as sp
from verify_engine import x, t, c, x0, alpha, s, lam, build_operators, truth_value_from_sign

print("="*80)
print("L2 ANALYSIS for double-log with s = -1/c^2, lam = -1/20")
print("="*80)

psi_dlog = -sp.ln(1 + t) - sp.ln(1 + x)

subs_c2 = {
    alpha: 1,
    s: -1/c**2,
    lam: sp.Rational(-1, 20),
}

ops = build_operators(psi_dlog, subs_c2)
L2_expr = ops['L2']

# Substitute T = 1+t, X = 1+x for cleaner expressions
T_sym, X_sym = sp.symbols('T X', positive=True)

L2_sub = L2_expr.subs([(t, T_sym - 1), (x, X_sym - 1)])
L2_simplified = sp.simplify(L2_sub)

print("\nL2 in terms of T=1+t, X=1+x:")
print(L2_simplified)

# Factor out known positive quantities
# The denominator should be positive. Let's extract it.
L2_numer, L2_denom = sp.fraction(sp.cancel(L2_simplified))
print("\nNumerator:", sp.collect(sp.expand(L2_numer), [c, T_sym, X_sym]))
print("\nDenominator:", sp.factor(L2_denom))

# Check if denominator is positive
print("\nDenominator is positive?", truth_value_from_sign(L2_denom, '>0'))

# The key: is the numerator > 0?
# Let's substitute z = c^2 * T^2 / X^2 and R = (TX)^(1/10)
# and see the structure

# Actually, let me factor out from the numerator
# All terms have T^(1/20)*X^(1/20) as a factor (from phi)
# Let me divide out phi = T^(1/20)*X^(1/20) and the common denominator factors

# Instead, let me use the L2/phi^3 form since that's what the engine prints
phi_val = ops['phi']
L2_over_phi3 = sp.simplify(L2_expr / phi_val**3)
print("\nL2/phi^3 =", sp.factor(L2_over_phi3))

# Actually, let me think about this more carefully using the structure
# from the failed_approaches analysis.
# L2 numerator = A(z) - B(z)*R where z = c^2*T^2/X^2, R = (TX)^(1/10)
# 
# For the s = -1/c^2 case, the coefficients A and B will have different c-dependence.
# Let me extract this.

# The L2 expression has s = -1/c^2.
# O(s) term: proportional to s = -1/c^2, so 1/c^2 after sign
# O(s^3) term: proportional to s^3 = -1/c^6, so 1/c^6 after sign
# 
# So L2 ~ (1/c^2) * [positive term] - (1/c^6) * [R-growing term]
# = (1/c^2) * [positive] * (1 - (1/c^4) * [R-growing]/[positive])
# 
# For L2 > 0: [R-growing]/[positive] < c^4
# 
# The R-growing part has R = (TX)^(1/10), and the positive part is a polynomial in T, X.
# The question is whether R/polynomial is bounded above by c^4.
# 
# At t=0, x = large X: R = X^(1/10), and the ratio may approach a constant.
# Then we need that constant < c^4.
# But c is a parameter - we need this for ALL c > 0, including c -> 0.
# As c -> 0+, c^4 -> 0, so the condition can't hold for arbitrarily small c!
# 
# Unless the positive part also depends on c in a way that helps.
# Let's check.

# Substitute specific values to see the c-dependence
print("\n\nNumerical tests: L2 at specific points")
import numpy as np

def eval_L2_sympy(x_val, t_val, c_val):
    """Evaluate L2 using sympy for exact computation."""
    val = L2_expr.subs([(x, x_val), (t, t_val), (c, c_val)])
    return float(val.evalf())

# Test c -> 0
print("\nL2 at x=0, t=0 for various c:")
for c_val in [0.01, 0.1, 0.5, 1, 2, 10, 100]:
    L2_val = eval_L2_sympy(0, 0, c_val)
    print(f"  c={c_val}: L2 = {L2_val:.6e}")

print("\nL2 at x=100, t=0 for various c:")
for c_val in [0.01, 0.1, 0.5, 1, 2, 10, 100]:
    L2_val = eval_L2_sympy(100, 0, c_val)
    print(f"  c={c_val}: L2 = {L2_val:.6e}")

print("\nL2 at x=0, t=100 for various c:")
for c_val in [0.01, 0.1, 0.5, 1, 2, 10, 100]:
    L2_val = eval_L2_sympy(0, 100, c_val)
    print(f"  c={c_val}: L2 = {L2_val:.6e}")

# Critical test: large x, small c
print("\nL2 at large x, small c (critical regime):")
for x_val, c_val in [(1000, 0.01), (1000, 0.001), (10000, 0.01), (10000, 0.001)]:
    L2_val = eval_L2_sympy(x_val, 0, c_val)
    print(f"  x={x_val}, c={c_val}: L2 = {L2_val:.6e}")

# Use mpmath for extreme values  
print("\nUsing mpmath for extreme values:")
import mpmath
mpmath.mp.dps = 50

def eval_L2_mpmath(x_v, t_v, c_v, N, s_v):
    """Evaluate L2 for double-log with mpmath."""
    x_v = mpmath.mpf(x_v)
    t_v = mpmath.mpf(t_v)
    c_v = mpmath.mpf(c_v)
    N_v = mpmath.mpf(N)
    s_v = mpmath.mpf(s_v)
    lam_v = -1/N_v
    
    T = 1 + t_v
    X = 1 + x_v
    
    phi = (T * X)**(1/N_v)
    
    psi_t = -1/T
    psi_x = -1/X
    psi_tt = 1/T**2
    psi_xx = 1/X**2
    
    box_psi = psi_tt - c_v**2 * psi_xx
    tilde_psi = psi_t**2 - c_v**2 * psi_x**2
    
    # phi derivatives
    phi_t = phi / (N_v * T)
    phi_x = phi / (N_v * X)
    phi_tt = phi / T**2 * (1 - N_v) / N_v**2
    phi_xx = phi / X**2 * (1 - N_v) / N_v**2
    phi_tx = phi / (N_v**2 * T * X)
    
    # tilde_psi derivatives
    tilde_psi_t = -2/T**3
    tilde_psi_x = 2*c_v**2/X**3
    tilde_psi_tt = 6/T**4
    tilde_psi_xx = -6*c_v**2/X**4
    
    # box_psi derivatives  
    box_psi_t = -2/T**3
    box_psi_x = 2*c_v**2/X**3
    box_psi_tt = 6/T**4
    box_psi_xx = -6*c_v**2/X**4
    
    # (phi * tilde_psi) second derivatives
    pt = phi * tilde_psi
    pt_tt = phi_tt*tilde_psi + 2*phi_t*tilde_psi_t + phi*tilde_psi_tt
    pt_xx = phi_xx*tilde_psi + 2*phi_x*tilde_psi_x + phi*tilde_psi_xx
    sq_pt = pt_tt - c_v**2 * pt_xx
    
    # (phi * box_psi) second derivatives (needed for alpha != 1)
    pb = phi * box_psi
    pb_tt = phi_tt*box_psi + 2*phi_t*box_psi_t + phi*box_psi_tt
    pb_xx = phi_xx*box_psi + 2*phi_x*box_psi_x + phi*box_psi_xx
    sq_pb = pb_tt - c_v**2 * pb_xx
    
    alpha_v = 1
    
    # Term 1: (1/2)*((alpha-1)*s*lam*sq_pb - s*lam^2*sq_pt)
    term1 = mpmath.mpf('0.5') * ((alpha_v - 1)*s_v*lam_v*sq_pb - s_v*lam_v**2*sq_pt)
    
    # Term 2: s^3*lam^3*(alpha-1)*phi^3*tilde_psi*box_psi - s^3*lam^4*phi^3*tilde_psi^2
    phi3 = phi**3
    term2 = s_v**3 * lam_v**3 * (alpha_v - 1) * phi3 * tilde_psi * box_psi - s_v**3 * lam_v**4 * phi3 * tilde_psi**2
    
    # Term 3: s^3*lam^3*(d/dt(phi^3*tilde_psi*psi_t) + c^2*d/dx(phi^3*tilde_psi*psi_x))
    phi3_t = 3*phi**2 * phi_t
    phi3_x = 3*phi**2 * phi_x
    
    dA_dt = phi3_t*tilde_psi*psi_t + phi3*tilde_psi_t*psi_t + phi3*tilde_psi*psi_tt
    dB_dx = phi3_x*tilde_psi*psi_x + phi3*tilde_psi_x*psi_x + phi3*tilde_psi*psi_xx
    
    term3 = s_v**3 * lam_v**3 * (dA_dt + c_v**2 * dB_dx)
    
    return float(term1 + term2 + term3)

# Test with s = -1/c^2
print("\nWith N=20, s = -1/c^2:")
test_cases = [
    # x, t, c
    (0, 0, 0.001),
    (0, 0, 0.01),
    (0, 0, 0.1),
    (0, 0, 1),
    (0, 0, 10),
    (0, 0, 100),
    (1e10, 0, 1),
    (1e20, 0, 1),
    (1e50, 0, 1),
    (1e100, 0, 1),
    (1e10, 1e10, 1),
    (1e20, 1e20, 1),
    (0, 1e10, 1),
    (0, 1e20, 1),
    (1e10, 0, 0.01),
    (1e20, 0, 0.01),
    (1e10, 0, 1e6),
    (0, 0, 1e-6),
    (0, 0, 1e-10),
]

for x_v, t_v, c_v in test_cases:
    s_v = -1.0/c_v**2
    try:
        L2_v = eval_L2_mpmath(x_v, t_v, c_v, 20, s_v)
        print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.0e}: s={s_v:.2e}, L2 = {L2_v:.6e}")
    except Exception as e:
        print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.0e}: ERROR {e}")

# Now test with s = -1/(1+c^2) to handle small c better
print("\n\nWith N=20, s = -1/(1+c^2):")
for x_v, t_v, c_v in test_cases:
    s_v = -1.0/(1 + c_v**2)
    try:
        L2_v = eval_L2_mpmath(x_v, t_v, c_v, 20, s_v)
        print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.0e}: s={s_v:.2e}, L2 = {L2_v:.6e}")
    except Exception as e:
        print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.0e}: ERROR {e}")

