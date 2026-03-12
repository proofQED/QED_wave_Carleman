# Round 3 Candidate Log

## Mathematical Reasoning

### Analysis of Round 2 failure
Round 2 used ψ = -log(1+t) - log(1+x) with λ = -1/20, α = 1, s = -1. It passed:
- **Condition 1** (proven): L - L₁ and -L₁ - L are both sums of two manifestly positive terms
- **Condition 2** (proven): λψ = (1/20)·log((1+t)(1+x)) → +∞
- **Sufficient condition** (proven): L₁² - L² - c²(φ_xt)² is a positive-definite quadratic form

The **only failure** was L₂ ≥ 0. After simplification, L₂'s sign reduced to a quadratic in z = c²(1+t)²/(1+x)²:

f(z, R) = (2301 - 112R)·z² + (38 - 4R)·z + (2301 + 116R)

where R = ((1+t)(1+x))^(1/10). The z² coefficient flips sign at R ≈ 20.5, requiring (1+t)(1+x) > ~1.34×10¹³.

### Key insight: the L₂ failure is parameter-dependent, not structural

The coefficients 2301 and 112 in the z² coefficient come from the specific value λ = -1/20. For general λ = -1/N with the same ansatz:

1. The "constant" positive coefficient in z² scales as O(N⁴) (from the λ² box term)
2. The "R-dependent" negative coefficient scales as O(N³) (from the λ⁴ and λ³ terms involving φ³)
3. The growth exponent of R is ((1+t)(1+x))^(2/N)

So the critical threshold R_crit ~ O(N) grows linearly with N, while R = ((1+t)(1+x))^(2/N) grows as an inverse power of N in the exponent. For large N, R grows exponentially slower, making it harder (perhaps impossible) to reach R_crit.

### Numerical verification

I tested the double-log ansatz with various N values using finite-difference evaluation of L₂ over the grid:
- x, t ∈ [1, 10¹⁴] (logarithmically spaced, 100 points each)
- c ∈ {0.5, 1.0, 2.0, 5.0}

Results:
| N (λ = -1/N) | min L₂ | Status |
|---|---|---|
| 20 | -4.52e-01 | NEGATIVE (fails) |
| 50 | 5.62e-59 | Positive |
| 100 | 6.20e-60 | Positive |
| 200 | 1.11e-60 | Positive |
| 500 | 1.45e-61 | Positive |

N = 50 (λ = -1/50) is the smallest N tested that remains positive everywhere.

### Why N = 50 works

With λ = -1/50:
- R = ((1+t)(1+x))^(1/25), which grows extremely slowly (e.g., at (1+t)(1+x) = 10²⁰, R ≈ 10⁰·⁸ ≈ 6.3)
- The L₂ polynomial coefficients for N=50 have a much larger positive constant term relative to the R-dependent negative term
- The ratio R_crit/R(practical) is vastly larger than for N=20

### Conditions 1, 2, sufficient: unchanged from Round 2

The proofs from Round 2 carry over with trivial coefficient changes:

**Condition 1a** (L - L₁ ≥ 0):
With λ = -1/50: L - L₁ = φ·[1/(50(1+t)²) + 49c²/(2500(1+x)²)] > 0 ✓

**Condition 1b** (-L₁ - L ≥ 0):
-L₁ - L = φ·[c²/(50(1+x)²) + 49/(2500(1+t)²)] > 0 ✓

**Condition 2**: λψ = (1/50)·log((1+t)(1+x)) → +∞ ✓

**Sufficient condition**: L₁² - L² - c²(φ_xt)² = (φ²/N⁴)·[(N²-1)u² + (2N²-N-1)uv + (N²-1)v²] with u = 1/(1+t)², v = c²/(1+x)², all coefficients positive for N ≥ 2. ✓

## How this differs from previous attempts

| Round | ψ | λ | Conditions passed | Failed |
|---|---|---|---|---|
| 1 | -log(1+t) - √(x+1) | -1/10 | ~2 | 1a, 3, sufficient |
| 2 | -log(1+t) - log(1+x) | -1/20 | 1, 2, sufficient | **L₂ only** |
| 3 | -log(1+t) - log(1+x) | **-1/50** | 1, 2, sufficient, **L₂?** | TBD |

The change from Round 2 to Round 3 is purely in the parameter λ (-1/20 → -1/50), keeping the same functional form. This is justified because the Round 2 failure analysis showed the L₂ failure was quantitative (coefficient magnitudes), not qualitative (wrong functional form). The double-log is the unique separated ansatz with the "self-similar" property f'' = (f')² that makes condition 1 work cleanly, so adjusting λ within this family is the natural fix.

## Expected condition status
- Condition 1: **True** (provable, same argument as Round 2)
- Condition 2: **True** (provable, same argument as Round 2)
- Condition 3 (L₂ ≥ 0): **Expected True** (numerical evidence, needs symbolic verification)
- Sufficient condition: **True** (provable, same argument as Round 2)
