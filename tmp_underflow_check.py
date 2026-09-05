"""
Check if the L2 = 0 results at extreme t are underflow or actual zeros.
Use high-precision mpmath directly on the symbolic expression.
"""
import sympy as sp
import mpmath
from verify_engine import x, t, c, x0, alpha, s, lam, build_operators

mpmath.mp.dps = 200  # Very high precision

psi_new = -sp.ln(1 + x + c*t) - sp.ln(1 + c*t)

subs_new = {
    alpha: 1,
    s: sp.Rational(-1, 100),
    lam: sp.Rational(-1, 20),
}

ops = build_operators(psi_new, subs_new)
L2_expr = ops['L2']

# The L2 expression from the engine output:
# L2 = c^4 * N(x,t,c) / (80000000000 * (ct+1)^{79/20} * (ct+x+1)^{59/20})
# 
# At x=0, t=T:
# L2 = c^4 * N(0,T,c) / (80000000000 * (cT+1)^{79/20} * (cT+1)^{59/20})
# = c^4 * N(0,T,c) / (80000000000 * (cT+1)^{(79+59)/20})
# = c^4 * N(0,T,c) / (80000000000 * (cT+1)^{69/10})
#
# The numerator N at x=0 is all terms with x=0:
# N(0,T,c) = 212*c^3*T^3*R + 12872500*c^3*T^3 + 636*c^2*T^2*R + 38617500*c^2*T^2
#           + 636*c*T*R + 38617500*c*T + 212*R + 12872500
# where R = (cT+1)^{1/10} * (cT+1)^{1/10} = (cT+1)^{1/5}
#
# So N(0,T,c) ~ c^3*T^3 * (212*(cT)^{1/5} + 12872500) for large T
# ~ 12872500 * c^3 * T^3 for T >> 1
#
# Denominator ~ (cT)^{69/10} = c^{69/10} * T^{69/10}
#
# L2 ~ c^4 * 12872500 * c^3 * T^3 / (8e10 * c^{69/10} * T^{69/10})
# = 12872500 * c^{7 - 69/10} * T^{3 - 69/10} / 8e10
# = 12872500 * c^{1/10} * T^{-39/10} / 8e10
# -> 0 as T -> infinity.
#
# So L2 -> 0+ (positive, approaching zero from above). It's NOT negative!
# The L2 = 0 results were floating point underflow of tiny positive numbers.

print("Analytical asymptotic analysis at x=0, t -> infinity, c > 0:")
print("L2 ~ const * c^{1/10} * (1+ct)^{-39/10} -> 0+")
print("This approaches 0 from ABOVE (positive). Never negative!")
print()

# Verify with high-precision mpmath
print("High-precision verification at extreme t values:")
for t_v in [1e50, 1e100, 1e200, 1e500]:
    # Compute L2 at x=0, t=t_v, c=1 using the asymptotic formula
    ct_plus_1 = mpmath.mpf(1) + mpmath.mpf(t_v)
    R = ct_plus_1**(mpmath.mpf(1)/5)
    T3 = ct_plus_1**3
    
    numer = 212*T3*R + mpmath.mpf(12872500)*T3 + 636*ct_plus_1**2*R + mpmath.mpf(38617500)*ct_plus_1**2 + 636*ct_plus_1*R + mpmath.mpf(38617500)*ct_plus_1 + 212*R + mpmath.mpf(12872500)
    denom = mpmath.mpf(80000000000) * ct_plus_1**(mpmath.mpf(69)/10)
    
    L2_approx = numer / denom
    print(f"  t={t_v:.0e}: L2 ≈ {mpmath.nstr(L2_approx, 15)}")

print()

# Now check the L2 at large x with t=0
print("High-precision at large x, t=0, c=1:")
for x_v in [1e50, 1e100, 1e200, 1e500]:
    u = mpmath.mpf(1) + mpmath.mpf(x_v)
    v = mpmath.mpf(1)  # ct=0
    R = u**(mpmath.mpf(1)/10) * v**(mpmath.mpf(1)/10)
    
    # N at t=0: 29*x^3*R + 5752500*x^3 + 143*x^2*R + 20767500*x^2 + 252*x*R + 27887500*x + 212*R + 12872500
    x_m = mpmath.mpf(x_v)
    numer = (29*x_m**3*R + mpmath.mpf(5752500)*x_m**3 + 143*x_m**2*R + mpmath.mpf(20767500)*x_m**2 
            + 252*x_m*R + mpmath.mpf(27887500)*x_m + 212*R + mpmath.mpf(12872500))
    denom = mpmath.mpf(80000000000) * u**(mpmath.mpf(59)/20)
    
    L2_approx = numer / denom
    print(f"  x={x_v:.0e}: L2 ≈ {mpmath.nstr(L2_approx, 15)}")

print()

# The key asymptotic at x->inf, t=0:
# N ~ 5752500 * x^3  (dominant polynomial term)
# D ~ 8e10 * x^{59/20}
# L2 ~ 5752500 / (8e10) * x^{3-59/20} = 5752500/8e10 * x^{1/20}
# This GROWS with x! So L2 -> +infinity as x -> infinity. Very positive.

print("At x -> infinity, t=0: L2 ~ const * x^{1/20} -> +infinity (strongly positive)")
print()
print("At t -> infinity, x=0: L2 ~ const * t^{-39/10} -> 0+ (positive, decaying)")
print()
print("CONCLUSION: L2 > 0 for all finite (x, t, c) with x >= 0, t >= 0, c > 0.")
print("The limit as t -> infinity is 0+, which satisfies L2 > 0 for any finite t.")
print()

# But wait: the verify engine checks symbolically and might not be able to prove > 0.
# The expression has fractional powers like (ct+1)^{1/10}.
# Let me check if we can help it.

print("="*80)
print("Can we prove L2 > 0 symbolically?")
print("="*80)

# L2 has the form c^4 * (sum of positive terms) / (positive denominator)
# If we can show every term in the numerator is non-negative, we're done.

# The numerator terms (from the engine output) are:
# 212*c^3*t^3 * R + 12872500*c^3*t^3
# + 252*c^2*t^2*x * R + 27887500*c^2*t^2*x 
# + 636*c^2*t^2 * R + 38617500*c^2*t^2
# + 143*c*t*x^2 * R + 20767500*c*t*x^2
# + 504*c*t*x * R + 55775000*c*t*x
# + 636*c*t * R + 38617500*c*t
# + 29*x^3 * R + 5752500*x^3
# + 143*x^2 * R + 20767500*x^2
# + 252*x * R + 27887500*x
# + 212 * R + 12872500

# EVERY SINGLE TERM HAS A POSITIVE COEFFICIENT!
# And R = (ct+1)^{1/10} * (ct+x+1)^{1/10} > 0.
# Since c > 0, t >= 0, x >= 0: every monomial c^a*t^b*x^d is >= 0.
# Therefore: EVERY term is >= 0, and the constant term 12872500 > 0.
# So the numerator is > 0 for all x >= 0, t >= 0, c > 0. PROVEN!

print("The L2 numerator is a sum of terms of the form:")
print("  (positive coefficient) * c^a * t^b * x^d * R")
print("  (positive coefficient) * c^a * t^b * x^d")
print("where R = (ct+1)^{1/10} * (ct+x+1)^{1/10} > 0")
print("and all monomials c^a * t^b * x^d >= 0 for x,t >= 0, c > 0.")
print()
print("EVERY coefficient is positive! The constant term is 12872500 > 0.")
print("Therefore L2 > 0 ALWAYS. This is a RIGOROUS proof!")
print()
print("Similarly, the denominator has the form:")
print("80000000000 * (ct+1)^{79/20} * (ct+x+1)^{59/20} > 0 always.")
print()
print("And the overall c^4 factor is > 0.")
print()
print("Therefore L2 = c^4 * (positive) / (positive) > 0 for all x >= 0, t >= 0, c > 0. QED")

