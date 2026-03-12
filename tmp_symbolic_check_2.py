import sympy as sp

x, t = sp.symbols('x t', nonnegative=True)
c = sp.symbols('c', positive=True)

# Power-law ansatz: psi = -(1+x)^q for some 0 < q < 1
# Combined with t dependence
# Try psi = beta*t - (1+x)^q

# For L1 <= 0 with lambda < 0:
# L1/phi = lam^2*((psi_t)^2 + c^2*(psi_x)^2) + lam*(psi_tt + c^2*psi_xx)

# psi = beta*t - (1+x)^q
# psi_t = beta, psi_tt = 0
# psi_x = -q*(1+x)^(q-1), psi_xx = -q*(q-1)*(1+x)^(q-2)
# (psi_t)^2 = beta^2
# (psi_x)^2 = q^2*(1+x)^(2q-2)
# psi_tt + c^2*psi_xx = -c^2*q*(q-1)*(1+x)^(q-2)

# L1/phi = lam^2*(beta^2 + c^2*q^2*(1+x)^(2q-2)) + lam*(-c^2*q*(q-1)*(1+x)^(q-2))

# For L1 <= 0: the lam^2 term (positive) must be dominated by -lam*(c^2*q*(q-1)*(1+x)^(q-2))
# With lam < 0: -lam > 0, so we need q-1 < 0, i.e., q < 1. Then q*(q-1) < 0, so
# -lam*(-c^2*q*(q-1)*(1+x)^(q-2)) = -lam*c^2*q*(1-q)*(1+x)^(q-2)
# This is |lam|*c^2*q*(1-q)*(1+x)^(q-2), which is POSITIVE and decays as (1+x)^(q-2).

# The gradient term: lam^2*c^2*q^2*(1+x)^(2q-2)
# This decays as (1+x)^(2q-2).

# For the Laplacian to dominate: need (1+x)^(q-2) to dominate (1+x)^(2q-2)
# i.e., q-2 > 2q-2, i.e., -q > 0, i.e., q < 0. But we assumed q > 0!

# So for 0 < q < 1: 2q-2 < q-2 < -1, both decay, but 2q-2 < q-2 means
# (1+x)^(2q-2) decays FASTER than (1+x)^(q-2). Good!

# At x = 0: L1/phi = lam^2*(beta^2 + c^2*q^2) + lam*(-c^2*q*(q-1))
# = lam^2*(beta^2 + c^2*q^2) + |lam|*c^2*q*(1-q)  [since lam < 0, -lam = |lam|]
# For this to be <= 0: need |lam|*c^2*q*(1-q) <= -lam^2*(beta^2 + c^2*q^2)
# But lam^2 = |lam|^2, so: |lam|*c^2*q*(1-q) <= |lam|^2*(beta^2 + c^2*q^2)... wait
# L1/phi = lam^2*P + lam*Q where P = beta^2 + c^2*q^2*(1+x)^(2q-2), Q = -c^2*q*(q-1)*(1+x)^(q-2)
# = |lam|^2*P - |lam|*Q  [since lam < 0, lam = -|lam|]
# Wait: lam*Q = (-|lam|)*Q. Q = -c^2*q*(q-1)*(1+x)^(q-2)
# For 0<q<1: q-1 < 0, so Q = c^2*q*(1-q)*(1+x)^(q-2) > 0
# lam*Q = -|lam|*Q < 0. So:
# L1/phi = |lam|^2*P - |lam|*Q
# For L1 <= 0: |lam|*P <= Q
# At x=0: |lam|*(beta^2 + c^2*q^2) <= c^2*q*(1-q)
# As x->inf: |lam|*(beta^2) <= 0 (since Q->0, P->beta^2). This requires beta = 0!

# If beta = 0: psi = -(1+x)^q, psi_t = 0
# Then L1/phi = |lam|^2*c^2*q^2*(1+x)^(2q-2) - |lam|*c^2*q*(1-q)*(1+x)^(q-2)
#             = |lam|*c^2*q*(1+x)^(q-2)*[|lam|*q*(1+x)^(q) - (1-q)]
# As x->inf: the [...] -> +inf, so L1/phi > 0 for large x. FAILS.

print("Power-law ansatz for 0 < q < 1 fails: gradient grows faster than Laplacian at infinity")
print("The self-similar property (psi_x)^2 = psi_xx is unique to logarithmic forms")
print()

# What about combining log with something that kills the L2 problem?
# The L2 issue comes from phi^3 * tilde_square(psi)^2 growing too fast.
# For psi = -log(1+t) - log(1+x): tilde_square(psi) = 1/(1+t)^2 - c^2/(1+x)^2
# This doesn't decay to 0; it approaches -c^2/(1+x)^2 as t->inf.

# What if tilde_square(psi) = 0? Then psi_t^2 = c^2*psi_x^2.
# For separated form: f'(t)^2 = c^2*g'(x)^2, so f'(t) = +/-c*g'(x).
# This requires f'(t) and g'(x) both constant: f(t) = at, g(x) = bx, with a = +/-cb.
# So psi = at +/- cbx = a(t +/- cx/...). Actually psi = a*t - a*c*x = a*(t-cx) or a*(t+cx).
# Or more generally psi = f(t - cx) or f(t + cx).

# For psi = -log(1+x+ct): a TRAVELING WAVE solution!
psi_tw = -sp.ln(1 + x + c*t)
psi_t_tw = sp.diff(psi_tw, t)
psi_x_tw = sp.diff(psi_tw, x)
psi_tt_tw = sp.diff(psi_tw, t, 2)
psi_xx_tw = sp.diff(psi_tw, x, 2)

tilde_psi_tw = psi_t_tw**2 - c**2 * psi_x_tw**2
box_psi_tw = psi_tt_tw - c**2 * psi_xx_tw

print("TRAVELING WAVE ANSATZ psi = -log(1+x+ct):")
print("psi_t =", sp.simplify(psi_t_tw))
print("psi_x =", sp.simplify(psi_x_tw))
print("psi_tt =", sp.simplify(psi_tt_tw))
print("psi_xx =", sp.simplify(psi_xx_tw))
print("tilde(psi) =", sp.simplify(tilde_psi_tw))
print("box(psi) =", sp.simplify(box_psi_tw))
print()

# L1 check
lam = sp.Symbol('lam', negative=True)
grad_sq = psi_t_tw**2 + c**2 * psi_x_tw**2
lapl_sum = psi_tt_tw + c**2 * psi_xx_tw

L1_over_phi = lam**2 * grad_sq + lam * lapl_sum
L1_simplified = sp.simplify(L1_over_phi)
print("L1/phi = lam^2*(psi_t^2 + c^2*psi_x^2) + lam*(psi_tt + c^2*psi_xx)")
print("       =", L1_simplified)

# Factor out common terms
print("\nWith lam = -1/20:")
L1_at_lam = L1_simplified.subs(lam, sp.Rational(-1, 20))
L1_at_lam_simplified = sp.simplify(L1_at_lam)
print("L1/phi =", L1_at_lam_simplified)
print("       =", sp.factor(L1_at_lam_simplified))
print()

# L = lam^2*phi*tilde(psi) - (alpha-1)*lam*phi*box(psi)
# With alpha=1 and tilde(psi) = 0: L = 0
print("L = lam^2*phi*tilde(psi) = lam^2*phi*0 = 0")
print("Condition 1: L1 <= L <= -L1 becomes L1 <= 0 <= -L1, which holds since L1 <= 0")
print()

# Sufficient condition check
print("Sufficient condition: L1^2 - L^2 >= c^2*phi_xt^2")
print("Since L = 0: L1^2 >= c^2*phi_xt^2")

lam_val = sp.Rational(-1, 20)
phi_tw = sp.exp(lam_val * psi_tw)
phi_tw_simplified = sp.simplify(phi_tw)
print("\nphi =", phi_tw_simplified)

phi_xt = sp.diff(phi_tw, x, t)
phi_xt_simplified = sp.simplify(phi_xt)
print("phi_xt =", phi_xt_simplified)

L1_full = lam_val**2 * (psi_t_tw**2 + c**2*psi_x_tw**2) * phi_tw + lam_val * (psi_tt_tw + c**2*psi_xx_tw) * phi_tw
L1_full_simplified = sp.simplify(L1_full)
print("L1 =", L1_full_simplified)

diff_expr = L1_full**2 - c**2 * phi_xt**2
diff_simplified = sp.simplify(diff_expr)
print("\nL1^2 - c^2*phi_xt^2 =", diff_simplified)

# Factor
diff_factored = sp.factor(diff_simplified)
print("Factored:", diff_factored)
print()

# Check sign
# Let u = 1+x+ct, then this should be positive
u = sp.Symbol('u', positive=True)
print("Substituting u = 1+x+ct:")
diff_in_u = diff_simplified.subs(1+x+c*t, u)
diff_in_u_simplified = sp.simplify(diff_in_u)
print("L1^2 - c^2*phi_xt^2 =", diff_in_u_simplified)
print()

print("NOW: What about L2?")
print("With box(psi) = 0 and tilde_square(psi) = 0:")
print("ALL TERMS IN L2 ARE ZERO -> L2 = 0")
print()
print("KEY QUESTION: Does the verify_engine check >= 0 or > 0?")
print("If strict > 0 is required, L2 = 0 fails.")
print("If >= 0 suffices, this traveling wave ansatz solves everything!")
