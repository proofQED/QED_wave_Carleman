# Description: Characteristic logarithmic weight psi = -ln(x + c*t + x0).
# Key insight: Using the characteristic variable xi = x + c*t makes both
# square(psi) = 0 and tilde_square(psi) = 0, which forces L = 0 and L2 = 0.
# Condition 1 reduces to L1 <= 0, which holds for -1 < lambda < 0.
# The sufficient condition L1^2 >= c^2*(phi_xt)^2 holds strictly.

psi = -sp.ln(x + c*t + x0)

subs_dict = {
    alpha : 2,
    x0    : 1,
    s     : -1,
    lam   : sp.Rational(-1, 2),
}
