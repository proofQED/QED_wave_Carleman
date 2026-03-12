"""
Explore the effect of alpha on L2 for the double-log ansatz.
With alpha != 1, the (alpha-1) terms in L2 become nonzero.
This introduces new positive terms that might help.
"""
import sympy as sp
import mpmath
import sys
sys.path.insert(0, '/local/home/cyanz/wave_PINN')
from verify_engine import x, t, c, x0, alpha, s, lam, build_operators, truth_value_from_sign

print("="*80)
print("EXPLORING: alpha != 1 for the double-log ansatz")
print("="*80)

# For psi = -log(1+t) - log(1+x), with alpha=1, box(psi) = tilde(psi).
# With alpha != 1, L = lam^2*phi*tilde - (alpha-1)*lam*phi*box = phi*[lam^2*tilde - (alpha-1)*lam*box]
# Since tilde = box for this ansatz:
# L = phi*tilde*[lam^2 - (alpha-1)*lam] = phi*lam*tilde*[lam - alpha + 1]

# For condition 1: L1 < L < -L1
# L1 = lam(lam+1)*phi*(psi_t^2 + c^2*psi_x^2) (this doesn't depend on alpha)
# L = lam*phi*tilde*[lam - alpha + 1]
# 
# Condition 1a: L - L1 > 0
# L - L1 = lam*phi*tilde*(lam-alpha+1) - lam(lam+1)*phi*P
# where P = psi_t^2 + c^2*psi_x^2 and tilde = psi_t^2 - c^2*psi_x^2
# = lam*phi*[(lam-alpha+1)*tilde - (lam+1)*P]
# = lam*phi*[(lam-alpha+1)*(A^2 - c^2*B^2) - (lam+1)*(A^2 + c^2*B^2)]
# where A = -1/(1+t), B = -1/(1+x)
# = lam*phi*[A^2*(lam-alpha+1-lam-1) + c^2*B^2*(-(lam-alpha+1)-(lam+1))]
# = lam*phi*[A^2*(-alpha) + c^2*B^2*(-2lam+alpha-2)]
# = lam*phi*[-alpha*A^2 - (2lam-alpha+2)*c^2*B^2]
# Since lam < 0: lam*phi < 0
# L - L1 = -|lam|*phi*[-alpha*A^2 - (2lam-alpha+2)*c^2*B^2]
#         = |lam|*phi*[alpha*A^2 + (2lam-alpha+2)*c^2*B^2]
# For this > 0: need alpha*A^2 + (2lam-alpha+2)*c^2*B^2 > 0
# A^2, B^2 > 0, so need:
# alpha > 0 AND 2lam-alpha+2 > 0, i.e., alpha < 2+2lam = 2*(1+lam)
# OR one coefficient can be negative if compensated.
# For alpha > 0 and alpha < 2(1+lam): this requires lam > -1 (satisfied by lam=-1/20).
# With lam = -1/20: alpha < 2*19/20 = 19/10 = 1.9

# Condition 1b: -L1 - L > 0
# -L1 - L = -(lam+1)*lam*phi*P - lam*phi*tilde*(lam-alpha+1)
# = -lam*phi*[(lam+1)*P + (lam-alpha+1)*tilde]
# = |lam|*phi*[(lam+1)*(A^2+c^2B^2) + (lam-alpha+1)*(A^2-c^2B^2)]
# = |lam|*phi*[A^2*(lam+1+lam-alpha+1) + c^2B^2*(lam+1-lam+alpha-1)]
# = |lam|*phi*[A^2*(2lam+2-alpha) + c^2B^2*alpha]
# Same conditions: 2lam+2-alpha > 0 and alpha > 0.

# So condition 1 works for 0 < alpha < 2(1+lam).

# Now the key: how does alpha affect L2?
# With alpha != 1, the (alpha-1)*s*lam*square(phi*box_psi) term is nonzero.
# And the (alpha-1)*s^3*lam^3*phi^3*tilde*box term is nonzero.

# For the double-log with box = tilde:
# Term in L2 from (alpha-1):
# (1/2)*(alpha-1)*s*lam*square(phi*box) 
# + s^3*lam^3*(alpha-1)*phi^3*tilde*box
# = (1/2)*(alpha-1)*s*lam*square(phi*tilde) + s^3*lam^3*(alpha-1)*phi^3*tilde^2

# The full L2 becomes:
# L2 = (1/2)*((alpha-1)*s*lam - s*lam^2)*square(phi*tilde)
#    + s^3*lam^3*((alpha-1) - lam)*phi^3*tilde^2
#    + s^3*lam^3*(div terms)
# = (1/2)*s*lam*(alpha-1-lam)*square(phi*tilde)
#   + s^3*lam^3*(alpha-1-lam)*phi^3*tilde^2
#   + s^3*lam^3*(div terms)
# = s*lam*(alpha-1-lam)*[(1/2)*square(phi*tilde) + s^2*lam^2*phi^3*tilde^2]
#   + s^3*lam^3*(div terms)

# The common factor s*lam*(alpha-1-lam):
# s < 0, lam < 0, so s*lam > 0
# For alpha > 1+lam (e.g., alpha=1, lam=-1/20 gives 1+lam = 19/20 < 1, so alpha > 19/20):
# alpha-1-lam > 0
# So s*lam*(alpha-1-lam) > 0

# The bracket: (1/2)*square(phi*tilde) + s^2*lam^2*phi^3*tilde^2
# s^2*lam^2*phi^3*tilde^2 >= 0 always
# If square(phi*tilde) >= 0, the whole bracket is positive.
# From Part 1's computation, square(phi*tilde_psi) had all positive terms!

# So the issue is the "div terms" which have mixed signs.
# Let me compute L2 with alpha != 1 to see if the extra (alpha-1) terms help enough.

print("\nComputing L2 with alpha=1.5 (midpoint of allowed range [0, 1.9])...")

psi_dlog = -sp.ln(1 + t) - sp.ln(1 + x)

subs_alpha = {
    alpha: sp.Rational(3, 2),  # alpha = 1.5
    s: sp.Rational(-1, 100),
    lam: sp.Rational(-1, 20),
}

print("Building operators...")
ops_a = build_operators(psi_dlog, subs_alpha)
print("L =", sp.factor(ops_a['L']))
print("L1 =", sp.factor(ops_a['L1']))

# Check condition 1
cond_1a = sp.simplify(ops_a['L'] - ops_a['L1'])
cond_1b = sp.simplify(-ops_a['L1'] - ops_a['L'])
print("\nL - L1 =", sp.factor(cond_1a))
print("-L1 - L =", sp.factor(cond_1b))
print("L - L1 > 0?", truth_value_from_sign(cond_1a, '>0'))
print("-L1 - L > 0?", truth_value_from_sign(cond_1b, '>0'))

# Check condition 2
lam_psi = sp.Rational(-1, 20) * psi_dlog
print("\nlim(x->inf) lam*psi =", sp.limit(lam_psi, x, sp.oo))

# Check sufficient condition  
phi_a = ops_a['phi']
phi_xt = sp.diff(phi_a, x, t)
suff = sp.simplify(ops_a['L1']**2 - ops_a['L']**2 - c**2 * phi_xt**2)
print("Sufficient >= 0?", truth_value_from_sign(suff, '>=0'))

# L2 analysis
L2_a = sp.simplify(ops_a['L2'])
print("\nL2 =", str(L2_a)[:300], "...")
print("L2 > 0?", truth_value_from_sign(L2_a, '>0'))

# Numerical check of L2
print("\nNumerical L2 check:")
from verify_engine import numerical_check
status, details = numerical_check(L2_a, '>=0', 
                                  x_range=(0, 100, 50), t_range=(0, 100, 50),
                                  c_vals=(0.1, 0.5, 1.0, 2.0, 10.0))
print(f"  Status: {status}, Details: {details}")

# Extended range
status2, details2 = numerical_check(L2_a, '>=0',
                                    x_range=(0, 10000, 100), t_range=(0, 10000, 100),
                                    c_vals=(0.1, 0.5, 1.0, 2.0, 10.0, 100.0))
print(f"  Extended: {status2}, Details: {details2}")

# Also test with s = -1/(100*c) to handle the c-dependence
print("\n\n--- Testing alpha=1.5, s = -1/(100*c) ---")
subs_alpha_c = {
    alpha: sp.Rational(3, 2),
    s: sp.Rational(-1, 100) / c,
    lam: sp.Rational(-1, 20),
}

ops_ac = build_operators(psi_dlog, subs_alpha_c)
L2_ac = sp.simplify(ops_ac['L2'])
print("L2 > 0?", truth_value_from_sign(L2_ac, '>0'))

status3, details3 = numerical_check(L2_ac, '>=0',
                                    x_range=(0, 10000, 100), t_range=(0, 10000, 100),
                                    c_vals=(0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0))
print(f"  Extended: {status3}, Details: {details3}")

