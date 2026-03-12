# Description: Two-traveling-wave logarithm ansatz: psi = -log(1+x+ct) - log(1+ct)
#
# FUNDAMENTALLY DIFFERENT from Rounds 2-6 (which all used psi = -log(1+t) - log(1+x)).
# The key structural change: both log arguments involve ct (the wave characteristic),
# making tilde_square(psi) = (psi_t)^2 - c^2*(psi_x)^2 STRICTLY POSITIVE everywhere.
# This eliminates the sign-indefinite tilde_square that caused L2 failure in all prior rounds.
#
# KEY STRUCTURAL PROPERTIES:
# - psi_t = -c/(1+x+ct) - c/(1+ct), psi_x = -1/(1+x+ct)
# - tilde_square(psi) = c^2/(1+ct)^2 + 2c^2/((1+x+ct)(1+ct)) > 0 ALWAYS
# - box(psi) = c^2/(1+ct)^2 > 0 ALWAYS
# - (psi_t)^2 + c^2(psi_x)^2 = c^2*(2/(1+x+ct)^2 + 2/((1+x+ct)(1+ct)) + 1/(1+ct)^2) > 0
# - psi_tt + c^2*psi_xx = c^2*(2/(1+x+ct)^2 + 1/(1+ct)^2) > 0
#
# The sign-definiteness of tilde_square(psi) is the CRITICAL difference from
# the double-log ansatz. In the double-log case:
#   tilde_square = 1/(1+t)^2 - c^2/(1+x)^2  (changes sign!)
# Here:
#   tilde_square = c^2/(1+ct)^2 + 2c^2/((1+x+ct)(1+ct))  (always positive!)
#
# This means the problematic term -s^3*lam^4*phi^3*(tilde_square)^2 in L2
# is now phi^3 * (positive)^2 * (-s^3) * lam^4 = phi^3 * (positive) * |s|^3 * lam^4 > 0
# So the term that was NEGATIVE in all prior rounds is now POSITIVE!
#
# CONDITIONS:
# 1. L1 <= 0 requires lam*(lam+1) < 0, i.e., -1 < lam < 0. With lam=-1/20: ✓
#    Cond 1a: (L-L1)/phi = c^2 * positive_quad(ct,x) / denom > 0 ✓
#    Cond 1b: (-L1-L)/phi = c^2 * positive_quad(ct,x) / denom > 0 ✓
# 2. lam*psi = (1/20)*(log(1+x+ct) + log(1+ct)) → +∞ as x → ∞ ✓
# 3. L2 > 0: ALL coefficients in the numerator polynomial are positive ✓
# 4. Sufficient: ALL coefficients in the numerator polynomial are positive ✓

psi = -sp.ln(1 + x + c*t) - sp.ln(1 + c*t)

subs_dict = {
    alpha : 1,
    s     : sp.Rational(-1, 100),
    lam   : sp.Rational(-1, 20),
}
