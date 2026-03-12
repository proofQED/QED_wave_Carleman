import sympy as sp
import sys
sys.path.insert(0, '/local/home/cyanz/wave_PINN')
from verify_engine import x, t, c, x0, alpha, s, lam, build_operators, truth_value_from_sign

# BUG CHECK: the build_operators returned L=0, L1=0, L2=0 for double-log with s=-1/c^2
# This seems wrong. Let me check manually.

psi_dlog = -sp.ln(1 + t) - sp.ln(1 + x)

subs1 = {
    alpha: 1,
    s: -1/c**2,
    lam: sp.Rational(-1, 20),
}

print("Testing double-log with s = -1/c^2...")
ops1 = build_operators(psi_dlog, subs1)
print("psi =", ops1['psi'])
print("phi =", ops1['phi'])
print("L =", ops1['L'])
print("L1 =", ops1['L1'])
print("L2 =", ops1['L2'])
print()

# That L=0, L1=0 looks wrong. The double-log with alpha=1 should give nonzero L and L1.
# Let me check: is the issue with how subs works?

# Manual computation:
phi = sp.exp(sp.Rational(-1, 20) * psi_dlog)
print("phi manually =", sp.simplify(phi))
print("phi_tt manually =", sp.simplify(sp.diff(phi, t, 2)))
print("phi_xx manually =", sp.simplify(sp.diff(phi, x, 2)))

L1_manual = sp.diff(phi, t, 2) + c**2 * sp.diff(phi, x, 2)
L1_manual_simplified = sp.simplify(L1_manual)
print("L1 manual =", L1_manual_simplified)
print("L1 manual factored =", sp.factor(L1_manual_simplified))

# The issue might be in the substitution order or simplification
print("\n\nDEBUG: Checking build_operators step by step...")
phi_sym = sp.exp(lam * psi_dlog)
print("phi_sym =", phi_sym)
print("phi_sym.subs(subs1) =", sp.simplify(phi_sym.subs(subs1)))

L1_sym = c**2 * sp.diff(phi_sym, x, 2) + sp.diff(phi_sym, t, 2)
print("L1_sym =", sp.simplify(L1_sym))
print("L1_sym.subs(subs1) =", sp.simplify(L1_sym.subs(subs1)))
print("L1_sym.subs(subs1) expanded =", sp.simplify(sp.expand(L1_sym.subs(subs1))))

# Ah wait - L1 doesn't depend on alpha or s! Only on lam.
# So L1.subs(subs1) should just sub lam=-1/20.
# Let me check what the subs does:
test_subs = L1_sym.subs(lam, sp.Rational(-1, 20))
print("\nL1_sym.subs(lam, -1/20) =", sp.simplify(test_subs))
print("Is nonzero?", sp.simplify(test_subs) != 0)

# Now check with full subs1
test_subs2 = L1_sym.subs(subs1)
print("\nL1_sym.subs(subs1) =", sp.simplify(test_subs2))

# Maybe the issue is that s=-1/c^2 introduces c in a way that confuses the substitution
# Let me try with a concrete constant s
subs2 = {
    alpha: 1,
    s: sp.Rational(-1, 100),
    lam: sp.Rational(-1, 20),
}
print("\n\nTesting with s = -1/100 (constant)...")
ops2 = build_operators(psi_dlog, subs2)
print("L =", sp.factor(ops2['L']))
print("L1 =", sp.factor(ops2['L1']))
print("L2 (first 200 chars) =", str(sp.factor(ops2['L2']))[:200])
