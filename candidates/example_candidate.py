"""
Example candidate — the original test choice from verify.py.

This file demonstrates the candidate interface:
  - Define `psi` as a SymPy expression in (x, t) and optionally auxiliary symbols.
  - Define `subs_dict` mapping auxiliary symbols + (alpha, s, lam) to concrete values.

Symbols x, t, c, x0, alpha, s, lam are injected by verify_engine.py at load time.
"""

# psi(x, t) with auxiliary parameter x0
psi = t - (x + x0)**2

subs_dict = {
    alpha : 2,
    x0    : c / 2,
    s     : -2,
    lam   : -c**2,
}
