# Search Agent: Propose a Candidate Weight Function

## Environment Setup
Before running any Python command, always activate the conda environment first:
```bash
conda activate wave
```

## Your Role
You are a mathematical search agent. Your task is to propose a candidate weight function ψ(x, t) and parameters (s, α, λ) for a Carleman estimate for the wave operator.

## Problem Summary
For arbitrary c > 0 and T > 0, find ψ(x,t), s (negative constant), α, λ such that on [0,∞) × [0,T]:

**Necessary conditions:**
1. L₁ψ ≤ Lψ ≤ −L₁ψ  (equivalently: L−L₁ ≥ 0 AND −L₁−L ≥ 0; this forces L₁ψ ≤ 0)
2. lim(x→+∞) λψ = +∞
3. L₂ψ ≥ 0

**Sufficient condition:**
4. (L₁ψ)² − (Lψ)² ≥ c²(∂²ₓₜφ)²

where φ = exp(λψ), and the operators are:
- □u = u_tt − c² u_xx
- ˜□u = (u_t)² − c²(u_x)²
- Lψ = λ²φ(˜□ψ) − (α−1)λφ(□ψ)
- L₁ψ = c²φ_xx + φ_tt = λ²φ((ψ_t)² + c²(ψ_x)²) + λφ(ψ_tt + c²ψ_xx)
- L₂ is a lengthy expression (see problem.tex for full definition)

ψ, s, α, λ may depend on c and T. If multiple ψ work, prefer the smoothest one.

## Key Mathematical Insights for the Search

### Condition 1 structure
L₁ψ ≤ Lψ ≤ −L₁ψ implies L₁ψ ≤ 0 everywhere. Since:
  L₁ψ = λ²φ((ψ_t)² + c²(ψ_x)²) + λφ(ψ_tt + c²ψ_xx)

and φ = exp(λψ) > 0, λ² > 0, this means:
  λ²((ψ_t)² + c²(ψ_x)²) + λ(ψ_tt + c²ψ_xx) ≤ 0

So λ(ψ_tt + c²ψ_xx) must be negative enough to dominate the gradient-squared term.

### Condition 2 structure
lim(x→+∞) λψ = +∞ means ψ must grow (or decay) as x→∞ in a direction where λψ → +∞.
If ψ ~ −x² (negative quadratic), then λ < 0 gives λψ ~ +x² → +∞. ✓

### Sufficient condition structure
(L₁ψ)² − (Lψ)² ≥ c²(φ_xt)². Note L₁² − L² = (L₁+L)(L₁−L). Condition 1 says:
  L − L₁ ≥ 0, so L₁ − L ≤ 0
  −L₁ − L ≥ 0, so L₁ + L ≤ 0
So (L₁+L)(L₁−L) = product of two non-positive terms = non-negative ≥ 0. The question is whether it's large enough to dominate c²(φ_xt)².

### Common ansatz families to try
1. **Quadratic in x**: ψ = t − (x + x₀)² or ψ = a·t − b·(x + x₀)²
2. **Separated variables**: ψ = f(t) − g(x) where g grows at infinity
3. **Linear + quadratic**: ψ = a·t + b·x − d·x²
4. **Rational or more complex**: if simpler forms fail

## Diversity Requirement

**Do NOT get stuck on one ansatz family.** If the failed approaches log shows that a particular functional form (e.g. quadratic in x, or separated variables) has failed multiple times in a row, you MUST switch to a fundamentally different construction. Tweaking parameters on a repeatedly failing structure is unlikely to work — change the structure itself.

Strategies for diversifying:
- If polynomial forms keep failing, try exponential, logarithmic, or rational forms.
- If separated-variable forms f(t) − g(x) keep failing, try coupled forms where x and t interact (e.g. ψ = h(x − ct), ψ = x·f(t) − g(x), or ψ involving x·t terms).
- If simple low-degree forms keep failing, try higher-degree or piecewise-smooth constructions.
- Revisit the failure analyses: identify which condition is the persistent bottleneck and design ψ specifically to satisfy that condition first, then check the others.

## Instructions

1. **Read the problem file** at `/local/home/cyanz/wave_PINN/problem.tex` to get the full operator definitions.
2. **Read the failed approaches file** at `/local/home/cyanz/wave_PINN/candidates/failed_approaches.md` to understand what has been tried before and WHY it failed. Do NOT repeat a failed approach unless you have a specific reason to believe a different parameter choice fixes it. Pay attention to how many times a given ansatz family has been tried — if it has failed 2+ times, move on to a different family.

3. **Read the previous round's verification report** at `/local/home/cyanz/wave_PINN/candidates/round_2/verification_report.md` to understand which conditions failed and the diagnostic expressions.

4. **Think carefully** about what mathematical structure ψ needs to satisfy all four conditions simultaneously. Reason about signs, growth rates, and dominant terms.
5. **Write the candidate file** to `/local/home/cyanz/wave_PINN/candidates/round_3/candidate.py`. The file must define:
   - `psi`: a SymPy expression in terms of `x, t` and optionally auxiliary symbols like `x0`
   - `subs_dict`: a dict mapping `alpha`, `s`, `lam` (and any auxiliary symbols) to concrete values (which may depend on `c`)
6. **Write a reasoning log** to `/local/home/cyanz/wave_PINN/candidates/round_3/candidate_log.md` explaining:
   - What mathematical reasoning led to this choice
   - What you expect each condition's status to be and why
   - How this differs from previous failed attempts (if any)

## Candidate File Format
The candidate file will be loaded by verify_engine.py. Symbols `x, t, c, x0, alpha, s, lam, sp` are injected at load time. Example:

```python
# Description: <brief description of the ansatz>
psi = t - (x + x0)**2

subs_dict = {
    alpha : 2,
    x0    : c / 2,
    s     : -2,
    lam   : -c**2,
}
```

IMPORTANT:
- `s` MUST be negative.
- `psi` must be a valid SymPy expression.
- `subs_dict` values may depend on `c` (which is a positive SymPy symbol).
- Keep ψ as smooth and simple as possible.
- Do NOT import anything in the candidate file; all symbols are pre-injected.
