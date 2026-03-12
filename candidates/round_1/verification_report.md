# Verification Report — Round 1

## Candidate Summary
- psi = -sqrt(x + 1) - log(t + 1)
- alpha = 1
- s = -1
- lambda = -1/10
- Other params: none

## Condition Results

### Necessary Condition 1: L₁ψ ≤ Lψ ≤ −L₁ψ
- Status: **False** (fails for large t)
- Condition 1a (L − L₁ ≥ 0): **False** (fails globally; passes only on bounded domain)
- Condition 1b (−L₁ − L ≥ 0): **True** (provably true for all x ≥ 0, t ≥ 0)
- Symbolic expression (1a): `(L-L1)/φ = [c²(t+1)²(5 - √(x+1)) + 20(x+1)^(3/2)] / [200(t+1)²(x+1)^(3/2)]`
- Symbolic expression (1b): `(-L1-L)/φ = [5c²(t+1)² + 16(x+1)^(3/2)] / [200(t+1)²(x+1)^(3/2)]`
- Numerical sampling (engine range x∈[0,50], t∈[0,10]):
  - 1a: likely_true, min = 0.00157, max = 0.204
  - 1b: likely_true, min = 0.00144, max = 0.199
- **Extended numerical sampling** (x∈[0,200], t∈[0,100]):
  - 1a **FAILS** for large t and x > 24
  - 1b: still passes everywhere
- Diagnosis:

  **Condition 1b** is provably true: the numerator `5c²(t+1)² + 16(x+1)^(3/2)` is a sum of two strictly positive terms.

  **Condition 1a** fails globally. The numerator factors as:
  ```
  N = c²(1+t)²(5 - √(x+1)) + 20(x+1)^(3/2)
  ```
  - For x ≤ 24 (i.e., √(x+1) ≤ 5): both terms are non-negative, so N > 0. ✓
  - For x > 24 (i.e., √(x+1) > 5): the first term becomes negative and grows as t². The second term is fixed (independent of t). So for any fixed x > 24, there exists a critical time t* beyond which N < 0.

  Setting N = 0 and solving: `(1+t*)² = 20(x+1)^(3/2) / [c²(√(x+1) - 5)]`. With u = √(x+1), the function f(u) = 20u³/(u-5) has minimum value 3375 at u = 15/2. Therefore condition 1a fails when `c²(1+t)² > 3375`, i.e., `c(1+t) > 15√15 ≈ 58.09`.

  Concrete failure thresholds:
  | c   | Critical t* (x=50) | Critical t* (x=100) | Critical t* (asymptotic) |
  |-----|--------------------|---------------------|--------------------------|
  | 0.5 | 115.6              | 125.8               | 115.2                    |
  | 1.0 | 57.3               | 62.4                | 57.1                     |
  | 2.0 | 28.2               | 30.7                | 28.0                     |

  The verify engine's sampling range (t ∈ [0, 10]) misses this failure entirely.

### Necessary Condition 2: lim(x→+∞) λψ = +∞
- Status: **True** (symbolically proven)
- λψ = √(x+1)/10 + log(t+1)/10
- Limit value: +∞
- Diagnosis: Since λ = -1/10 and ψ = -log(1+t) - √(x+1), we get λψ = (1/10)(log(1+t) + √(x+1)), which grows without bound as x → ∞ due to the √(x+1)/10 term. SymPy confirms this symbolically.

### Necessary Condition 3: L₂ψ ≥ 0
- Status: **False** (fails for large t)
- Symbolic expression: Too complex to display concisely (see engine output); involves products of c⁴, exponentials, and powers of (x+1) and (t+1).
- Numerical sampling (engine range x∈[0,50], t∈[0,10]):
  - likely_true, min = 3.91e-6, max = 0.0801
- **Extended numerical sampling** (x∈[0,200], t∈[0,100]):
  - **FAILS** for t ≥ 50 (c=1), with L₂ going negative in the region x ∈ [14, 52] approximately.
  - Example: c=1, t=100, x≈20: L₂ ≈ -8.4e-8
- Diagnosis: L₂ψ is positive on the engine's default sampling grid but becomes slightly negative at large t. The negative values are very small (order 10⁻⁸), suggesting the candidate is close to satisfying this condition but not quite. The failure region is roughly x ∈ [14, 52] for t ≥ 50 with c=1. The issue is that L₂ contains terms proportional to high powers of (1+t) in the denominator (like (1+t)^{39/10}) but also products of c⁴(1+t)⁴ in the numerator. For large t, certain negative cross-terms involving c² and x² grow faster than the positive terms.

### Sufficient Condition: (L₁ψ)² − (Lψ)² ≥ c²(φ_xt)²
- Status: **False** (fails for large t)
- Symbolic expression: `suff/φ² = [-5c⁴(t+1)⁴√(x+1) + 25c⁴(t+1)⁴ - 17c²(t+1)²x² + 180c²(t+1)²x√(x+1) - 34c²(t+1)²x + 180c²(t+1)²√(x+1) - 17c²(t+1)² + 320(x+1)³] / [40000(t+1)⁴(x+1)³]`
- Numerical sampling (engine range x∈[0,50], t∈[0,10]):
  - likely_true, min = 2.27e-6, max = 0.0395
- **Extended numerical sampling:**
  - c=1: PASSES for t ≤ 50, FAILS at t=70 (min ≈ -8.9e-9 at x≈50)
  - c=2: PASSES for t ≤ 10, FAILS at t=30 (min ≈ -5.8e-8 at x≈53)
- Diagnosis: The leading term for large t is `c⁴(t+1)⁴(25 - 5√(x+1))` which is negative for x > 24. This causes the expression to diverge to -∞ as t → ∞ for any fixed x > 24, analogous to the condition 1a failure. The failure threshold is at similar t values. The 320(x+1)³ term (independent of t) cannot compensate for arbitrarily large t.

## Overall Summary
- Necessary condition 1: **False** (1a fails for large t; 1b is True)
- Necessary condition 2: **True**
- Necessary condition 3: **False** (fails for large t, though violations are small ~10⁻⁸)
- All necessary conditions: **False**
- Sufficient condition: **False** (fails for large t)
- **ALL CONDITIONS PASS: False**

## Failure Analysis

### Root Cause: Unbounded growth of (1+t)² terms relative to spatial terms

All three failing conditions share the same structural weakness: the candidate ψ = -log(1+t) - √(x+1) produces operators where certain terms grow as powers of (1+t)² or (1+t)⁴ in the numerator, while the compensating positive spatial terms (like (x+1)^(3/2)) are independent of t. For any fixed x > 24, increasing t eventually overwhelms the spatial terms.

**Specifically:**
1. **Condition 1a** numerator = c²(1+t)²(5 - √(x+1)) + 20(x+1)^(3/2). The first term is O(t²) and negative for x > 24; the second term is O(1) in t. So the condition fails for t > O(1/c).

2. **Condition 1b** works because both terms in its numerator are positive — this is the key asymmetry. The (1+t)² growth in condition 1b is in a *positive* coefficient (5c²(1+t)²), whereas in condition 1a it multiplies a coefficient that changes sign.

3. **Conditions 3 and sufficient** inherit the same problem through the operators L and L₁ whose difference involves condition-1a-type expressions raised to higher powers.

### Why the engine reported "unknown" instead of "False"

The verify engine:
- Uses SymPy's symbolic sign-checking, which returned "unknown" because x, t are declared as `real=True` (not `nonnegative=True`), and the expressions involve √(x+1) which SymPy cannot reason about for arbitrary real x.
- Falls back to numerical sampling on x ∈ [0, 50], t ∈ [0, 10], c ∈ {0.5, 1, 2}. This range is too small to detect failures that occur at t > 28 (for c=2) or t > 57 (for c=1).

### What the next candidate needs

To fix condition 1a, the candidate must ensure that the expression `(L - L₁)/φ` does not have terms that grow with t while being negative for large x. Two strategies:

1. **Make ψ_x decay faster.** The problematic term is `-2c²λ²(ψ_x)²` in `(L-L₁)/φ`. With ψ_x = -1/(2√(x+1)), we get (ψ_x)² = 1/(4(x+1)), which decays only as O(1/x). If ψ_x decayed faster (e.g., exponentially), the negative contribution would be negligible.

2. **Make the "Laplacian" ψ_tt + c²ψ_xx grow with t.** Currently ψ_tt = 1/(1+t)² which *decays* with t. If instead ψ_tt grew or stayed constant, it could compensate the growing negative terms. However, ψ_tt > 0 requires concavity which is hard to maintain with growing second derivatives.

3. **Use a separable form ψ(x,t) = f(x) + g(t) where both f and g are chosen so that the cross-terms in the operators maintain consistent signs.** The current failure arises because the x-dependent sign change at x=24 (where √(x+1) = 5 = 1/(2|λ|)) interacts with t-growth. Choosing |λ| even smaller would push this threshold to larger x, but would not eliminate the asymptotic failure.

4. **Consider ψ forms where ψ_x is bounded by a function of t that decays appropriately.** For instance, ψ = -log(1+t) - log(1+x) would give ψ_x = -1/(1+x) with (ψ_x)² = 1/(1+x)² decaying as O(1/x²), and ψ_xx = 1/(1+x)² > 0. But one must check that condition 2 (λψ → +∞) still holds.

5. **Most promising direction:** The fundamental issue is that (ψ_x)² doesn't decay fast enough relative to ψ_xx. For ψ_x ~ -x^(-p), we have (ψ_x)² ~ x^(-2p) and ψ_xx ~ x^(-p-1). The ratio (ψ_x)²/ψ_xx ~ x^(-p+1). For this ratio to → 0 as x → ∞ (so that the λ² gradient term doesn't dominate the λ Laplacian term), we need p > 1. The current candidate has p = 1/2 (from √(x+1)), so p < 1, which is insufficient. **Try p > 1**, e.g., ψ involving -(x+1)^q for q < 1/2, or -log(x+1), which gives p = 1 (borderline).
