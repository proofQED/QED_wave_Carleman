import sympy as sp
import mpmath
import sys
sys.path.insert(0, '/local/home/cyanz/wave_PINN')
from verify_engine import x, t, c, x0, alpha, s, lam, build_operators, truth_value_from_sign, run_verification

mpmath.mp.dps = 50

print("="*80)
print("ANALYSIS: What makes L2 fail for the double-log?")
print("="*80)

# For psi = -log(T) - log(X) with T=1+t, X=1+x, lam=-1/N, alpha=1:
# The L2 numerator (in terms of T, X, c) after extracting positive factors is:
# L2_num = 2301*c^8*T^4 + 38*c^6*T^2*X^2 + 2301*c^4*X^4   [O(s) positive terms]
#        - 112*c^4*T^4*R - 4*c^2*T^2*X^2*R + 116*X^4*R      [O(s^3) mixed terms]
# where R = (TX)^(1/10) for N=20, s=-1/c^2

# The negative terms: -112*c^4*T^4*R and -4*c^2*T^2*X^2*R
# At x=0, T large: R = T^(1/10), and the negative term is -112*c^4*T^(4+1/10)
# The positive term from O(s): 2301*c^8*T^4
# Ratio: 2301*c^8*T^4 / (112*c^4*T^(4+1/10)) = 2301*c^4 / (112*T^(1/10))
# This ratio -> 0 as T -> infinity. So L2 ALWAYS becomes negative for large T.
#
# KEY: The failure at large t is INDEPENDENT of s.
# The O(s) terms scale as T^4 while the O(s^3) terms with R scale as T^(4+2/N).
# Making s depend on c changes the c-dependence but NOT the t-dependence!

print("The double-log ansatz has L2 ~ A*T^4 - B*T^(4+2/N) for large t.")
print("This always becomes negative for T large enough, regardless of s.")
print("The parameter s only affects the c-dependence of A and B, not their t-powers.")
print()

print("="*80)
print("EXPLORING: Can we make L2 > 0 strictly with a traveling wave perturbation?")
print("="*80)

# Key insight from the analysis:
# 1. Pure traveling wave psi = -log(1+x+ct): L2 = 0 (fails strict inequality)
# 2. Double-log psi = -log(1+t) - log(1+x): L2 < 0 for large t (fails)
# 3. Perturbed traveling wave: psi = -log(1+x+ct) + epsilon * f(x,t)
#    where f is chosen to make L2 > 0

# The idea: the traveling wave makes ALL L2 terms vanish because box(psi) = tilde(psi) = 0.
# A perturbation breaks this, introducing small O(epsilon) contributions.
# The question: can the perturbation be chosen so that L2 > 0?

# For a small perturbation psi = -log(1+x+ct) + eps*g:
# box(psi) = eps*box(g) + O(eps^2)
# tilde(psi) = 2*(-c/(1+x+ct))*eps*g_t + 2*(c^2/(1+x+ct))*eps*g_x + ... wait
# tilde(psi) = (psi_t)^2 - c^2*(psi_x)^2
#            = (-c/(u) + eps*g_t)^2 - c^2*(-1/u + eps*g_x)^2  where u = 1+x+ct
#            = c^2/u^2 - 2c*eps*g_t/u + eps^2*(g_t)^2 - c^2/u^2 + 2c^2*eps*g_x/u - c^2*eps^2*(g_x)^2
#            = eps*(2c^2*g_x/u - 2c*g_t/u) + O(eps^2)
#            = (2c*eps/u)*(c*g_x - g_t) + O(eps^2)

# So tilde(psi) is O(eps) and box(psi) is O(eps).
# In L2, the O(s) term involves square(phi*tilde_psi) which is O(eps) (derivatives of O(eps) terms)
# The O(s^3) terms involve phi^3 * (tilde_psi)^2 which is O(eps^2)
# And phi^3 * tilde_psi * box_psi which is O(eps^2)
# So L2 = O(eps) * (something from O(s) terms) + O(eps^2) * (something from O(s^3) terms)
# For small eps, the O(eps) term dominates!

# The O(eps) term: -(s/2)*lam^2*square(phi*tilde_psi)
# = -(s/2)*lam^2*square(phi * 2c*eps/u * (c*g_x - g_t))
# = -(s/2)*lam^2 * 2c*eps * square(phi * (c*g_x - g_t)/u)
# Since s < 0: this is |s|/2 * lam^2 * 2c*eps * square(phi * h/u)
# where h = c*g_x - g_t.

# For L2 > 0: we need square(phi * h/u) > 0
# where h = c*g_x - g_t is related to the backward characteristic derivative of g.

# If g = g(x-ct) (backward traveling wave), then g_t = -c*g', g_x = g', so h = c*g' - (-c*g') = 2c*g'.
# Then phi * h / u = phi * 2c*g'(x-ct) / u, and square of this should be > 0.
# Actually, for phi = (1+x+ct)^(1/N) (from the base traveling wave):
# phi * 2c*g'/u = 2c*g'*u^(1/N)/u = 2c*g'*u^(1/N - 1)
# square(2c*g'*u^(1/N-1)) = (2c*g')_tt * u^(1/N-1) + ... (product rule with u^(1/N-1))

# This is getting complicated. Let me try a specific perturbation numerically.
# Simplest: g = -log(1+x), so psi = -log(1+x+ct) - eps*log(1+x)

# This is actually the Round 5 ansatz (which failed)! But with eps as a small parameter.
# Round 5 used eps=1 (equal weight). Maybe eps << 1 would work?

# Let's try: psi = -log(1+x+ct) - eps*log(1+x) with eps small
# Run the full verify engine with eps as a parameter

print("\nTesting psi = -log(1+x+ct) - eps*log(1+x)")
print("with different epsilon values:")

def test_candidate_numerical(eps_val, s_val, lam_val_num, c_val, x_range, t_range):
    """Numerically evaluate L2 for the perturbed traveling wave."""
    N = int(round(1.0/abs(lam_val_num)))
    
    results = []
    for x_v in x_range:
        for t_v in t_range:
            x_m = mpmath.mpf(x_v)
            t_m = mpmath.mpf(t_v)
            c_m = mpmath.mpf(c_val)
            eps_m = mpmath.mpf(eps_val)
            s_m = mpmath.mpf(s_val)
            lam_m = mpmath.mpf(lam_val_num)
            
            u = 1 + x_m + c_m*t_m  # 1+x+ct
            X = 1 + x_m            # 1+x
            T = 1 + t_m            # 1+t
            
            # psi = -log(u) - eps*log(X)
            # psi_t = -c/u
            # psi_x = -1/u - eps/X
            # psi_tt = c^2/u^2
            # psi_xx = 1/u^2 + eps/X^2
            # psi_tx = c/u^2
            
            psi_t = -c_m/u
            psi_x = -1/u - eps_m/X
            psi_tt = c_m**2/u**2
            psi_xx = 1/u**2 + eps_m/X**2
            psi_tx = c_m/u**2
            
            box_psi = psi_tt - c_m**2 * psi_xx
            tilde_psi = psi_t**2 - c_m**2 * psi_x**2
            
            # phi = exp(lam*psi) = u^(-lam) * X^(-eps*lam)
            phi = u**(-lam_m) * X**(-eps_m*lam_m)
            
            # phi derivatives (using product rule)
            # phi = u^a * X^b where a = -lam, b = -eps*lam
            a = -lam_m
            b = -eps_m*lam_m
            
            # u_t = c, u_x = 1, X_t = 0, X_x = 1
            phi_t = phi * a * c_m / u
            phi_x = phi * (a / u + b / X)
            phi_tt = phi * (a*(a-1)*c_m**2/u**2)
            phi_xx = phi * ((a*(a-1))/u**2 + 2*a*b/(u*X) + b*(b-1)/X**2)
            phi_tx = phi * (a*c_m*(a-1)/u**2 + a*b*c_m/(u*X))  # Hmm, need to be more careful
            
            # Actually let me compute phi_tx properly
            # phi_t = a*c*phi/u
            # phi_tx = d/dx(a*c*phi/u)
            #        = a*c*(phi_x/u - phi/u^2)
            #        = a*c*phi*(1/u)*(a/u + b/X - 1/u)
            #        = a*c*phi*((a-1)/u^2 + b/(u*X))
            phi_tx = a*c_m*phi*((a-1)/u**2 + b/(u*X))
            
            # tilde_psi derivatives
            # tilde_psi = c^2/u^2 - c^2*(1/u + eps/X)^2
            #           = c^2/u^2 - c^2/u^2 - 2*c^2*eps/(u*X) - c^2*eps^2/X^2
            #           = -2*c^2*eps/(u*X) - c^2*eps^2/X^2
            # Check:
            tilde_check = -2*c_m**2*eps_m/(u*X) - c_m**2*eps_m**2/X**2
            assert abs(float(tilde_psi - tilde_check)) < 1e-30 * max(1, abs(float(tilde_psi)))
            
            # box_psi = c^2/u^2 - c^2*(1/u^2 + eps/X^2) = -c^2*eps/X^2
            box_check = -c_m**2*eps_m/X**2
            assert abs(float(box_psi - box_check)) < 1e-30 * max(1, abs(float(box_psi)))
            
            # tilde_psi_t = d/dt(-2c^2*eps/(uX) - c^2*eps^2/X^2)
            #             = 2c^2*eps*c/(u^2*X) = 2c^3*eps/(u^2*X)
            tilde_psi_t = 2*c_m**3*eps_m/(u**2*X)
            
            # tilde_psi_x = d/dx(-2c^2*eps/(uX) - c^2*eps^2/X^2)
            #             = 2c^2*eps/(u^2*X) + 2c^2*eps/(u*X^2) + 2c^2*eps^2/X^3
            tilde_psi_x = 2*c_m**2*eps_m/(u**2*X) + 2*c_m**2*eps_m/(u*X**2) + 2*c_m**2*eps_m**2/X**3
            
            tilde_psi_tt = -4*c_m**4*eps_m/(u**3*X)
            tilde_psi_xx = (-6*c_m**2*eps_m/(u**3*X) 
                          - 4*c_m**2*eps_m/(u**2*X**2) 
                          - 2*c_m**2*eps_m/(u*X**3) 
                          - 6*c_m**2*eps_m**2/X**4)
            
            # box_psi_t = d/dt(-c^2*eps/X^2) = 0
            box_psi_t = 0
            # box_psi_x = d/dx(-c^2*eps/X^2) = 2c^2*eps/X^3
            box_psi_x = 2*c_m**2*eps_m/X**3
            box_psi_tt = 0
            box_psi_xx = -6*c_m**2*eps_m/X**4
            
            # Now build L2 piece by piece
            alpha_v = 1
            
            # phi*tilde_psi and its second derivatives
            pt = phi * tilde_psi
            pt_tt = phi_tt*tilde_psi + 2*phi_t*tilde_psi_t + phi*tilde_psi_tt
            pt_xx = phi_xx*tilde_psi + 2*phi_x*tilde_psi_x + phi*tilde_psi_xx
            sq_pt = pt_tt - c_m**2 * pt_xx
            
            # phi*box_psi and its second derivatives  
            pb = phi * box_psi
            pb_tt = phi_tt*box_psi + 2*phi_t*box_psi_t + phi*box_psi_tt
            pb_xx = phi_xx*box_psi + 2*phi_x*box_psi_x + phi*box_psi_xx
            sq_pb = pb_tt - c_m**2 * pb_xx
            
            # Term1: (1/2)*((alpha-1)*s*lam*sq_pb - s*lam^2*sq_pt)
            term1 = mpmath.mpf('0.5') * ((alpha_v - 1)*s_m*lam_m*sq_pb - s_m*lam_m**2*sq_pt)
            
            # Term2: s^3*lam^3*(alpha-1)*phi^3*tilde_psi*box_psi - s^3*lam^4*phi^3*tilde_psi^2
            phi3 = phi**3
            term2 = s_m**3 * lam_m**3 * (alpha_v - 1) * phi3 * tilde_psi * box_psi
            term2 -= s_m**3 * lam_m**4 * phi3 * tilde_psi**2
            
            # Term3: s^3*lam^3*(d/dt(phi^3*tilde_psi*psi_t) + c^2*d/dx(phi^3*tilde_psi*psi_x))
            phi3_t = 3*phi**2 * phi_t
            phi3_x = 3*phi**2 * phi_x
            
            dA_dt = phi3_t*tilde_psi*psi_t + phi3*tilde_psi_t*psi_t + phi3*tilde_psi*psi_tt
            dB_dx = phi3_x*tilde_psi*psi_x + phi3*tilde_psi_x*psi_x + phi3*tilde_psi*psi_xx
            
            term3 = s_m**3 * lam_m**3 * (dA_dt + c_m**2 * dB_dx)
            
            L2_val = float(term1 + term2 + term3)
            results.append((x_v, t_v, L2_val))
    
    return results

# Test the perturbed traveling wave with various epsilon
x_test = [0, 1, 10, 100, 1000, 1e6, 1e10, 1e20]
t_test = [0, 1, 10, 100, 1000, 1e6, 1e10, 1e20]

for eps_val in [1.0, 0.1, 0.01, 0.001]:
    print(f"\n--- eps = {eps_val}, s = -1, lam = -1/20, c = 1 ---")
    results = test_candidate_numerical(eps_val, -1.0, -1.0/20, 1.0, x_test, t_test)
    
    min_L2 = min(r[2] for r in results)
    min_point = min(results, key=lambda r: r[2])
    max_L2 = max(r[2] for r in results)
    
    print(f"  min L2 = {min_L2:.6e} at x={min_point[0]:.0e}, t={min_point[1]:.0e}")
    print(f"  max L2 = {max_L2:.6e}")
    
    # Print all negative values
    neg_results = [(x_v, t_v, v) for x_v, t_v, v in results if v < 0]
    if neg_results:
        print(f"  {len(neg_results)} negative values found:")
        for x_v, t_v, v in sorted(neg_results, key=lambda r: r[2])[:5]:
            print(f"    x={x_v:.0e}, t={t_v:.0e}: L2 = {v:.6e}")

# Now test with s depending on c
print("\n\n--- Testing with eps=1, s = -1/(1+c), lam=-1/20 ---")
for c_val in [0.01, 0.1, 1.0, 10.0, 100.0]:
    s_val = -1.0/(1 + c_val)
    print(f"\n  c = {c_val}, s = {s_val:.6f}")
    results = test_candidate_numerical(1.0, s_val, -1.0/20, c_val, 
                                       [0, 100, 1e6, 1e10, 1e20],
                                       [0, 100, 1e6, 1e10, 1e20])
    min_L2 = min(r[2] for r in results)
    min_point = min(results, key=lambda r: r[2])
    print(f"  min L2 = {min_L2:.6e} at x={min_point[0]:.0e}, t={min_point[1]:.0e}")
    neg_results = [(x_v, t_v, v) for x_v, t_v, v in results if v < 0]
    if neg_results:
        print(f"  {len(neg_results)} negative values")
        for x_v, t_v, v in sorted(neg_results, key=lambda r: r[2])[:3]:
            print(f"    x={x_v:.0e}, t={t_v:.0e}: L2 = {v:.6e}")
    else:
        print(f"  ALL POSITIVE!")

