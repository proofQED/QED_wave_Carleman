# Round 7 Candidate Log

## Candidate
```
ψ = -log(1 + x + ct) - log(1 + ct)
α = 1, s = -1/100, λ = -1/20
```

## Mathematical Reasoning

### Diagnosis of the structural failure in Rounds 2-6

All six prior rounds used the **double-logarithm ansatz** ψ = -log(1+t) - log(1+x), which passed conditions 1, 2, and the sufficient condition but **structurally failed L₂ ≥ 0**. The root cause was:

1. For ψ = -log(1+t) - log(1+x), the "energy form" is:
   □̃ψ = ψ_t² - c²ψ_x² = 1/(1+t)² - c²/(1+x)²
   This **changes sign**: it is positive when (1+x) > c(1+t) and negative when (1+x) < c(1+t).

2. The L₂ operator contains the term -s³λ⁴φ³(□̃ψ)². Since s³ < 0, λ⁴ > 0, φ³ > 0, (□̃ψ)² ≥ 0, this term is always **non-negative**. But more importantly, the divergence terms in L₂ (involving ∂_t(φ³·□̃ψ·ψ_t) + c²∂_x(φ³·□̃ψ·ψ_x)) produce **sign-indefinite** contributions due to the sign changes in □̃ψ.

3. The competition between the O(s) positive terms and the O(s³) sign-indefinite terms created an unavoidable failure at sufficiently large (1+t)(1+x), regardless of parameter choices.

### Key insight: make □̃ψ sign-definite

The structural fix is to choose ψ so that **□̃ψ ≥ 0 everywhere**. If □̃ψ is sign-definite and positive, then:
- All products involving □̃ψ in L₂ have predictable signs
- The divergence terms in L₂ involve derivatives of (positive × positive × negative_grad), which produce controlled signs
- The φ³ factor no longer competes against sign-indefinite polynomial factors

### Construction of the new ansatz

Consider ψ = -log(1 + x + ct) - log(1 + ct). The critical differences from the double-log:

**Derivatives:**
- ψ_t = -c/(1+x+ct) - c/(1+ct)
- ψ_x = -1/(1+x+ct)
- ψ_tt = c²/(1+x+ct)² + c²/(1+ct)²
- ψ_xx = 1/(1+x+ct)²
- ψ_xt = c/(1+x+ct)²

**Wave operator:** □ψ = ψ_tt - c²ψ_xx = c²/(1+ct)² > 0 always

**Energy form:** □̃ψ = ψ_t² - c²ψ_x² = c²/(1+ct)² + 2c²/((1+x+ct)(1+ct))
- This is a **sum of positive terms** — strictly positive for all x ≥ 0, t ≥ 0, c > 0!
- Compare with double-log: □̃ψ = 1/(1+t)² - c²/(1+x)² which changes sign.

**"Gradient energy":** ψ_t² + c²ψ_x² = c²(2/(1+x+ct)² + 2/((1+x+ct)(1+ct)) + 1/(1+ct)²) > 0

**"Laplacian":** ψ_tt + c²ψ_xx = c²(2/(1+x+ct)² + 1/(1+ct)²) > 0

### Why the "two-traveling-wave" structure works

The argument (1+x+ct) in the first log is a traveling wave characteristic: it represents the forward characteristic x + ct of the wave equation. The argument (1+ct) in the second log is a "temporal characteristic" (x = 0 characteristic).

Both arguments are strictly positive and monotonically increasing in both x and t (for c > 0). This ensures that:
- All derivatives of ψ involve only reciprocals of positive, growing functions
- The wave operator □ψ only has positive contributions (from the (1+ct) term; the traveling wave term contributes 0 to □ψ since log(1+x+ct) satisfies □(log(1+x+ct)) = 0 up to sign)
- The energy form □̃ψ only has positive contributions

## Expected Condition Status

### Condition 1: L₁ψ ≤ Lψ ≤ -L₁ψ — **Expected: TRUE**

With α = 1:
- L = λ²φ·□̃ψ (since (α-1) = 0)
- L₁ = λ²φ·P + λφ·Q where P = ψ_t² + c²ψ_x² > 0 and Q = ψ_tt + c²ψ_xx > 0

Condition 1a: (L - L₁)/φ = λ²(□̃ψ - P) - λQ
= λ²(-2c²ψ_x²) - λQ
= λ²·2c²/(1+x+ct)² + |λ|·Q > 0 ✓ (sum of positives)

More precisely: (L - L₁)/φ = c²(29(ct)² + 20(ct)x + 10x² + 58(ct) + 20x + 29) / (200·(1+ct)^{39/20}·(1+x+ct)^{39/20})

This is a positive-definite quadratic form in (ct, x):
- Discriminant of 29u² + 20uv + 10v² (treating ct=u, x=v): Δ = 400 - 4·29·10 = -760 < 0
- Leading coefficient 29 > 0
So the quadratic is positive definite. ✓

Condition 1b: (-L₁ - L)/φ = c²(26(ct)² + 16(ct)x + 9x² + 52(ct) + 16x + 26) / (200·denom)

Discriminant: 256 - 4·26·9 = -680 < 0, leading coefficient 26 > 0. Positive definite. ✓

### Condition 2: lim(x→∞) λψ = +∞ — **Expected: TRUE**

λψ = (1/20)(log(1+x+ct) + log(1+ct)) → +∞ as x → ∞. ✓

### Condition 3: L₂ ≥ 0 — **Expected: TRUE**

The verify engine output shows L₂ = c⁴ · N / D where:
- D = 80000000000·(ct+1)^{79/20}·(ct+x+1)^{59/20} > 0
- N = 212(ct)³R + 12872500(ct)³ + 252(ct)²xR + 27887500(ct)²x + ... + 212R + 12872500

where R = (ct+1)^{1/10}·(ct+x+1)^{1/10} > 0.

**Every single term in N has a positive coefficient.** The 20 terms form a polynomial in (ct, x) with R-weighted and unweighted components, all positive. The constant term is 12872500 > 0.

Since ct ≥ 0, x ≥ 0, R > 0, and all 20 coefficients are positive, N > 0 for all x ≥ 0, t ≥ 0, c > 0. Therefore L₂ > 0 globally. ✓

**This is the key structural difference from Rounds 2-6**, where the L₂ numerator had terms with **negative coefficients** multiplied by R. The sign-definite □̃ψ in this ansatz ensures that all L₂ contributions are positive.

Verified numerically with mpmath at x = 10^{2000}, t = 10^{2000}, c = 10^{2000}: L₂ > 0. ✓

### Sufficient condition: (L₁ψ)² - (Lψ)² ≥ c²(φ_xt)² — **Expected: TRUE**

The expression (L₁² - L² - c²φ_xt²) / φ² = c⁴ · S / (160000·(ct+1)⁴·(ct+x+1)⁴)

where S = 2692(ct)⁴ + 3972(ct)³x + 10768(ct)³ + 3363(ct)²x² + 11916(ct)²x + 16152(ct)² + 1360(ct)x³ + 6726(ct)x² + 11916(ct)x + 10768(ct) + 360x⁴ + 1360x³ + 3363x² + 3972x + 2692

All coefficients are positive. The constant term is 2692 > 0. Therefore S > 0 globally. ✓

## How This Differs from Previous Attempts

| Aspect | Rounds 2-6 (double-log) | Round 7 (two-traveling-wave) |
|--------|------------------------|------------------------------|
| ψ | -log(1+t) - log(1+x) | -log(1+x+ct) - log(1+ct) |
| □̃ψ sign | **Indefinite** (changes sign) | **Positive definite** |
| □ψ sign | Indefinite | Positive (= c²/(1+ct)²) |
| L₂ coefficients | Mixed signs (some negative) | **All positive** |
| L₂ status | Fails at extreme values | **Globally positive** |
| Conditions 1, 2, Sufficient | Pass | Pass |

The fundamental shift is from a **separated-variable** form f(t) + g(x) to a **characteristic-aligned** form f(x+ct) + g(ct), which makes the energy form □̃ψ sign-definite and eliminates the structural sign competition in L₂.
