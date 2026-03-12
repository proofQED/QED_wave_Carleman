"""
Verify psi = -log(1+x+ct) - log(1+ct) at extreme points.
ALL coefficients in L2 appear positive! Verify this.
"""
import sympy as sp
import mpmath
import sys
sys.path.insert(0, '/local/home/cyanz/wave_PINN')
from verify_engine import x, t, c, x0, alpha, s, lam, build_operators, run_verification

mpmath.mp.dps = 80

print("="*80)
print("VERIFICATION: psi = -log(1+x+ct) - log(1+ct)")
print("="*80)

# First, let me carefully examine the L2 numerator structure.
# The engine output shows L2 = c^4 * N(x,t,c) / D(x,t,c) where D > 0.
# Let me extract and check every coefficient in N.

psi_new = -sp.ln(1 + x + c*t) - sp.ln(1 + c*t)

subs_new = {
    alpha: 1,
    s: sp.Rational(-1, 100),
    lam: sp.Rational(-1, 20),
}

ops = build_operators(psi_new, subs_new)
L2 = ops['L2']

# Let me substitute u = c*t (for simplicity) and check
# Actually, let me check L2 at extreme mpmath values

def eval_L2_new(x_v, t_v, c_v):
    """Evaluate L2 for psi = -log(1+x+ct) - log(1+ct) using mpmath."""
    x_v = mpmath.mpf(x_v)
    t_v = mpmath.mpf(t_v)
    c_v = mpmath.mpf(c_v)
    N = 20
    lam_v = mpmath.mpf(-1)/N
    s_v = mpmath.mpf(-1)/100
    alpha_v = mpmath.mpf(1)
    
    u = 1 + x_v + c_v*t_v   # 1+x+ct
    v = 1 + c_v*t_v          # 1+ct
    
    psi_t = -c_v/u - c_v/v
    psi_x = -1/u
    psi_tt = c_v**2/u**2 + c_v**2/v**2
    psi_xx = 1/u**2
    psi_tx = c_v/u**2
    
    box_psi = psi_tt - c_v**2 * psi_xx  # = c^2/u^2 + c^2/v^2 - c^2/u^2 = c^2/v^2
    tilde_psi = psi_t**2 - c_v**2 * psi_x**2  # = (c/u+c/v)^2 - c^2/u^2 = c^2/v^2 + 2c^2/(uv)
    
    # phi = (u*v)^{1/N}
    phi = (u * v)**(mpmath.mpf(1)/N)
    a = mpmath.mpf(1)/N  # exponent for u
    b = mpmath.mpf(1)/N  # exponent for v
    
    # phi derivatives: phi = u^a * v^b
    # u_t = c, u_x = 1, v_t = c, v_x = 0
    phi_t = phi * (a*c_v/u + b*c_v/v)
    phi_x = phi * (a/u)
    phi_tt = phi * ((a*(a-1)*c_v**2/u**2 + 2*a*b*c_v**2/(u*v) + b*(b-1)*c_v**2/v**2) 
                    + (a*c_v/u + b*c_v/v)**2 - (a*c_v/u + b*c_v/v)**2 
                    + (a*(a-1)*c_v**2/u**2 + 2*a*b*c_v**2/(u*v) + b*(b-1)*c_v**2/v**2))
    # Hmm, let me be more careful. phi = u^a * v^b
    # phi_t = a*c*u^{a-1}*v^b + b*c*u^a*v^{b-1} = phi*(a*c/u + b*c/v)
    # phi_tt = d/dt[phi*(ac/u + bc/v)]
    #        = phi_t*(ac/u + bc/v) + phi*(-ac^2/u^2 - bc^2/v^2)
    #        = phi*(ac/u+bc/v)^2 + phi*(-ac^2/u^2 - bc^2/v^2)
    #        = phi*((ac/u+bc/v)^2 - ac^2/u^2 - bc^2/v^2)
    #        = phi*(a^2c^2/u^2 + 2abc^2/(uv) + b^2c^2/v^2 - ac^2/u^2 - bc^2/v^2)
    #        = phi*(a(a-1)c^2/u^2 + 2abc^2/(uv) + b(b-1)c^2/v^2)
    phi_tt = phi * (a*(a-1)*c_v**2/u**2 + 2*a*b*c_v**2/(u*v) + b*(b-1)*c_v**2/v**2)
    phi_xx = phi * (a*(a-1)/u**2)  # since v_x = 0
    phi_tx = phi * (a*c_v*(a-1)/u**2 + a*b*c_v/(u*v))  # d/dx[phi_t]
    # phi_t = phi*(ac/u + bc/v)
    # phi_tx = d/dx[phi*(ac/u+bc/v)] = phi_x*(ac/u+bc/v) + phi*(-ac/u^2)  [v_x=0]
    #        = phi*(a/u)*(ac/u+bc/v) + phi*(-ac/u^2)
    #        = phi*a*c/u*(a/u-1/u) + phi*ab*c/(u*v)... let me redo
    #        = phi*(a/u)*(ac/u+bc/v) - phi*ac/u^2
    #        = phi*[a^2c/u^2 + abc/(uv) - ac/u^2]
    #        = phi*[a(a-1)c/u^2 + abc/(uv)]
    phi_tx = phi * (a*(a-1)*c_v/u**2 + a*b*c_v/(u*v))
    
    # Derivatives of tilde_psi and box_psi
    # tilde_psi = c^2/v^2 + 2c^2/(uv)
    tilde_t = -2*c_v**3/v**3 - 2*c_v**3/(u**2*v) - 2*c_v**3/(u*v**2)
    tilde_x = 2*c_v**2/(u**2*v)
    tilde_tt = 6*c_v**4/v**4 + 2*c_v**4/(u**3*v)*2 + 4*c_v**4/(u**2*v**2) + 6*c_v**4/(u*v**3)
    # Actually this is getting complicated. Let me use a different approach.
    
    # Use finite differences for verification
    h = mpmath.mpf('1e-15')
    
    def psi_func(xx, tt):
        uu = 1 + xx + c_v*tt
        vv = 1 + c_v*tt
        return -mpmath.log(uu) - mpmath.log(vv)
    
    def phi_func(xx, tt):
        return mpmath.exp(lam_v * psi_func(xx, tt))
    
    def tilde_psi_func(xx, tt):
        pt = (psi_func(xx, tt+h) - psi_func(xx, tt-h))/(2*h)
        px = (psi_func(xx+h, tt) - psi_func(xx-h, tt))/(2*h)
        return pt**2 - c_v**2 * px**2
    
    def box_psi_func(xx, tt):
        ptt = (psi_func(xx, tt+h) - 2*psi_func(xx, tt) + psi_func(xx, tt-h))/h**2
        pxx = (psi_func(xx+h, tt) - 2*psi_func(xx, tt) + psi_func(xx-h, tt))/h**2
        return ptt - c_v**2 * pxx
    
    # Compute L2 numerically using the full formula
    # This is extremely tedious. Let me instead use sympy's lambdify.
    # Actually, let me just use the symbolic expression and substitute.
    
    val = L2.subs([(x, mpmath.mpf(x_v)), (t, mpmath.mpf(t_v)), (c, mpmath.mpf(c_v))])
    return float(val.evalf(50))

# Test at extreme points
test_points = [
    (0, 0, 1),
    (0, 1e10, 1),
    (0, 1e20, 1),
    (0, 1e50, 1),
    (0, 1e100, 1),
    (0, 1e200, 1),
    (1e10, 0, 1),
    (1e20, 0, 1),
    (1e50, 0, 1),
    (1e100, 0, 1),
    (1e10, 1e10, 1),
    (1e20, 1e20, 1),
    (0, 0, 100),
    (0, 0, 1e6),
    (0, 0, 1e10),
    (0, 0, 0.01),
    (0, 0, 0.001),
    (0, 1e10, 100),
    (0, 1e20, 100),
    (0, 1e100, 100),
    (1e10, 0, 0.01),
    (1e10, 1e10, 0.01),
    (0, 1e10, 0.01),
    (0, 1e20, 0.01),
    (0, 1e100, 0.01),
    (0, 1e200, 0.01),
]

print("\nExtreme point tests for L2:")
all_positive = True
for x_v, t_v, c_v in test_points:
    try:
        L2_v = eval_L2_new(x_v, t_v, c_v)
        status = "+" if L2_v > 0 else "-" if L2_v < 0 else "0"
        if L2_v <= 0:
            all_positive = False
        print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.2e}: L2 = {L2_v:.6e} [{status}]")
    except Exception as e:
        print(f"  x={x_v:.0e}, t={t_v:.0e}, c={c_v:.2e}: ERROR {e}")

print(f"\nAll tested points positive? {all_positive}")

# Now let's understand WHY L2 has all positive terms.
# For this ansatz: box(psi) = c^2/(1+ct)^2, tilde(psi) = c^2/(1+ct)^2 + 2c^2/((1+x+ct)(1+ct))
# Both are POSITIVE for all x, t >= 0!
# 
# In the double-log: tilde(psi) = 1/(1+t)^2 - c^2/(1+x)^2 which CHANGES SIGN.
# The sign change created negative contributions to L2.
# Here, tilde(psi) > 0 always, which might make ALL L2 terms positive!

print("\n\nStructural analysis:")
print("For psi = -log(1+x+ct) - log(1+ct):")
print("  box(psi) = c^2/(1+ct)^2 > 0 always")
print("  tilde(psi) = c^2/(1+ct)^2 + 2c^2/((1+x+ct)(1+ct)) > 0 always")
print()
print("Compare with double-log psi = -log(1+t) - log(1+x):")
print("  box(psi) = tilde(psi) = 1/(1+t)^2 - c^2/(1+x)^2 which CHANGES SIGN!")
print()
print("The sign-definite tilde(psi) may be why ALL L2 terms have positive coefficients.")

