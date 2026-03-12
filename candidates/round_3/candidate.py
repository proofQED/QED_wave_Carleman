# Description: Double-logarithm ansatz with smaller |lambda|=-1/50 to fix L2
#
# This is the SAME functional form as Round 2 (psi = -log(1+t) - log(1+x))
# but with lambda = -1/50 instead of -1/20.
#
# Round 2 passed conditions 1, 2, and the sufficient condition.
# The ONLY failure was L2 >= 0, which failed because the z^2 coefficient
# (2301 - 112*R) in the L2 quadratic flipped sign at R = ((1+t)(1+x))^(1/10) ~ 20.5.
#
# With lambda = -1/50:
# - R = ((1+t)(1+x))^(2/50) = ((1+t)(1+x))^(1/25), which grows much slower
# - The polynomial coefficients in L2 change: the constant positive term scales as
#   ~N^4 while the R-dependent negative term scales as ~N^3, making the ratio
#   ~N, so the critical R_crit grows with N.
# - For N=50, numerical testing over x,t in [1, 10^14] and c in {0.5, 1, 2, 5}
#   found L2 strictly positive everywhere.
#
# Key properties (identical structure to Round 2):
# - psi_t = -1/(1+t), psi_x = -1/(1+x)
# - (psi_t)^2 = psi_tt, (psi_x)^2 = psi_xx  ("self-similar" property)
# - With alpha=1: L1/phi = lam(lam+1)*P where P = (1/(1+t)^2 + c^2/(1+x)^2) > 0
#   and lam(lam+1) = (-1/50)(49/50) = -49/2500 < 0, so L1 < 0. Condition 1 satisfied.
# - Condition 2: lam*psi = (1/50)*log((1+t)(1+x)) -> +inf
# - Sufficient: (L1^2 - L^2)/phi^2 = positive polynomial in 1/(1+t)^2 and c^2/(1+x)^2

psi = -sp.ln(1 + t) - sp.ln(1 + x)

subs_dict = {
    alpha : 1,
    s     : -1,
    lam   : sp.Rational(-1, 50),
}
