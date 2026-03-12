import sympy as sp

x, t = sp.symbols('x t', nonnegative=True)
c = sp.symbols('c', positive=True)

# Double-log ansatz
psi = -sp.ln(1 + t) - sp.ln(1 + x)

# Parameters
alpha_val = 1
lam_val = sp.Rational(-1, 20)
# s depends on c: s = -1/c^k for some k
# Let's examine the L2 structure

# phi = exp(lam * psi) = ((1+t)(1+x))^(-1/20)
phi = sp.exp(lam_val * psi)
phi_simplified = sp.simplify(phi)
print("phi =", phi_simplified)

# Key derivatives
psi_t = sp.diff(psi, t)
psi_x = sp.diff(psi, x)
psi_tt = sp.diff(psi, t, 2)
psi_xx = sp.diff(psi, x, 2)

# Wave and energy operators on psi
box_psi = psi_tt - c**2 * psi_xx  # = 1/(1+t)^2 - c^2/(1+x)^2
tilde_psi = psi_t**2 - c**2 * psi_x**2  # = 1/(1+t)^2 - c^2/(1+x)^2

print("box_psi =", sp.simplify(box_psi))
print("tilde_psi =", sp.simplify(tilde_psi))

# For this ansatz, box_psi = tilde_psi (the "self-similar" property)
print("box_psi == tilde_psi?", sp.simplify(box_psi - tilde_psi) == 0)

product = phi * tilde_psi
sq_product = sp.diff(product, t, 2) - c**2 * sp.diff(product, x, 2)
sq_product_simplified = sp.simplify(sq_product)
print("\nsquare(phi*tilde_psi) =", sq_product_simplified)

print("\n\nKEY INSIGHT:")
print("The problem allows lambda to depend on c and T.")
print("For the double-log ansatz, the L2 failure threshold scales as ~ C^{N/2} where N=1/|lambda|.")
print("For any finite T, choosing N > 2*log(1+T)/log(C) makes L2 >= 0 on [0,inf)x[0,T].")
print("This means lam = -1/ceil(2*log(1+T)/log(C) + 1) would work!")
print()
print("But wait - in the subs_dict, values can depend on c (a sympy symbol) but")
print("T needs to be handled. Let me check if T is available as a symbol...")

print("\nThe subs_dict maps alpha, s, lam (and optional x0) to concrete values")
print("that may depend on c. T is not a predefined symbol in the verify engine.")
print()
print("So we need a solution that works for ALL T > 0 simultaneously,")
print("or we need to introduce T as a parameter.")
print()
print("Actually wait - re-reading the failed_approaches Round 4 analysis:")
print("'The problem demands conditions hold for arbitrary c > 0, meaning the same psi and s must work for ALL c simultaneously.'")
print("But the problem.tex says: 'psi, s, alpha, lambda could be dependent on c and T'")
print("So they CAN depend on both c and T.")
print()
print("However, the verify engine doesn't seem to support T as a symbol.")
print("The verification is done symbolically with x, t as free variables.")
print("If t ranges over [0, T] and T is a parameter, the engine checks over all t >= 0.")
print()
print("This means: the engine is actually STRICTER than needed.")
print("It checks conditions for ALL t >= 0, not just t in [0, T].")
print("So if we want the engine to pass, we need conditions for all t >= 0.")
print()
print("Given this, the double-log with any finite lambda CANNOT pass the engine.")
print("We need a genuinely different ansatz.")
