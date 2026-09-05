"""
Explore two-wave ansatz: psi = -log(1+x+ct) - log(1+x-ct+2cT)
or similar combinations that make tilde(psi) small but not exactly 0.

Also explore: psi = -log((1+x)^2 + c^2*t^2) which mixes x and t symmetrically.
"""
import sympy as sp
import mpmath
from verify_engine import x, t, c, x0, alpha, s, lam, build_operators, truth_value_from_sign, run_verification

print("="*80)
print("IDEA 1: psi = -log((1+x)^2 + c^2*(1+t)^2)")
print("="*80)

# This is a radial-type function in (x, ct) space
psi1 = -sp.ln((1 + x)**2 + c**2*(1 + t)**2)

psi1_t = sp.diff(psi1, t)
psi1_x = sp.diff(psi1, x)
psi1_tt = sp.diff(psi1, t, 2)
psi1_xx = sp.diff(psi1, x, 2)

print("psi_t =", sp.simplify(psi1_t))
print("psi_x =", sp.simplify(psi1_x))
print("(psi_t)^2 + c^2*(psi_x)^2 =", sp.simplify(psi1_t**2 + c**2*psi1_x**2))
print("psi_tt + c^2*psi_xx =", sp.simplify(psi1_tt + c**2*psi1_xx))

# L1/phi ratio: lam^2*((psi_t)^2 + c^2*(psi_x)^2) + lam*(psi_tt + c^2*psi_xx)
# Let u = (1+x)^2 + c^2*(1+t)^2
# psi_t = -2c^2*(1+t)/u, psi_x = -2(1+x)/u
# (psi_t)^2 = 4c^4*(1+t)^2/u^2, (psi_x)^2 = 4(1+x)^2/u^2
# (psi_t)^2 + c^2*(psi_x)^2 = 4c^2*(c^2*(1+t)^2 + (1+x)^2)/u^2 = 4c^2*u/u^2 = 4c^2/u

# psi_tt = -2c^2/u + 4c^4*(1+t)^2/u^2 = -2c^2*(u - 2c^2*(1+t)^2)/u^2 = -2c^2*((1+x)^2 - c^2*(1+t)^2)/u^2
# psi_xx = -2/u + 4(1+x)^2/u^2 = -2*(u-2(1+x)^2)/u^2 = -2*(c^2*(1+t)^2 - (1+x)^2)/u^2
# = 2*((1+x)^2 - c^2*(1+t)^2)/u^2

# psi_tt + c^2*psi_xx = -2c^2*((1+x)^2-c^2*(1+t)^2)/u^2 + 2c^2*((1+x)^2-c^2*(1+t)^2)/u^2 = 0!

# So psi_tt + c^2*psi_xx = 0 (this is the harmonic/Laplace condition in the (x,ct) plane)
# Then L1/phi = lam^2*4c^2/u + lam*0 = 4c^2*lam^2/u > 0!
# L1 > 0, violating condition 1.

print("\nL1/phi = 4c^2*lam^2/u > 0 ALWAYS. Condition 1 FAILS.")
print("This is because psi_tt + c^2*psi_xx = 0 (harmonic in (x,ct)).")
print("The Laplacian term that was supposed to make L1 negative is missing!")

print("\n" + "="*80)
print("IDEA 2: psi = -log((1+x)^2 + (1+t)^2)")
print("(Note: no c in the argument)")
print("="*80)

psi2 = -sp.ln((1 + x)**2 + (1 + t)**2)
u_sym = (1 + x)**2 + (1 + t)**2

psi2_t = sp.diff(psi2, t)
psi2_x = sp.diff(psi2, x)
psi2_tt = sp.diff(psi2, t, 2)
psi2_xx = sp.diff(psi2, x, 2)

L1_ratio = sp.simplify(sp.Rational(-1, 20)**2*(psi2_t**2 + c**2*psi2_x**2) + sp.Rational(-1, 20)*(psi2_tt + c**2*psi2_xx))
print("L1/phi =", sp.factor(sp.simplify(L1_ratio)))

# psi_tt + c^2*psi_xx = -2(u - 2(1+t)^2)/u^2 + c^2*(-2)(u - 2(1+x)^2)/u^2
# = (-2/u^2)*(u - 2(1+t)^2 + c^2*(u - 2(1+x)^2))
# = (-2/u^2)*((1+c^2)*u - 2(1+t)^2 - 2c^2*(1+x)^2)
# = (-2/u^2)*((1+c^2)*((1+x)^2+(1+t)^2) - 2(1+t)^2 - 2c^2*(1+x)^2)
# = (-2/u^2)*((1+c^2-2)(1+t)^2 + (1+c^2-2c^2)(1+x)^2)  wait...
# = (-2/u^2)*((c^2-1)(1+t)^2 + (1-c^2)(1+x)^2)
# = (-2/u^2)*(c^2-1)*((1+t)^2 - (1+x)^2)

# So psi_tt + c^2*psi_xx = -2(c^2-1)*((1+t)^2-(1+x)^2)/u^2
# This changes sign depending on c vs 1 and t vs x. Not clean.

print("\npsi_tt + c^2*psi_xx = -2(c^2-1)*((1+t)^2-(1+x)^2)/((1+x)^2+(1+t)^2)^2")
print("This changes sign. Not useful.")

print("\n" + "="*80)
print("IDEA 3: psi = -A*log(1+x+ct) - B*log(1+x-ct+D)")
print("Two traveling waves in opposite directions")
print("="*80)

# For this to make sense, we need 1+x-ct+D > 0 for all x >= 0, t >= 0.
# This requires D - ct >= -x-1 for all t, x. But for t -> infinity, D - ct -> -infinity,
# so 1+x-ct+D < 0 for large t. BAD.

# Alternative: 1+x+ct and 1+x are both always positive.
# Use psi = -A*log(1+x+ct) - B*log(1+x) (this is Round 5's form)

# What about psi = -log((1+x+ct)(1+x))?
# This is exactly psi = -log(1+x+ct) - log(1+x) = Round 5's form.

# What about psi = -log(1+x+ct) - log(1+ct)?
# 1+ct > 0 for all t >= 0. ✓
# psi_t = -c/(1+x+ct) - c/(1+ct)
# psi_x = -1/(1+x+ct)
# box(psi) = c^2/(1+x+ct)^2 - c^2/(1+x+ct)^2 + c^2/(1+ct)^2 - 0 = c^2/(1+ct)^2
# tilde(psi) = (c/(1+x+ct) + c/(1+ct))^2 - c^2/(1+x+ct)^2
# = c^2/(1+ct)^2 + 2c^2/((1+x+ct)(1+ct))
# This is always positive!

print("Testing psi = -log(1+x+ct) - log(1+ct):")
psi3 = -sp.ln(1 + x + c*t) - sp.ln(1 + c*t)

box3 = sp.simplify(sp.diff(psi3, t, 2) - c**2 * sp.diff(psi3, x, 2))
tilde3 = sp.simplify(sp.diff(psi3, t)**2 - c**2 * sp.diff(psi3, x)**2)

print("box(psi) =", box3)
print("tilde(psi) =", tilde3)

# Condition 2: lam*psi = |lam|*(log(1+x+ct)+log(1+ct)) -> +inf as x -> inf ✓

# L1/phi check
grad_sq3 = sp.simplify(sp.diff(psi3, t)**2 + c**2*sp.diff(psi3, x)**2)
lapl3 = sp.simplify(sp.diff(psi3, t, 2) + c**2*sp.diff(psi3, x, 2))
print("(psi_t)^2 + c^2*(psi_x)^2 =", grad_sq3)
print("psi_tt + c^2*psi_xx =", lapl3)

lam_v = sp.Rational(-1, 20)
L1_ratio3 = lam_v**2 * grad_sq3 + lam_v * lapl3
L1_ratio3_simplified = sp.simplify(L1_ratio3)
print("\nL1/phi =", L1_ratio3_simplified)

# Check sign: need L1/phi < 0
# lam^2 * (grad_sq) + lam * (lapl)
# = (1/400)*grad_sq - (1/20)*lapl
# Need: (1/20)*lapl > (1/400)*grad_sq
# i.e., 20*lapl > grad_sq

# Let u = 1+x+ct, v = 1+ct
# psi_t = -c/u - c/v, psi_x = -1/u
# grad_sq = c^2/u^2 + 2c^2/(uv) + c^2/v^2 + c^2/u^2 = 2c^2/u^2 + 2c^2/(uv) + c^2/v^2
# lapl = c^2/u^2 + 2c^3/(uv)... wait, let me just compute
# psi_tt = c^2/u^2 + c^2/v^2
# psi_xx = 1/u^2
# lapl = c^2/u^2 + c^2/v^2 + c^2/u^2 = 2c^2/u^2 + c^2/v^2
# grad_sq = (c/u+c/v)^2 + c^2/u^2 = c^2/u^2 + 2c^2/(uv) + c^2/v^2 + c^2/u^2
#         = 2c^2/u^2 + 2c^2/(uv) + c^2/v^2

# So L1/phi = (1/400)*(2c^2/u^2 + 2c^2/(uv) + c^2/v^2) - (1/20)*(2c^2/u^2 + c^2/v^2)
# = c^2*[(2/400 - 2/20)/u^2 + 2/(400*uv) + (1/400-1/20)/v^2]
# = c^2*[(2/400 - 40/400)/u^2 + 2/(400*uv) + (1/400 - 20/400)/v^2]
# = c^2*[(-38/400)/u^2 + (2/400)/(uv) + (-19/400)/v^2]
# = c^2/(400)*[-38/u^2 + 2/(uv) - 19/v^2]
# = c^2/(400)*[-(38/u^2 - 2/(uv) + 19/v^2)]

# Check if 38/u^2 - 2/(uv) + 19/v^2 > 0:
# = 38*v^2/(u^2*v^2) - 2*u/(u^2*v^2) + 19*u^2/(u^2*v^2)
# Wait... let me redo: 38/u^2 - 2/(uv) + 19/v^2
# Multiply by u^2*v^2: 38*v^2 - 2*u*v + 19*u^2
# This is a quadratic in u: 19*u^2 - 2*v*u + 38*v^2
# Discriminant: 4*v^2 - 4*19*38*v^2 = 4*v^2*(1 - 722) < 0
# So always positive! ✓

print("\n38/u^2 - 2/(uv) + 19/v^2 is positive definite (discriminant < 0)")
print("Therefore L1/phi < 0 for all x, t. ✓")

# Now check condition 1: L - L1 > 0 and -L1 - L > 0
# With alpha=1: L = lam^2*phi*tilde(psi)
# tilde(psi) = c^2/v^2 + 2c^2/(uv) > 0
# So L > 0.
# L - L1: L > 0 and L1 < 0, so L - L1 > 0. ✓
# -L1 - L: -L1 > 0, but -L > 0... wait, L > 0, so -L < 0.
# -L1 - L = -L1 + (-L). -L1 > 0 but -L < 0.
# Need -L1 > L, i.e., |L1| > L.
# L = lam^2*phi*tilde = (1/400)*phi*(c^2/v^2 + 2c^2/(uv))
# |L1| = |L1/phi|*phi = c^2/(400)*phi*(38/u^2 - 2/(uv) + 19/v^2)
# L/phi = (1/400)*c^2*(1/v^2 + 2/(uv))
# |L1|/phi = c^2/(400)*(38/u^2 - 2/(uv) + 19/v^2)
# |L1| - L = c^2*phi/(400)*[38/u^2 - 2/(uv) + 19/v^2 - 1/v^2 - 2/(uv)]
# = c^2*phi/(400)*[38/u^2 - 4/(uv) + 18/v^2]
# = c^2*phi/(400)*2*[19/u^2 - 2/(uv) + 9/v^2]
# Check: 19/u^2 - 2/(uv) + 9/v^2. Multiply by u^2*v^2: 19*v^2 - 2*u*v + 9*u^2.
# Discriminant: 4 - 4*19*9 = 4*(1-171) < 0. Always positive! ✓

print("-L1 - L > 0: 19/u^2 - 2/(uv) + 9/v^2 positive definite. ✓")
print("\nCondition 1: PASSES ✓")
print("Condition 2: lam*psi = |lam|*(log(u) + log(v)) -> +infinity as x -> infinity ✓")

# Now: sufficient condition
# L = (1/400)*c^2*phi*(1/v^2 + 2/(uv))
# L1 = -c^2*phi/(400)*(38/u^2 - 2/(uv) + 19/v^2)
# L1 + L = -c^2*phi/(400)*(38/u^2 - 2/(uv) + 19/v^2) + c^2*phi/(400)*(1/v^2+2/(uv))
# = c^2*phi/(400)*(-38/u^2 + 4/(uv) - 18/v^2)
# = -c^2*phi/(400)*2*(19/u^2 - 2/(uv) + 9/v^2)
# L1 - L = -c^2*phi/(400)*(38/u^2 - 4/(uv) + 20/v^2)
# L1^2 - L^2 = (L1+L)(L1-L) = [c^2*phi/(400)]^2 * 2*(19/u^2-2/(uv)+9/v^2)*(38/u^2-4/(uv)+20/v^2)

# phi_xt: phi = exp(lam*psi) = (u*v)^{1/20}... wait
# phi = exp(-1/20 * (-log(u) - log(v))) = exp(1/20 * (log(u) + log(v))) = (uv)^{1/20}
# phi_x = d/dx[(uv)^{1/20}] = (1/20)*(uv)^{-19/20} * v * 1 = v/(20*(uv)^{19/20})
# Actually u_x = 1, v_x = 0, so:
# phi_x = (1/20)*(uv)^{-19/20}*v*u_x = (1/20)*v^{1/20}/u^{19/20}... hmm
# Better: phi = u^{1/20}*v^{1/20}
# phi_x = (1/20)*u^{-19/20}*v^{1/20} (since u_x=1, v_x=0)
# phi_t = u^{1/20}*(1/20)*v^{-19/20}*c + (1/20)*u^{-19/20}*c*v^{1/20}
#       = c/(20)*[u^{1/20}/v^{19/20} + v^{1/20}/u^{19/20}]
# phi_xt = d/dx[phi_t] = c/(20)*[d/dx(u^{1/20}/v^{19/20}) + d/dx(v^{1/20}/u^{19/20})]
# Since v_x = 0: d/dx(u^{1/20}/v^{19/20}) = (1/20)*u^{-19/20}/v^{19/20}
# d/dx(v^{1/20}/u^{19/20}) = v^{1/20}*(-19/20)*u^{-39/20}
# phi_xt = c/(20)*[(1/20)*u^{-19/20}/v^{19/20} - (19/20)*v^{1/20}/u^{39/20}]
# = c/400 * [u^{-19/20}/v^{19/20} - 19*v^{1/20}/u^{39/20}]
# = c/400 * (uv)^{1/20} * [1/u - 19/u^2]... this is getting messy.

# Let me just use the verify engine for the full check.
print("\n\nRunning full verification with the verify engine...")
subs3 = {
    alpha: 1,
    s: sp.Rational(-1, 100),
    lam: sp.Rational(-1, 20),
}

results3, report3 = run_verification(psi3, subs3)
print(report3)

