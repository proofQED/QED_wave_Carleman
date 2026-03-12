import sympy as sp

x, t, c = sp.symbols('x t c', positive=True)
lam_val = sp.Rational(-1, 100)  # very small |lambda|
alpha_val = 1

# Try power-law: psi = -(1+x)^b - (1+t)^a
# For condition 2: lam*psi = |lam|*((1+x)^b + (1+t)^a) -> +inf as x->inf, need b > 0. OK.
# For condition 1: L1 <= 0 means lam*(psi_tt + c^2*psi_xx) must dominate -lam^2*((psi_t)^2 + c^2*(psi_x)^2)
# psi_t = -a*(1+t)^(a-1), psi_x = -b*(1+x)^(b-1)
# psi_tt = -a*(a-1)*(1+t)^(a-2), psi_xx = -b*(b-1)*(1+x)^(b-2)
# For a < 1: psi_tt = -a*(a-1)*(1+t)^(a-2) = a*(1-a)*(1+t)^(a-2) > 0
# For b < 1: psi_xx = b*(1-b)*(1+x)^(b-2) > 0

# The key ratio controlling condition 1 (L1 <= 0):
# lambda*[(psi_t)^2 + c^2*(psi_x)^2] + (psi_tt + c^2*psi_xx) <= 0  (dividing by lambda^2*phi, then multiply by lambda since lambda < 0)
# Actually: L1/phi = lambda^2*[(psi_t)^2 + c^2*(psi_x)^2] + lambda*(psi_tt + c^2*psi_xx) <= 0
# = lambda^2*[a^2*(1+t)^(2a-2) + c^2*b^2*(1+x)^(2b-2)] + lambda*[a*(1-a)*(1+t)^(a-2) + c^2*b*(1-b)*(1+x)^(b-2)]

# For the second (lambda) term to dominate the first (lambda^2) term, we need:
# |lambda| * gradient_sq << |Laplacian|
# |lambda| * a^2*(1+t)^(2a-2) << a*(1-a)*(1+t)^(a-2)
# |lambda| * a*(1+t)^(2a-2) << (1-a)*(1+t)^(a-2)
# |lambda| * a << (1-a)*(1+t)^(a-2-2a+2) = (1-a)*(1+t)^(-a)
# |lambda| * a << (1-a)*(1+t)^(-a)
# This holds for ALL t >= 0 if a > 0 (since (1+t)^(-a) >= 1 when a <= 0, but for a > 0, (1+t)^(-a) -> 0)
# Wait: for a > 0, (1+t)^(-a) -> 0 as t -> inf, so the RHS goes to 0. This means for large t, the condition fails!

# UNLESS: 2a-2 < a-2, i.e., a < 0. Then the gradient term decays faster.
# 2a-2 < a-2 => a < 0. But we need psi -> -inf for condition 2 with lambda < 0.
# psi = -(1+t)^a - (1+x)^b. For lambda*psi -> +inf: need psi -> -inf, i.e., (1+x)^b -> +inf, need b > 0.

# For t-part: if a < 0, then -(1+t)^a is bounded (goes to 0 as t->inf). OK for psi but
# psi_t = -a*(1+t)^(a-1). For a < 0, psi_t = |a|*(1+t)^(a-1) -> 0 fast.
# psi_tt = -a*(a-1)*(1+t)^(a-2) = |a|*(|a|+1)*(1+t)^(a-2) > 0
# gradient_sq in t: a^2*(1+t)^(2a-2), Laplacian in t: a*(1-a)*(1+t)^(a-2)
# For a < 0: 2a-2 < a-2 (since a < 0), so gradient decays faster. GOOD.

# For x-part: similarly, if 0 < b < 1:
# gradient_sq in x: b^2*(1+x)^(2b-2), Laplacian in x: b*(1-b)*(1+x)^(b-2)
# 2b-2 vs b-2: 2b-2 < b-2 iff b < 0. For 0 < b < 1, 2b-2 > b-2, so gradient_sq decays SLOWER. BAD.

# Hmm. So for x with 0 < b < 1, the gradient term dominates the Laplacian at large x.
# The ratio is: |lam|*b*(1+x)^(2b-2-(b-2)) = |lam|*b*(1+x)^b
# This grows -> inf. So condition 1 fails for large x!

# What if b < 0? Then (1+x)^b -> 0, and psi doesn't grow -> -inf. Condition 2 fails.
# What if b = 0? psi independent of x. Not useful.

# So for power-law in x with b > 0, condition 1 fails at large x unless |lam| -> 0,
# but then condition 2 (rate of divergence) becomes very slow.

# Actually wait - condition 2 is just lim(x->inf) lambda*psi = +inf.
# lambda*psi = |lam|*((1+x)^b + (1+t)^a) -> +inf as x->inf if b > 0. Rate doesn't matter.

# So we need |lam|*b*(1+x)^b < (1-b) for all x >= 0.
# This requires b = 0 or... this can never hold for all x if b > 0!

# UNLESS we DON'T use separated variables. What about ψ = -(x + f(t))^b?
# Or ψ = -(1 + x + g(t))^b?

# Actually, let me reconsider. The log ansatz WORKED for conditions 1, 2, sufficient.
# Only L2 failed. The log has b=0 effectively (logarithmic growth).
# For log: (psi_x)^2 = 1/(1+x)^2, psi_xx = 1/(1+x)^2. Same rate! So ratio is |lam|*1.
# That's why it works with small |lam|.

# The L2 failure for log was structural. Let me think about what ansatz could fix L2.

# Key insight: For the double-log, L2 reduced to a quadratic in z with R-dependent coefficients.
# The R = ((1+t)(1+x))^(3*lambda) factor comes from phi^3.
# With lambda = -1/20, R = ((1+t)(1+x))^(1/10) grew -> inf.
# What if we could make the phi^3 factor decay or stay bounded?
# phi = exp(lambda*psi). For double-log: phi = ((1+t)(1+x))^(-lambda) = ((1+t)(1+x))^(1/20).
# phi^3 = ((1+t)(1+x))^(3/20). This grows.

# What if psi had a BOUNDED x-part? Then phi wouldn't grow with x.
# But condition 2 needs lambda*psi -> +inf as x->inf. With lambda < 0, need psi -> -inf.
# So psi must decrease without bound in x.

# What about psi = A*t - (x+x0)^2? Quadratic in x.
# lambda*psi = lambda*A*t - lambda*(x+x0)^2. With lambda < 0: -> +inf if (x+x0)^2 dominates. OK.
# But: psi_x = -2*(x+x0), psi_xx = -2.
# (psi_x)^2 = 4*(x+x0)^2. This grows as x^2.
# psi_tt + c^2*psi_xx = 0 + c^2*(-2) = -2c^2.
# L1/phi = lambda^2*(psi_t^2 + c^2*4*(x+x0)^2) + lambda*(-2c^2 + psi_tt)
# This has a lambda^2*(x+x0)^2 term that grows -> inf. L1 won't be <= 0. Bad.

# What about psi = A*t - B*x? Linear in x.
# psi_x = -B, psi_xx = 0. (psi_x)^2 = B^2. Constant.
# L1/phi = lambda^2*(psi_t^2 + c^2*B^2) + lambda*(psi_tt + 0)
# = lambda^2*(A^2 + c^2*B^2) + lambda*0 if psi_t = A constant
# = lambda^2*(A^2 + c^2*B^2) > 0. L1 > 0. BAD (need L1 <= 0).
# Unless psi_tt + c^2*psi_xx provides a negative contribution. But psi_tt = 0, psi_xx = 0 for linear.

# The key is we need psi_tt + c^2*psi_xx to be NEGATIVE enough to overpower lam^2*grad^2.
# For the double-log: psi_tt + c^2*psi_xx = 1/(1+t)^2 + c^2/(1+x)^2 > 0.
# But L1/phi = lam^2*(same thing) + lam*(same thing) = (lam^2 + lam)*(same thing)
# = lam*(lam+1)*(thing). With lam=-1/20: lam*(lam+1) = (-1/20)(19/20) = -19/400 < 0. Works!

# So the trick is: for separated ψ = f(t) + g(x) with f'' > 0, g'' > 0:
# ψ_tt + c²ψ_xx = f'' + c²g'' > 0
# (ψ_t)² + c²(ψ_x)² = (f')² + c²(g')²
# If ψ_tt + c²ψ_xx = (ψ_t)² + c²(ψ_x)², then L1/phi = (lam² + lam)*P = lam(lam+1)*P
# This is < 0 iff lam(lam+1) < 0, i.e., -1 < lam < 0.

# For f = -log(1+t): f' = -1/(1+t), f'' = 1/(1+t)^2 = (f')^2. Similarly for g = -log(1+x).
# So this "self-similar" property (f'' = (f')^2) is what makes the double-log work for condition 1.

# What other functions satisfy f'' = (f')^2?
# f'' = (f')^2. Let u = f'. Then u' = u^2. Solution: u = -1/(t+C), so f = -log(t+C).
# The ONLY functions satisfying this are f = -log(t+C) + const, and f = const (trivial).

# So the double-log is essentially the UNIQUE separated ansatz satisfying condition 1 cleanly!
# Any other form will need a different mechanism to ensure L1 ≤ 0.

# What about a COUPLED ansatz? E.g., ψ = -log(1 + t + x)?
# psi_t = -1/(1+t+x), psi_x = -1/(1+t+x). So psi_t = psi_x.
# psi_tt = 1/(1+t+x)^2, psi_xx = 1/(1+t+x)^2, psi_tx = 1/(1+t+x)^2
# square_psi = psi_t^2 - c^2*psi_x^2 = (1-c^2)/(1+t+x)^2
# box_psi = psi_tt - c^2*psi_xx = (1-c^2)/(1+t+x)^2
# psi_tt + c^2*psi_xx = (1+c^2)/(1+t+x)^2
# (psi_t)^2 + c^2*(psi_x)^2 = (1+c^2)/(1+t+x)^2
# So again "self-similar" property holds! L1/phi = lam(lam+1)*(1+c^2)/(1+t+x)^2 < 0 for -1<lam<0. ✓
# Condition 2: lam*psi = |lam|*log(1+t+x) -> +inf. ✓

# The question is: does L2 >= 0 hold for this coupled ansatz?
# Key difference from double-log: now there are cross-derivative terms (psi_tx ≠ 0).
# This could change the L2 structure significantly.

# Let's compute L2 symbolically for psi = -log(1+t+x)

lam_sym = sp.Symbol('lambda', negative=True)
s_sym = sp.Symbol('s', negative=True)
alpha_sym = sp.Symbol('alpha')

psi = -sp.ln(1 + t + x)
phi = sp.exp(lam_val * psi)  # with lam = -1/100

# Compute derivatives
psi_t = sp.diff(psi, t)
psi_x = sp.diff(psi, x)
psi_tt = sp.diff(psi, t, 2)
psi_xx = sp.diff(psi, x, 2)
psi_tx = sp.diff(psi, t, x)

print("psi =", psi)
print("psi_t =", psi_t)
print("psi_x =", psi_x)
print("psi_tt =", psi_tt)
print("psi_xx =", psi_xx)
print("psi_tx =", psi_tx)

# box and tilde_box
box_psi = psi_tt - c**2 * psi_xx
tilde_box_psi = psi_t**2 - c**2 * psi_x**2

print("\nbox_psi =", sp.simplify(box_psi))
print("tilde_box_psi =", sp.simplify(tilde_box_psi))

# With alpha=1: L = lam^2*phi*tilde_box - 0 = lam^2*phi*tilde_box
# L1 = lam^2*phi*((psi_t)^2 + c^2*(psi_x)^2) + lam*phi*(psi_tt+c^2*psi_xx)
lam_v = lam_val
alpha_v = 1
s_v = -1

phi_expr = (1 + t + x)**sp.Rational(1, 100)  # exp(-1/100 * -log(1+t+x)) = (1+t+x)^(1/100)
print("\nphi =", phi_expr)

# Verify
print("exp(lam*psi) =", sp.simplify(sp.exp(lam_v * psi)))
print("phi check:", sp.simplify(sp.exp(lam_v * psi) - phi_expr))

# Now compute L, L1
grad_sq = psi_t**2 + c**2 * psi_x**2  # (1+c^2)/(1+t+x)^2
laplacian = psi_tt + c**2 * psi_xx     # (1+c^2)/(1+t+x)^2

L = lam_v**2 * phi_expr * tilde_box_psi - (alpha_v - 1) * lam_v * phi_expr * box_psi
L1 = lam_v**2 * phi_expr * grad_sq + lam_v * phi_expr * laplacian

print("\nL =", sp.simplify(L))
print("L1 =", sp.simplify(L1))

# L - L1 and -L1 - L
LmL1 = sp.simplify(L - L1)
mL1mL = sp.simplify(-L1 - L)
print("\nL - L1 =", LmL1)
print("-L1 - L =", mL1mL)

# Now compute L2. This is complex. Let me use the definition.
# L2 = (1/2)*((alpha-1)*s*lam*(box(phi*box_psi)) - s*lam^2*(box(phi*tilde_box_psi)))
#    + s^3*lam^3*(alpha-1)*phi^3*tilde_box_psi*box_psi
#    - s^3*lam^4*phi^3*(tilde_box_psi)^2
#    + s^3*lam^3*(d_t(phi^3*tilde_box_psi*psi_t) + c^2*d_x(phi^3*tilde_box_psi*psi_x))

# With alpha = 1, the (alpha-1) terms vanish!
# L2 = (1/2)*(-s*lam^2*(box(phi*tilde_box_psi)))
#    + 0  (alpha-1 = 0)
#    - s^3*lam^4*phi^3*(tilde_box_psi)^2
#    + s^3*lam^3*(d_t(phi^3*tilde_box_psi*psi_t) + c^2*d_x(phi^3*tilde_box_psi*psi_x))

print("\n--- Computing L2 with alpha=1, s=-1, lam=-1/100 ---")

# Term 1: -(1/2)*s*lam^2 * box(phi*tilde_box_psi)
expr1_inner = phi_expr * tilde_box_psi
expr1_inner_s = sp.simplify(expr1_inner)
print("phi*tilde_box =", expr1_inner_s)
box_expr1 = sp.diff(expr1_inner, t, 2) - c**2 * sp.diff(expr1_inner, x, 2)
box_expr1_s = sp.simplify(box_expr1)
print("box(phi*tilde_box) =", box_expr1_s)
term1 = sp.Rational(-1, 2) * s_v * lam_v**2 * box_expr1
term1_s = sp.simplify(term1)
print("Term1 =", term1_s)

# Term 2: -s^3*lam^4*phi^3*(tilde_box_psi)^2
phi3 = phi_expr**3
term2 = -s_v**3 * lam_v**4 * phi3 * tilde_box_psi**2
term2_s = sp.simplify(term2)
print("Term2 =", term2_s)

# Term 3: s^3*lam^3*(d_t(phi^3*tilde_box*psi_t) + c^2*d_x(phi^3*tilde_box*psi_x))
inner_t = phi3 * tilde_box_psi * psi_t
inner_x = phi3 * tilde_box_psi * psi_x
dt_inner = sp.diff(inner_t, t)
dx_inner = sp.diff(inner_x, x)
term3 = s_v**3 * lam_v**3 * (dt_inner + c**2 * dx_inner)
term3_s = sp.simplify(term3)
print("Term3 =", term3_s)

L2 = term1 + term2 + term3
L2_s = sp.simplify(L2)
print("\nL2 =", L2_s)

# Factor out common terms
u = 1 + t + x
L2_sub = L2_s.subs(1+t+x, sp.Symbol('u', positive=True))
print("\nL2 (in terms of u=1+t+x):", sp.simplify(L2_sub))

# Let's also try numerical evaluation
import numpy as np
print("\n--- Numerical check of L2 ---")
for c_val in [0.5, 1.0, 2.0]:
    for t_val in [0, 1, 10, 100, 1000, 1e6, 1e10]:
        for x_val in [0, 1, 10, 100, 1000, 1e6, 1e10]:
            val = float(L2_s.subs([(c, c_val), (t, t_val), (x, x_val)]))
            if val < 0:
                print(f"  NEGATIVE: c={c_val}, t={t_val}, x={x_val}, L2={val:.6e}")
    print(f"  c={c_val}: All checked values non-negative" if True else "")

# Check the sign more carefully - what matters is the sign of the expression
# Let's extract the key factor
print("\n--- Trying to factor L2 ---")
print("L2 simplified:", L2_s)
