# Verification Report — Round 7

## Candidate Summary
- psi = -log(1 + x + ct) - log(1 + ct)
- alpha = 1
- s = -1/100
- lambda = -1/20
- Other params: none

## Condition Results

### Necessary Condition 1: L₁ψ ≤ Lψ ≤ −L₁ψ
- Status: **True** (proved analytically; engine returned "unknown" due to sympy limitations)
- Condition 1a (L − L₁ ≥ 0): **True**
- Condition 1b (−L₁ − L ≥ 0): **True**
- Symbolic expression (1a): c²·(29(ct)² + 20(ct)x + 10x² + 58(ct) + 20x + 29) / (200·(ct+1)^(39/20)·(ct+x+1)^(39/20))
- Symbolic expression (1b): c²·(26(ct)² + 16(ct)x + 9x² + 52(ct) + 16x + 26) / (200·(ct+1)^(39/20)·(ct+x+1)^(39/20))
- Numerical sampling: 1a: min = 4.74×10⁻⁴ > 0 (likely_true); 1b: min = 4.17×10⁻⁴ > 0 (likely_true)
- Diagnosis: Both conditions are proved by showing the numerators are positive-definite quadratic forms on the domain u = ct ≥ 0, v = x ≥ 0.

  **Proof for 1a:** The numerator is Q₁(u,v) = 29u² + 20uv + 10v² + 58u + 20v + 29. The quadratic form matrix M₁ = [[29, 10], [10, 10]] has determinant 190 > 0 and leading entry 29 > 0, so it is positive definite. The unconstrained global minimum is at (u,v) = (-1, 0) with Q₁ = 0, which lies outside the domain u ≥ 0. On the boundary u = 0: Q₁ = 10v² + 20v + 29 = 10(v+1)² + 19 > 0. On the boundary v = 0: Q₁ = 29u² + 58u + 29 = 29(u+1)² > 0. At the corner (0,0): Q₁ = 29, with ∂Q₁/∂u = 58 > 0 and ∂Q₁/∂v = 20 > 0, so Q₁ is strictly increasing in both directions. Therefore Q₁ > 0 for all u ≥ 0, v ≥ 0. The denominator (ct+1)^(39/20)·(ct+x+1)^(39/20) > 0 and c² > 0, so condition 1a holds.

  **Proof for 1b:** The numerator is Q₂(u,v) = 26u² + 16uv + 9v² + 52u + 16v + 26. The quadratic form matrix M₂ = [[26, 8], [8, 9]] has determinant 170 > 0 and leading entry 26 > 0, so it is positive definite. The unconstrained global minimum is at (u,v) = (-1, 0) with Q₂ = 0, outside the domain. On the boundary u = 0: Q₂ = 9v² + 16v + 26 > 0 (discriminant 256 - 936 < 0). On the boundary v = 0: Q₂ = 26u² + 52u + 26 = 26(u+1)² > 0. At (0,0): Q₂ = 26 with ∂Q₂/∂u = 52 > 0, ∂Q₂/∂v = 16 > 0. Therefore Q₂ > 0 for all u ≥ 0, v ≥ 0. ∎

### Necessary Condition 2: lim(x→+∞) λψ = +∞
- Status: **True** (confirmed symbolically by engine)
- λψ = (1/20)·(log(1 + x + ct) + log(1 + ct))
- Limit value: +∞
- Diagnosis: Since λ = -1/20 < 0 and ψ = -log(1+x+ct) - log(1+ct) → -∞ as x → ∞, we get λψ = (1/20)·log(1+x+ct) + (1/20)·log(1+ct) → +∞. The log(1+x+ct) term diverges while the log(1+ct) term is a positive constant in x. ∎

### Necessary Condition 3: L₂ψ ≥ 0
- Status: **True** (proved analytically; engine returned "unknown" due to sympy limitations)
- Symbolic expression: L₂ = c⁴·N / (80000000000·(ct+1)^(79/20)·(ct+x+1)^(59/20)), where N is detailed below
- Numerical sampling: min = 4.97×10⁻⁹ > 0 (likely_true); verified with mpmath at (ct, x) = (10²⁰⁰⁰, 10²⁰⁰⁰): L₂ > 0
- Diagnosis: The denominator is manifestly positive. The numerator N is:

  N = 212u³R + 12872500u³ + 252u²vR + 27887500u²v + 636u²R + 38617500u²
    + 143uv²R + 20767500uv² + 504uvR + 55775000uv + 636uR + 38617500u
    + 29v³R + 5752500v³ + 143v²R + 20767500v² + 252vR + 27887500v + 212R + 12872500

  where u = ct ≥ 0, v = x ≥ 0, and R = (ct+1)^(1/10)·(ct+x+1)^(1/10) > 0.

  **Proof:** Every term in N is a product of: (1) a positive integer coefficient, (2) a non-negative monomial u^a·v^b with a,b ≥ 0, and (3) either R > 0 or 1. Since u ≥ 0 and v ≥ 0, every monomial u^a·v^b ≥ 0. The constant term 212R + 12872500 ≥ 212·1 + 12872500 > 0 (since R ≥ 1 when ct ≥ 0, x ≥ 0). Therefore N is a sum of non-negative terms with at least one strictly positive term, hence N > 0 for all u ≥ 0, v ≥ 0, c > 0.

  Confirmed numerically with mpmath (50+ digits) at extreme points including (ct, x) = (10²⁰⁰⁰, 10²⁰⁰⁰). ∎

### Sufficient Condition: (L₁ψ)² − (Lψ)² ≥ c²(φ_xt)²
- Status: **True** (proved analytically; engine returned "unknown" due to sympy limitations)
- Symbolic expression: (L₁² − L² − c²φ_xt²) / φ² = c⁴·S / (160000·(ct+1)⁴·(ct+x+1)⁴), where:
  S = 2692u⁴ + 3972u³v + 10768u³ + 3363u²v² + 11916u²v + 16152u²
    + 1360uv³ + 6726uv² + 11916uv + 10768u + 360v⁴ + 1360v³ + 3363v² + 3972v + 2692
  with u = ct, v = x.
- Numerical sampling: min = 1.98×10⁻⁷ > 0 (likely_true); verified with mpmath at (ct, x) = (10²⁰⁰⁰, 10²⁰⁰⁰): S > 0
- Diagnosis:

  **Proof:** The denominator 160000·(ct+1)⁴·(ct+x+1)⁴ > 0, φ² > 0, and c⁴ > 0. We need to show S > 0 for u ≥ 0, v ≥ 0.

  All 15 coefficients in S are strictly positive: {2692, 3972, 10768, 3363, 11916, 16152, 1360, 6726, 11916, 10768, 360, 1360, 3363, 3972, 2692}. Since u ≥ 0 and v ≥ 0, every monomial u^a·v^b ≥ 0. The constant term is 2692 > 0. Therefore S is a sum of non-negative terms with at least one strictly positive term, so S > 0 for all u ≥ 0, v ≥ 0.

  Confirmed numerically with mpmath at all extreme test points. ∎

## Overall Summary
- Necessary condition 1: **True** (proved: positive-definite quadratic forms)
- Necessary condition 2: **True** (proved: symbolic limit)
- Necessary condition 3: **True** (proved: all coefficients positive with non-negative monomials)
- All necessary conditions: **True**
- Sufficient condition: **True** (proved: all coefficients positive with non-negative monomials)
- **ALL CONDITIONS PASS: True**

## Failure Analysis

No conditions failed. All four conditions pass with rigorous analytical proofs.

**Why the engine reported "unknown":** The sympy `is_nonnegative` / `is_positive` attribute checks cannot determine the sign of expressions involving fractional powers like (ct+1)^(39/20). The engine correctly fell back to numerical sampling, which showed all conditions are "likely_true" with strictly positive minimum values and no violations found. Our independent analytical verification above confirms these results rigorously.

**Key structural properties that make this candidate work:**

1. **Sign-definite □̃ψ:** For ψ = -log(1+x+ct) - log(1+ct), we have □̃ψ = c²·(3(ct+1) + x) / ((ct+1)²·(ct+x+1)), which is a ratio of strictly positive quantities. This is the fundamental structural improvement over the double-log ansatz ψ = -log(1+t) - log(1+x), where □̃ψ = 1/(1+t)² - c²/(1+x)² changes sign.

2. **Characteristic-aligned construction:** Both log arguments involve the wave speed c through the combinations (x+ct) and (ct), which are forward characteristics of the wave equation. This ensures that the wave operator □ψ = c²/(1+ct)² > 0 (the traveling wave part log(1+x+ct) satisfies the homogeneous wave equation exactly, so □ψ comes only from the second term).

3. **All-positive numerator coefficients:** Because □̃ψ > 0 and □ψ > 0, the problematic sign-indefinite terms that plagued Rounds 2-6 are eliminated. Every coefficient in the L₂ numerator and the sufficient condition numerator is strictly positive, making the positivity proofs trivial.

4. **Parameter choice λ = -1/20:** With -1 < λ < 0, we have λ(λ+1) = (-1/20)(19/20) < 0, which ensures L₁ψ < 0 (needed for condition 1). The small magnitude |λ| = 1/20 keeps all polynomial coefficients positive.
