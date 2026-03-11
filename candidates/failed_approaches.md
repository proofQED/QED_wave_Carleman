# Failed Approaches Log

This file accumulates all previously tried candidates and why they failed.
The search agent should read this to avoid repeating dead ends.

---


## Round 1

### Candidate
```python
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
```

### Why it failed
## Failure Analysis

### Why the Engine Reports "unknown" Instead of "True"

The verification engine reports `ALL CONDITIONS PASS: False` only because two conditions have status "unknown" rather than "True". No condition is actually violated — the "unknown" results are an artifact of the SymPy symbolic prover's limitations.

**Root cause:** The symbols `x` and `t` are declared as `sp.symbols('x t', real=True)` in verify_engine.py (line 25). SymPy knows they are real but does NOT know they are non-negative. The expression `c²/(2*(c*t + x + 1)^(3/2))` involves a fractional power of `(c*t + x + 1)`. SymPy cannot determine the sign of `c*t + x + 1` for arbitrary real x, t — it could be negative if x and t are sufficiently negative. Hence SymPy returns `is_nonnegative = None` (unknown).

**Mathematical reality:** On the domain x ∈ [0, ∞), t ∈ [0, T], c > 0, we have:
- ξ = x + ct + 1 ≥ 0 + 0 + 1 = 1 > 0
- Therefore ξ^(3/2) > 0, and all expressions of the form (positive constant)/ξ^k are strictly positive.

Both the numerical sampling (no violations found across the entire grid) and the elementary analysis confirm that **all four conditions hold on the physical domain**.

### What Would Be Needed for Symbolic "True"

To get the engine to report `True` symbolically, one would need to either:
1. Declare `x` and `t` with `nonnegative=True` in verify_engine.py (but we are instructed not to modify it), OR
2. Choose a ψ whose resulting expressions have signs provable by SymPy without domain assumptions — e.g., expressions that are sums of squares, or that factor into manifestly positive terms.

### Assessment

This candidate appears to be a **genuine solution** to the weight construction problem. The characteristic-variable approach (ψ depending on ξ = x + ct) is elegant: it kills both □ψ and ˜□ψ simultaneously, zeroing out L and L₂ exactly, and reducing all conditions to simple sign checks on L₁. The parameter choice λ = −1/2 (satisfying −1 < λ < 0) ensures L₁ < 0, and the shift x₀ = 1 guarantees ξ ≥ 1 > 0 on the domain.

The only "failure" is that the symbolic prover cannot confirm what is mathematically obvious. If the engine were domain-aware, this candidate would pass all conditions with status True.

---

