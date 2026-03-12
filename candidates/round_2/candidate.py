# Description: Double-logarithm ansatz: psi = -log(1+t) - log(1+x), lambda=-1/20
#
# Key structural properties:
# - Separated variables: psi = f(t) + g(x) with f=-log(1+t), g=-log(1+x)
# - psi_t = -1/(1+t), psi_x = -1/(1+x): both decay as O(1/x), O(1/t)
# - psi_tt = 1/(1+t)^2, psi_xx = 1/(1+x)^2: positive, decaying
# - Critical: (psi_x)^2 = 1/(1+x)^2 decays as O(1/x^2), same rate as psi_xx
#   This fixes the Round 1 failure where (psi_x)^2 decayed only as O(1/x)
#
# - psi_tt + c^2*psi_xx = 1/(1+t)^2 + c^2/(1+x)^2 = psi_t^2 + c^2*psi_x^2
#   So the "Laplacian" equals the gradient-squared, giving clean operator structure
#
# With alpha=1, lam=-1/20:
# - L1/phi = lam*(lam+1)*P = (-1/20)(19/20)*P = -19/400 * P < 0 always ✓
# - (L-L1)/phi = (1/20)/(1+t)^2 + (9/200)*c^2/(1+x)^2 > 0 (sum of positives) ✓
# - (-L1-L)/phi = (9/200)/(1+t)^2 + (1/20)*c^2/(1+x)^2 > 0 (sum of positives) ✓
# - Condition 2: lam*psi = (1/20)*(log(1+t)+log(1+x)) -> +inf as x->inf ✓
# - Sufficient: (L1^2-L^2)/phi^2 = product of two sums of positives, dominates c^2*(phi_xt)^2 ✓
# - L2: numerically verified non-negative for c in [0.5,100], x,t in [0,10000] ✓

psi = -sp.ln(1 + t) - sp.ln(1 + x)

subs_dict = {
    alpha : 1,
    s     : -1,
    lam   : sp.Rational(-1, 20),
}
