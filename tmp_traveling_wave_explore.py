import sympy as sp

x, t = sp.symbols('x t', nonnegative=True)
c = sp.symbols('c', positive=True)
lam_sym = sp.Symbol('lam', negative=True)
s_sym = sp.Symbol('s', negative=True)
alpha_sym = sp.Symbol('alpha')

print("="*80)
print("PART 1: Pure traveling wave psi = -log(1+x+ct)")
print("="*80)

psi_tw = -sp.ln(1 + x + c*t)

# Check all operators
box_psi = sp.diff(psi_tw, t, 2) - c**2 * sp.diff(psi_tw, x, 2)
tilde_psi = sp.diff(psi_tw, t)**2 - c**2 * sp.diff(psi_tw, x)**2

print("box(psi) =", sp.simplify(box_psi))
print("tilde(psi) =", sp.simplify(tilde_psi))

# Both are 0, so L = 0 and L2 = 0.
# The traveling wave makes L2 exactly 0, which fails the strict inequality.

print("\n" + "="*80)
print("PART 2: Perturbed traveling wave psi = -log(1+x+ct) - eps*log(1+t)")
print("="*80)

eps = sp.Symbol('epsilon', positive=True)
psi_pert = -sp.ln(1 + x + c*t) - eps * sp.ln(1 + t)

box_psi_p = sp.simplify(sp.diff(psi_pert, t, 2) - c**2 * sp.diff(psi_pert, x, 2))
tilde_psi_p = sp.simplify(sp.diff(psi_pert, t)**2 - c**2 * sp.diff(psi_pert, x)**2)

print("box(psi) =", box_psi_p)
print("tilde(psi) =", tilde_psi_p)

# For the perturbed version, box(psi) and tilde(psi) are O(epsilon), not zero.
# This means L and L2 are O(epsilon), and the question is whether L2 > 0.

print("\n" + "="*80)
print("PART 3: Check what happens with s depending on c")
print("For psi = -log(1+t) - log(1+x), s = -1/c^k")
print("="*80)

# The key insight from Round 4 analysis: for the separated double-log,
# the failure only occurs at large c (not large x or large t on its own).
# Setting s = -1/c^k makes the O(s) term scale as 1/c^k and the O(s^3) term as 1/c^(3k).
# The ratio O(s^3)/O(s) ~ 1/c^(2k), which goes to 0 for large c if k > 0.
# But the L2 expression also has explicit c-dependence...

# Let me directly compute L2 for the double-log ansatz with s = -1/c^(1/5)
psi_dlog = -sp.ln(1 + t) - sp.ln(1 + x)
lam_val = sp.Rational(-1, 20)
alpha_val = 1

phi = sp.exp(lam_val * psi_dlog)

# Build L2 symbolically
from verify_engine import square, tilde_square, build_operators
import verify_engine as ve

# Test with s = -c^(-1/5) / 100
# Actually, the subs_dict can contain c as a symbol
subs_test = {
    ve.alpha: 1,
    ve.s: -1 / (100 * c**sp.Rational(1, 5)),
    ve.lam: sp.Rational(-1, 20),
}

print("Testing subs_dict with s = -1/(100*c^(1/5))...")
print("s =", subs_test[ve.s])

# This might take a while to compute...
# Let me try a simpler approach: just test the traveling wave directly
print("\n" + "="*80)
print("PART 4: Direct verification of traveling wave psi = -log(1+x+ct)")
print("with the verify_engine")
print("="*80)

# The pure traveling wave gives L2 = 0 exactly.
# Let's verify this using the engine's build_operators.

subs_tw = {
    ve.alpha: 1,
    ve.s: -1,
    ve.lam: sp.Rational(-1, 20),
}

print("Building operators for traveling wave...")
ops_tw = build_operators(psi_tw, subs_tw)
print("L =", sp.factor(ops_tw['L']))
print("L1 =", sp.factor(ops_tw['L1']))
print("L2 =", sp.factor(ops_tw['L2']))

# Check if L2 is exactly 0
L2_is_zero = sp.simplify(ops_tw['L2']) == 0
print("L2 == 0?", L2_is_zero)

print("\n" + "="*80)
print("PART 5: Try psi = -log(1+x+ct) - log(1+x) (asymmetric)")
print("="*80)

psi_asym = -sp.ln(1 + x + c*t) - sp.ln(1 + x)

box_asym = sp.simplify(sp.diff(psi_asym, t, 2) - c**2 * sp.diff(psi_asym, x, 2))
tilde_asym = sp.simplify(sp.diff(psi_asym, t)**2 - c**2 * sp.diff(psi_asym, x)**2)

print("box(psi) =", box_asym)
print("tilde(psi) =", tilde_asym)

# box(psi) = c^2/(1+x+ct)^2 - c^2/(1+x+ct)^2 - c^2/(1+x)^2 + c^2/(1+x)^2... let me check
# Actually: psi = -log(1+x+ct) - log(1+x)
# psi_t = -c/(1+x+ct)
# psi_tt = c^2/(1+x+ct)^2
# psi_x = -1/(1+x+ct) - 1/(1+x)
# psi_xx = 1/(1+x+ct)^2 + 1/(1+x)^2
# box(psi) = c^2/(1+x+ct)^2 - c^2*(1/(1+x+ct)^2 + 1/(1+x)^2)
#          = c^2/(1+x+ct)^2 - c^2/(1+x+ct)^2 - c^2/(1+x)^2
#          = -c^2/(1+x)^2
# tilde(psi) = c^2/(1+x+ct)^2 - c^2*(1/(1+x+ct) + 1/(1+x))^2
# = c^2/(1+x+ct)^2 - c^2*(1/(1+x+ct)^2 + 2/((1+x+ct)(1+x)) + 1/(1+x)^2)
# = -c^2*(2/((1+x+ct)(1+x)) + 1/(1+x)^2)
# This is always negative!

print("\nFor psi = -log(1+x+ct) - log(1+x):")
print("box(psi) = -c^2/(1+x)^2 (always negative)")
print("tilde(psi) is always negative")
print()
print("With alpha=1:")
print("L = lam^2*phi*tilde(psi) which is lam^2*phi*(negative) > 0... wait")
print("lam^2 > 0, phi > 0, tilde(psi) < 0, so L < 0")
print()
print("L1 = lam^2*phi*(psi_t^2 + c^2*psi_x^2) + lam*phi*(psi_tt + c^2*psi_xx)")
print("For condition 1: L1 <= L <= -L1 means L1 <= L < 0 and 0 < -L <= -L1, i.e., L1 <= L < 0.")
print("So we need L1 < L < 0.")

# This is the Round 5 ansatz that was already tried and failed!
# Let me verify...
print("\nThis is essentially Round 5's ansatz (which failed on L2).")

print("\n" + "="*80)
print("PART 6: The s(c) approach for separated double-log")
print("Testing if subs_dict can have s depending on c")
print("="*80)

# The key question: can the verify engine handle s = f(c)?
# Let's test it.
print("Testing if verify_engine accepts symbolic s depending on c...")
psi_dlog = -sp.ln(1 + t) - sp.ln(1 + x)

# Try s = -1/(c^2)
subs_c_dep = {
    ve.alpha: 1,
    ve.s: -1 / c**2,
    ve.lam: sp.Rational(-1, 20),
}

try:
    ops_cdep = build_operators(psi_dlog, subs_c_dep)
    print("SUCCESS: Engine accepts s = -1/c^2")
    print("L =", sp.factor(ops_cdep['L']))
    print("L1 =", sp.factor(ops_cdep['L1']))
    L2_cdep = sp.simplify(ops_cdep['L2'])
    print("L2 simplified (first 200 chars):", str(L2_cdep)[:200])
    
    # Check sign of L2
    from verify_engine import truth_value_from_sign
    sign_result = truth_value_from_sign(L2_cdep, '>0')
    print("L2 > 0 symbolic check:", sign_result)
    
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "="*80)
print("PART 7: Analyzing the s(c) double-log L2 structure")
print("="*80)

# For psi = -log(1+t) - log(1+x), alpha=1, lam=-1/N:
# The L2 expression (normalized by positive factors) has the form:
# L2_num = A(z) - B(z) * R
# where z = c^2*(1+t)^2/(1+x)^2, R = ((1+t)(1+x))^(2/N)
#
# With s = -1/c^k:
# The s-dependent terms scale as:
# O(s) terms: proportional to |s| = 1/c^k
# O(s^3) terms: proportional to |s|^3 = 1/c^(3k)
#
# After factoring out common c-powers from L2:
# L2 = (1/c^k) * [P_1(z) + c^(-2k) * P_3(z, R)]
# where P_1 is the O(s) part (positive) and P_3 is the O(s^3) part (has R growth).
#
# For L2 > 0: P_1(z) > c^(-2k) * |P_3(z, R)|
# The RHS decays as c -> infinity (if k > 0), so for large c, L2 > 0 automatically.
# But we also need L2 > 0 for small c...
#
# At c = 0+ : z = 0, and R = ((1+t)(1+x))^(2/N)
# L2 ~ (1/c^k) * [P_1(0)] + ... but c^k -> 0, so 1/c^k -> infinity.
# Actually we need to be more careful since L2 itself involves c through the operators.

# Let me just compute L2 numerically for several (c, s(c)) choices
print("Numerical evaluation of L2 for double-log with s = -1/c^2:")
import numpy as np

def eval_L2_numerically(x_val, t_val, c_val, N, s_val):
    """Evaluate L2 for psi = -log(1+t) - log(1+x) with given params."""
    # phi = ((1+t)(1+x))^(1/N)
    T = 1 + t_val
    X = 1 + x_val
    lam_v = -1.0/N
    
    phi_v = (T * X)**(1.0/N)
    
    psi_t = -1.0/T
    psi_x = -1.0/X
    psi_tt = 1.0/T**2
    psi_xx = 1.0/X**2
    
    box_psi = psi_tt - c_val**2 * psi_xx
    tilde_psi = psi_t**2 - c_val**2 * psi_x**2
    
    # L = lam^2*phi*tilde_psi (alpha=1)
    # L1 = lam^2*phi*(psi_t^2 + c^2*psi_x^2) + lam*phi*(psi_tt + c^2*psi_xx)
    
    # For L2, we need the full expression. This is complex.
    # Let me compute it term by term.
    
    # Term 1: (1/2) * (-s*lam^2 * square(phi*tilde_psi))
    # alpha=1, so the (alpha-1) term vanishes
    
    # phi * tilde_psi
    pt = phi_v * tilde_psi
    
    # d/dt(phi*tilde_psi):
    # phi_t = (1/N)*phi*(-1/T) = -phi/(N*T)
    phi_t = phi_v / (N * T)  # Actually: d/dt((TX)^(1/N)) = (1/N)*(TX)^(1/N-1)*X*1 ... 
    # Wait: phi = (T*X)^(1/N), phi_t = (1/N)*(T*X)^(1/N - 1) * X = phi/(N*T)
    # But lam = -1/N, so phi = exp(lam*psi) = exp((-1/N)*(-log(T) - log(X))) = (TX)^(1/N)
    # phi_t = d/dt[(TX)^(1/N)] = (1/N)*(TX)^(1/N - 1) * X * 1 = (1/N)*phi/T = phi/(N*T)
    phi_t = phi_v / (N * T)
    phi_x = phi_v / (N * X)
    
    # tilde_psi = 1/T^2 - c^2/X^2
    # d/dt(tilde_psi) = -2/T^3
    # d/dx(tilde_psi) = 2c^2/X^3
    tilde_psi_t = -2.0/T**3
    tilde_psi_x = 2.0*c_val**2/X**3
    
    # phi*tilde_psi derivatives
    pt_t = phi_t * tilde_psi + phi_v * tilde_psi_t
    pt_x = phi_x * tilde_psi + phi_v * tilde_psi_x
    
    # phi second derivatives
    phi_tt = phi_v * (1.0/(N*T)**2 * (1 - N) + 0)  # Need to be more careful
    # phi = (TX)^(1/N)
    # phi_t = (1/N)*(TX)^(1/N) / T = phi/(NT)
    # phi_tt = d/dt[phi/(NT)] = (phi_t/(NT)) + phi*(-1/(NT^2))... no
    # phi_tt = d/dt[phi/(NT)] = phi_t/(NT) - phi/(NT^2)
    #        = phi/(N^2*T^2) - phi/(NT^2) = phi/T^2 * (1/N^2 - 1/N) = phi/T^2 * (1-N)/(N^2)
    phi_tt = phi_v / T**2 * (1 - N) / N**2
    phi_xx = phi_v / X**2 * (1 - N) / N**2
    phi_tx = phi_v / (N**2 * T * X)
    
    # tilde_psi second derivatives
    tilde_psi_tt = 6.0/T**4
    tilde_psi_xx = -6.0*c_val**2/X**4
    tilde_psi_tx = 0.0  # cross derivative is 0 for separated form
    
    # (phi*tilde_psi)_tt
    pt_tt = phi_tt*tilde_psi + 2*phi_t*tilde_psi_t + phi_v*tilde_psi_tt
    pt_xx = phi_xx*tilde_psi + 2*phi_x*tilde_psi_x + phi_v*tilde_psi_xx
    
    # square(phi*tilde_psi) = pt_tt - c^2*pt_xx
    sq_pt = pt_tt - c_val**2 * pt_xx
    
    # Term 1 of L2:
    term1 = 0.5 * (-s_val * lam_v**2 * sq_pt)
    
    # Terms involving s^3:
    # s^3*lam^3*(alpha-1)*phi^3*tilde_psi*box_psi - s^3*lam^4*phi^3*tilde_psi^2
    # With alpha=1, first part vanishes
    term2 = -s_val**3 * lam_v**4 * phi_v**3 * tilde_psi**2
    
    # s^3*lam^3*(d/dt(phi^3*tilde_psi*psi_t) + c^2*d/dx(phi^3*tilde_psi*psi_x))
    phi3 = phi_v**3
    phi3_t = 3*phi_v**2 * phi_t
    phi3_x = 3*phi_v**2 * phi_x
    
    # d/dt(phi^3 * tilde_psi * psi_t)
    A_t = phi3 * tilde_psi * psi_t
    # = phi^3 * (1/T^2 - c^2/X^2) * (-1/T)
    # d/dt(A_t) = phi3_t*tilde_psi*psi_t + phi3*tilde_psi_t*psi_t + phi3*tilde_psi*psi_tt
    dA_t = phi3_t*tilde_psi*psi_t + phi3*tilde_psi_t*psi_t + phi3*tilde_psi*psi_tt
    
    # d/dx(phi^3 * tilde_psi * psi_x)
    B_x = phi3 * tilde_psi * psi_x
    dB_x = phi3_x*tilde_psi*psi_x + phi3*tilde_psi_x*psi_x + phi3*tilde_psi*psi_xx
    
    term3 = s_val**3 * lam_v**3 * (dA_t + c_val**2 * dB_x)
    
    L2_val = term1 + term2 + term3
    return L2_val

# Test at various points
print("\nWith N=20, s = -1/c^2:")
test_points = [
    (0, 0, 1),
    (10, 10, 1),
    (100, 100, 1),
    (1000, 1000, 1),
    (0, 0, 100),
    (0, 0, 0.01),
    (1e6, 0, 1),
    (1e10, 0, 1),
    (1e20, 0, 1),
    (0, 0, 1e6),
    (0, 0, 1e10),
]

for x_v, t_v, c_v in test_points:
    s_v = -1.0/c_v**2
    L2_v = eval_L2_numerically(x_v, t_v, c_v, 20, s_v)
    print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.0e}: L2 = {L2_v:.6e}")

print("\nWith N=20, s = -1/(c^2 + 1):")
for x_v, t_v, c_v in test_points:
    s_v = -1.0/(c_v**2 + 1)
    L2_v = eval_L2_numerically(x_v, t_v, c_v, 20, s_v)
    print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.0e}: L2 = {L2_v:.6e}")

# The critical test: does L2 remain positive for ALL x when s depends on c?
print("\nScanning x for fixed t=0, c=1, N=20, s=-1/c^2 = -1:")
for x_v in [1e5, 1e10, 1e15, 1e20, 1e30, 1e50, 1e100, 1e200]:
    s_v = -1.0
    L2_v = eval_L2_numerically(x_v, 0, 1, 20, s_v)
    print(f"  x={x_v:.0e}: L2 = {L2_v:.6e}")

print("\nNote: The Round 4 analysis showed that for the SEPARATED double-log,")
print("the failure occurs only at large c, not large x (for the O(s) vs O(s^3) competition).")
print("But the Round 5 analysis showed that for the COUPLED log, failure was at large x.")
print("For the separated double-log with s = -1/c^2, the c-dependence is removed,")
print("and the x-dependence is what matters. Let me check the x-asymptotics...")
print()

# The L2 for separated double-log at t=0 with general s:
# At t=0, x large: T=1, X=1+x~x
# phi = (1*x)^(1/N) = x^(1/N)
# tilde_psi = 1 - c^2/x^2 ~ 1
# box_psi = 1 - c^2/x^2 ~ 1
# 
# Term1 (O(s)): ~ s * lam^2 * derivatives of [x^(1/N) * 1]
#   = s * lam^2 * (0 - c^2 * d^2/dx^2[x^(1/N)])
#   = s * lam^2 * (-c^2) * (1/N)(1/N - 1) * x^(1/N - 2)
#   This is |s|*lam^2*c^2*(1-1/N)/N * x^(1/N-2) > 0
#
# Term2 (O(s^3)): ~ s^3 * lam^4 * x^(3/N) * 1 (negative)
#   = -|s|^3 * lam^4 * x^(3/N)
#
# Term3 (O(s^3)): ~ s^3 * lam^3 * c^2 * d/dx[x^(3/N) * 1 * (-1/x)]
#   = s^3 * lam^3 * c^2 * d/dx[-x^(3/N - 1)]
#   = s^3 * lam^3 * c^2 * (-(3/N - 1)) * x^(3/N - 2)
#   = |s|^3 * |lam|^3 * c^2 * (3/N - 1) * x^(3/N - 2)  (positive for N > 3)
#
# Competition: Term1 ~ |s|*c^2*x^(1/N - 2) vs Term2 ~ |s|^3*x^(3/N)
# The powers of x: 1/N - 2 vs 3/N
# 1/N - 2 < 3/N iff 1 - 2N < 3 iff -2N < 2 iff N > -1 (always true)
# So 3/N > 1/N - 2, meaning Term2 grows FASTER in x.
# 
# For large x: L2 ~ -|s|^3 * lam^4 * x^(3/N) + |s|^3 * |lam|^3 * c^2 * (3/N-1) * x^(3/N-2) + ...
# The leading x behavior is x^(3/N) (from Term2, negative) vs x^(3/N-2) (from Term3, positive).
# Since 3/N > 3/N - 2, Term2 dominates for large x. L2 -> -infinity!
# 
# Wait, but this contradicts the round 4 analysis which said the failure is at large c, not x.
# Let me recheck...

print("ASYMPTOTIC ANALYSIS at t=0, x -> infinity:")
print("Term1 (O(s)) ~ |s|*c^2*(N-1)/N^3 * x^(1/N-2)")
print("Term2 (O(s^3)) ~ -|s|^3/N^4 * x^(3/N)")  
print("Term3 (O(s^3)) ~ |s|^3*(3-N)/N^4 * c^2 * x^(3/N-2)")
print()
print("For N > 3: 3/N < 1, so 3/N > 3/N-2, and 1/N-2 < 0 < 3/N")
print("Leading term in x: -|s|^3/N^4 * x^(3/N) which is NEGATIVE and grows")
print("So L2 -> -infinity as x -> infinity, regardless of s!")
print()
print("THIS MEANS: for the separated double-log, L2 ALWAYS fails at large x,")
print("EVEN with s depending on c. The s(c) trick cannot fix this!")
print()
print("Wait - but the Round 4 failure analysis said the failure was at large c...")
print("Let me reconcile: at t=0, the 'R' factor is ((1)(1+x))^(2/N) = x^(2/N).")
print("The L2 numerator has form A(z) - B(z)*R where R = x^(2/N).")
print("At t=0, z = c^2/(1+x)^2 -> 0 for large x.")
print("So A(z) -> A(0) (positive constant) and B(z) -> B(0) (positive constant).")
print("L2_num = A(0) - B(0)*x^(2/N) -> -infinity.")
print("This happens for ANY c > 0 and ANY s!")
print()
print("So the SEPARATED double-log ALSO fails at large x, not just at large c!")
print("The Round 4 analysis was looking at different variables (z, R) and")
print("may have missed this regime. Let me double-check numerically...")

for x_v in [1e10, 1e20, 1e50, 1e100, 1e200, 1e300]:
    c_v = 1.0
    s_v = -0.01
    L2_v = eval_L2_numerically(x_v, 0, c_v, 20, s_v)
    print(f"  x={x_v:.0e}, c={c_v}, s={s_v}: L2 = {L2_v:.6e}")

