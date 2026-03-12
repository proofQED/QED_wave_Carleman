# Description: Double-logarithm ansatz with small |s| to fix L₂
#
# SAME functional form as Rounds 2-3: ψ = -log(1+t) - log(1+x)
# but with s = -1/100 (instead of s = -1).
#
# KEY INSIGHT: The L₂ operator decomposes as:
#   L₂ = Term_B + Term_D + Term_E
# where (with α=1):
#   Term_B = -(s/2)λ²·□(φψ̃)     ∝ |s|    (POSITIVE, since □(φψ̃) > 0 for double-log)
#   Term_D = -s³λ⁴φ³(ψ̃)²        ∝ |s|³   (POSITIVE)
#   Term_E = s³λ³·(div terms)     ∝ |s|³   (MIXED sign, contains growing φ³ factor)
#
# For |s| << 1, the O(|s|) positive Term_B dominates the O(|s|³) mixed Term_E.
# The failure scale moves to R_crit ~ O(1/|s|²), which with |s| = 1/100 gives
# R_crit ~ 10⁴, meaning (1+t)(1+x) ~ 10^(10⁴·N/2), astronomically large.
#
# Crucially, on the actual domain [0,∞)×[0,T] with fixed T and c:
# - When z = c²(1+t)²/(1+x)² ≥ 1: R is bounded by (c(1+T)²)^(1/10), so L₂ > 0
# - When z < 1: the large-R asymptotics give L₂ ~ (29 - 28z² - z)R > 0 since z < 1
# So L₂ > 0 everywhere on the problem domain for ANY fixed c, T > 0.
#
# Conditions 1, 2, and the sufficient condition are identical to Rounds 2-3
# (they don't depend on s at all), and were proven true there.

psi = -sp.ln(1 + t) - sp.ln(1 + x)

subs_dict = {
    alpha : 1,
    s     : sp.Rational(-1, 100),
    lam   : sp.Rational(-1, 20),
}
