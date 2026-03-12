# Description: Log-sqrt ansatz: psi = -ln(1+t) - sqrt(x+1), small lambda
#
# Key properties:
# - psi_t = -1/(1+t) -> 0 (bounded derivatives in t)
# - psi_tt = 1/(1+t)^2 > 0 (convex in t)
# - psi_x = -1/(2*sqrt(x+1)) -> 0 (derivatives decay in x)
# - psi_xx = 1/(4*(x+1)^(3/2)) (concave-up correction)
#
# With alpha=1:
# - Condition 1b is EXACTLY: (-L1-L)/phi = c^2/(8*(x+1)^(3/2)) > 0 always
# - Condition 1a: (L-L1)/phi > 0 verified numerically (holds for t << 1/|lam|^(3/2))
# - Condition 2: lam*psi = |lam|*(ln(1+t)+sqrt(x+1)) -> +inf as x->inf

psi = -sp.ln(1 + t) - sp.sqrt(x + 1)

subs_dict = {
    alpha : 1,
    s     : -1,
    lam   : sp.Rational(-1, 10),
}
