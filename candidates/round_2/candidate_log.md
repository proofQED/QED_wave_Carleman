# Round 2 Candidate Log

## Candidate
ψ = -log(1+t) - log(1+x), α = 1, s = -1, λ = -1/20

## Mathematical Reasoning

### Root cause of Round 1 failure
Round 1 used ψ = -log(1+t) - √(x+1) with λ = -1/10. The failure analysis identified that:
- (ψ_x)² = 1/(4(x+1)) decays only as O(1/x) while ψ_xx = 1/(4(x+1)^{3/2}) decays as O(1/x^{3/2})
- The ratio (ψ_x)²/ψ_xx ~ x^{1/2} → ∞, so the λ² gradient term dominates the λ Laplacian term
- This caused condition 1a to fail for large t (the c²(1+t)² growth overwhelmed the spatial terms)
- The failure report recommended p > 1 for ψ_x ~ -x^{-p}

### Why double-log works
Replacing √(x+1) with log(1+x):
- ψ_x = -1/(1+x), so (ψ_x)² = 1/(1+x)² — decays as **O(1/x²)**
- ψ_xx = 1/(1+x)² — also **O(1/x²)**
- The ratio (ψ_x)²/ψ_xx = 1 — **constant**, not growing

Critical structural property: for the double-log ansatz,
  ψ_t² + c²(ψ_x)² = 1/(1+t)² + c²/(1+x)² = ψ_tt + c²ψ_xx

So the gradient-squared equals the "Laplacian". This means L₁/φ = (λ²+λ)·P where P > 0, and all the operator expressions simplify to sums/products of manifestly-signed terms.

### Why λ = -1/20 instead of -1/10
- With λ = -1/10, the L₂ condition fails at extreme (x,t) values due to a dominant -27c⁴ term
- With λ = -1/20, the analogous negative term has coefficient -57/160000 (much smaller) and is dominated by the positive squared term and the 2301/320000 terms
- The constraint for L₁ ≤ 0 requires -1 ≤ λ < 0, so λ = -1/20 is well within range
- Conditions 1a and 1b require |λ| - 2λ² > 0, i.e., |λ| < 1/2, which holds for λ = -1/20

## Expected condition status

### Condition 1a (L - L₁ ≥ 0): **TRUE** (provably)
(L-L₁)/φ = (1/20)/(1+t)² + (9/200)c²/(1+x)² — sum of two positive terms, positive everywhere.

### Condition 1b (-L₁ - L ≥ 0): **TRUE** (provably)
(-L₁-L)/φ = (9/200)/(1+t)² + (1/20)c²/(1+x)² — sum of two positive terms.

### Condition 2 (lim λψ = +∞): **TRUE** (provably)
λψ = (1/20)(log(1+t) + log(1+x)) → +∞ as x → +∞.

### Condition 3 (L₂ ≥ 0): **Likely TRUE** (numerically verified)
Tested over c ∈ {0.5, 1, 2, 5, 10, 20, 50, 100}, x ∈ [0, 10000], t ∈ [0, 10000]. All values non-negative. Minimum ~10⁻¹⁸ (essentially zero at extreme points).

### Sufficient condition ((L₁)²-(L)² ≥ c²(φ_xt)²): **TRUE** (provably)
Both sides factor cleanly:
- LHS/φ² = (a·u + b·v)(b·u + a·v) where a = 9/200, b = 1/20, u = 1/(1+t)², v = c²/(1+x)²
- RHS/φ² = λ⁴·u·v = u·v/160000
- LHS - RHS = ab(u²+v²) + (a²+b²-λ⁴)·uv with all coefficients positive.

## How this differs from Round 1
1. **Changed spatial part**: log(1+x) instead of √(x+1) — faster decay of (ψ_x)²
2. **Reduced |λ|**: 1/20 instead of 1/10 — helps L₂ positivity
3. **Same α=1**: eliminates (α-1) terms, keeping expressions clean
4. **Same s=-1**: standard choice

The key innovation is that the double-log form gives ψ_t² + c²ψ_x² = ψ_tt + c²ψ_xx, which makes all operator expressions decompose into manifestly-signed sums.
