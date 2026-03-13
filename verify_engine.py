"""
Verification engine for the wave PINN weight construction problem.

This module contains:
  - All operator definitions (square, tilde_square, L, L1, L2)
  - Symbolic sign-checking utilities
  - Numerical sampling fallback for 'unknown' results
  - A run_verification() entry point that accepts (psi, subs_dict)
    and returns a structured result dict + prints a human-readable report.

Usage:
    python verify_engine.py candidates/round_N/candidate.py
"""

import sys
import importlib.util
import json
import numpy as np
import sympy as sp


# ============================================================
# Shared symbols  (importable by candidate files)
# ============================================================
x, t = sp.symbols('x t', real=True)
c = sp.symbols('c', positive=True, real=True)
x0 = sp.symbols('x0', real=True)
alpha, s, lam = sp.symbols('alpha s lam', real=True)


# ============================================================
# Operators
# ============================================================
def square(u):
    """Wave operator: square(u) = u_tt - c^2 u_xx."""
    return sp.diff(u, t, 2) - c**2 * sp.diff(u, x, 2)


def tilde_square(u):
    """Energy-like form: tilde_square(u) = (u_t)^2 - c^2 (u_x)^2."""
    return sp.diff(u, t)**2 - c**2 * sp.diff(u, x)**2


def build_operators(psi_expr, subs):
    """
    Given a symbolic psi and a substitution dict, build all operators
    and return them after substitution + simplification.
    """
    phi_sym = sp.exp(lam * psi_expr)

    L_sym = (lam**2 * phi_sym * tilde_square(psi_expr)
             - (alpha - 1) * lam * phi_sym * square(psi_expr))

    L1_sym = c**2 * sp.diff(phi_sym, x, 2) + sp.diff(phi_sym, t, 2)

    L2_sym = (
        sp.Rational(1, 2) * (
            (alpha - 1) * s * lam * square(phi_sym * square(psi_expr))
            - s * lam**2 * square(phi_sym * tilde_square(psi_expr))
        )
        + (
            s**3 * lam**3 * (alpha - 1) * phi_sym**3
            * tilde_square(psi_expr) * square(psi_expr)
            - s**3 * lam**4 * phi_sym**3 * tilde_square(psi_expr)**2
            + s**3 * lam**3 * (
                sp.diff(phi_sym**3 * tilde_square(psi_expr)
                        * sp.diff(psi_expr, t), t)
                - c**2 * sp.diff(phi_sym**3 * tilde_square(psi_expr)
                                 * sp.diff(psi_expr, x), x)
            )
        )
    )

    psi_sub = sp.simplify(psi_expr.subs(subs))
    phi_sub = sp.simplify(phi_sym.subs(subs))
    L_sub = sp.simplify(sp.expand(L_sym.subs(subs)))
    L1_sub = sp.simplify(sp.expand(L1_sym.subs(subs)))
    L2_sub = sp.simplify(sp.expand(L2_sym.subs(subs)))

    return {
        'psi': psi_sub,
        'phi': phi_sub,
        'L': L_sub,
        'L1': L1_sub,
        'L2': L2_sub,
    }


# ============================================================
# Utility functions
# ============================================================
def normalize_positive_factors(expr):
    """Remove factors that are provably always positive."""
    expr = sp.factor(sp.simplify(expr))
    if expr == 0:
        return sp.Integer(0)
    if isinstance(expr, sp.Mul):
        kept = [f for f in expr.args if f.is_positive is not True]
        if not kept:
            return sp.Integer(1)
        return sp.factor(sp.Mul(*kept))
    return expr


def truth_value_from_sign(expr, relation='>=0'):
    """Return True / False / 'unknown' for a sign condition."""
    expr_simplified = sp.simplify(expr)
    expr_normalized = normalize_positive_factors(expr_simplified)

    checks = {
        '>=0': ('is_nonnegative', 'is_negative'),
        '<=0': ('is_nonpositive', 'is_positive'),
        '>0':  ('is_positive', 'is_nonpositive'),
        '<0':  ('is_negative', 'is_nonnegative'),
    }

    if relation == '==0':
        if sp.simplify(expr_normalized) == 0:
            return True
        if expr_normalized.is_zero is False:
            return False
        return 'unknown'

    if relation in checks:
        pos_attr, neg_attr = checks[relation]
        if getattr(expr_normalized, pos_attr) is True:
            return True
        if getattr(expr_normalized, neg_attr) is True:
            return False

    return 'unknown'


def fmt(value):
    if value is True:
        return 'True'
    if value is False:
        return 'False'
    return 'unknown'


def check_limit_is_pos_infinity(expr, var):
    """Return (True/False/'unknown', limit_value)."""
    try:
        lim = sp.limit(sp.simplify(expr), var, sp.oo)
    except Exception:
        return 'unknown', None
    if lim == sp.oo:
        return True, lim
    if lim in (-sp.oo, sp.zoo) or lim.is_finite is True:
        return False, lim
    return 'unknown', lim


# ============================================================
# Numerical sampling fallback
# ============================================================
def numerical_check(expr, relation='>=0',
                    x_range=(0, 50, 20), t_range=(0, 10, 20),
                    c_vals=(0.5, 1.0, 2.0)):
    """
    Sample expr on a grid of (x, t, c) and check the relation numerically.

    Returns:
        'likely_true'  – no violations found
        'false'        – a concrete violation was found
        'error'        – evaluation failed
        + dict with details (min_value, violation_point, etc.)
    """
    f = sp.lambdify((x, t, c), expr, modules='numpy')

    x_arr = np.linspace(*x_range)
    t_arr = np.linspace(*t_range)

    global_min = float('inf')
    global_max = float('-inf')
    violation = None

    for c_val in c_vals:
        try:
            X, T = np.meshgrid(x_arr, t_arr)
            Z = f(X, T, c_val)

            if not np.all(np.isfinite(Z)):
                continue

            local_min = float(np.min(Z))
            local_max = float(np.max(Z))
            global_min = min(global_min, local_min)
            global_max = max(global_max, local_max)

            if relation == '>=0' and local_min < -1e-10:
                idx = np.unravel_index(np.argmin(Z), Z.shape)
                violation = {
                    'x': float(X[idx]),
                    't': float(T[idx]),
                    'c': c_val,
                    'value': local_min,
                }
                return 'false', {
                    'min': global_min, 'max': global_max,
                    'violation': violation,
                }
        except Exception:
            continue

    if global_min == float('inf'):
        return 'error', {}

    return 'likely_true', {'min': global_min, 'max': global_max}


# ============================================================
# Main verification routine
# ============================================================
def run_verification(psi_expr, subs_dict):
    """
    Run all checks on a candidate (psi, subs_dict).

    Returns (results_dict, report_string).
    """
    lines = []

    def log(msg=''):
        lines.append(msg)

    # ----------------------------------------------------------
    # 0. Basic parameter check
    # ----------------------------------------------------------
    s_val = subs_dict.get(s)
    if s_val is not None:
        s_numeric = float(sp.N(s_val.subs(subs_dict) if hasattr(s_val, 'subs') else s_val))
        if s_numeric >= 0:
            log(f'WARNING: s = {s_val} is not negative. The problem requires s < 0.')

    # ----------------------------------------------------------
    # 1. Build operators
    # ----------------------------------------------------------
    log('Building operators ...')
    ops = build_operators(psi_expr, subs_dict)

    log(f'psi = {ops["psi"]}')
    log(f'phi = {ops["phi"]}')
    log(f'L psi = {sp.factor(ops["L"])}')
    log(f'L1 psi = {sp.factor(ops["L1"])}')
    log(f'L2 psi = {sp.factor(ops["L2"])}')
    log()

    results = {}

    # ----------------------------------------------------------
    # 2. Necessary condition 1:  L1 psi <= L psi <= -L1 psi
    # ----------------------------------------------------------
    cond_1a_expr = sp.simplify(ops['L'] - ops['L1'])
    cond_1b_expr = sp.simplify(-ops['L1'] - ops['L'])

    cond_1a = truth_value_from_sign(cond_1a_expr, '>0')
    cond_1b = truth_value_from_sign(cond_1b_expr, '>0')

    cond_1 = (
        True if (cond_1a is True and cond_1b is True) else
        False if (cond_1a is False or cond_1b is False) else
        'unknown'
    )

    # Numerical fallback for unknown
    num_1a = num_1b = None
    if cond_1a == 'unknown':
        num_1a_status, num_1a = numerical_check(cond_1a_expr)
        log(f'Condition 1a numerical sampling: {num_1a_status} {num_1a}')
    if cond_1b == 'unknown':
        num_1b_status, num_1b = numerical_check(cond_1b_expr)
        log(f'Condition 1b numerical sampling: {num_1b_status} {num_1b}')

    log(f'Condition 1a (L - L1 > 0): {fmt(cond_1a)}')
    log(f'  expression = {sp.factor(cond_1a_expr)}')
    log(f'Condition 1b (-L1 - L > 0): {fmt(cond_1b)}')
    log(f'  expression = {sp.factor(cond_1b_expr)}')
    log(f'Necessary condition 1: {fmt(cond_1)}')
    log()

    results['cond_1'] = {
        'status': fmt(cond_1),
        'cond_1a': fmt(cond_1a),
        'cond_1b': fmt(cond_1b),
        'numerical_1a': num_1a,
        'numerical_1b': num_1b,
    }

    # ----------------------------------------------------------
    # 3. Necessary condition 2:  lim_{x->+inf} lam*psi = +inf
    # ----------------------------------------------------------
    limit_expr = sp.simplify((lam * psi_expr).subs(subs_dict))
    cond_2, limit_value = check_limit_is_pos_infinity(limit_expr, x)

    log(f'lambda * psi = {limit_expr}')
    log(f'limit_{{x -> +inf}} lambda * psi = {limit_value}')
    log(f'Necessary condition 2: {fmt(cond_2)}')
    log()

    results['cond_2'] = {
        'status': fmt(cond_2),
        'limit_value': str(limit_value),
    }

    # ----------------------------------------------------------
    # 4. Necessary condition 3:  L2 psi >= 0
    # ----------------------------------------------------------
    cond_3_expr = sp.simplify(ops['L2'])
    cond_3 = truth_value_from_sign(cond_3_expr, '>0')

    num_3 = None
    if cond_3 == 'unknown':
        num_3_status, num_3 = numerical_check(cond_3_expr)
        log(f'Condition 3 numerical sampling: {num_3_status} {num_3}')

    log(f'L2 psi = {sp.factor(cond_3_expr)}')
    try:
        log(f'L2 psi / phi^3 = {sp.factor(sp.simplify(cond_3_expr / ops["phi"]**3))}')
    except Exception:
        pass
    log(f'Necessary condition 3: {fmt(cond_3)}')
    log()

    results['cond_3'] = {
        'status': fmt(cond_3),
        'numerical': num_3,
    }

    # ----------------------------------------------------------
    # 5. Sufficient condition:
    #     (L1)^2 - (L)^2 >= c^2 (phi_xt)^2
    # ----------------------------------------------------------
    phi_xt = sp.simplify(sp.diff(ops['phi'], x, t))
    suff_expr = sp.simplify(ops['L1']**2 - ops['L']**2 - c**2 * phi_xt**2)
    suff_status = truth_value_from_sign(suff_expr, '>=0')

    num_suff = None
    if suff_status == 'unknown':
        num_suff_status, num_suff = numerical_check(suff_expr)
        log(f'Sufficient condition numerical sampling: {num_suff_status} {num_suff}')

    log(f'phi_xt = {sp.factor(phi_xt)}')
    log(f'Sufficient condition expr = {sp.factor(suff_expr)}')
    try:
        log(f'Sufficient condition expr / phi^2 = '
            f'{sp.factor(sp.simplify(suff_expr / ops["phi"]**2))}')
    except Exception:
        pass
    log(f'Sufficient condition: {fmt(suff_status)}')
    log()

    results['sufficient'] = {
        'status': fmt(suff_status),
        'numerical': num_suff,
    }

    # ----------------------------------------------------------
    # 6. Overall summary
    # ----------------------------------------------------------
    all_nec = [cond_1, cond_2, cond_3]
    overall_necessary = (
        True if all(v is True for v in all_nec) else
        False if any(v is False for v in all_nec) else
        'unknown'
    )

    log('================ SUMMARY ================')
    log(f'Necessary condition 1  : {fmt(cond_1)}')
    log(f'Necessary condition 2  : {fmt(cond_2)}')
    log(f'Necessary condition 3  : {fmt(cond_3)}')
    log(f'All necessary conditions: {fmt(overall_necessary)}')
    log(f'Sufficient condition   : {fmt(suff_status)}')

    all_pass = (overall_necessary is True and suff_status is True)
    log(f'ALL CONDITIONS PASS    : {fmt(all_pass)}')

    results['overall'] = {
        'all_necessary': fmt(overall_necessary),
        'sufficient': fmt(suff_status),
        'all_pass': fmt(all_pass),
    }

    report = '\n'.join(lines)
    return results, report


# ============================================================
# CLI: load candidate file and run
# ============================================================
def load_candidate(path):
    """
    Load a candidate.py file that defines `psi` and `subs_dict`.

    The candidate file may import symbols from this module:
        from verify_engine import x, t, c, x0, alpha, s, lam
    """
    spec = importlib.util.spec_from_file_location('candidate', path)
    mod = importlib.util.module_from_spec(spec)

    # Inject our symbols into the candidate module's namespace
    # so that `from verify_engine import ...` works even when
    # the candidate is loaded dynamically.
    mod.sp = sp
    mod.x = x
    mod.t = t
    mod.c = c
    mod.x0 = x0
    mod.alpha = alpha
    mod.s = s
    mod.lam = lam

    spec.loader.exec_module(mod)

    if not hasattr(mod, 'psi'):
        raise ValueError(f'{path} does not define `psi`')
    if not hasattr(mod, 'subs_dict'):
        raise ValueError(f'{path} does not define `subs_dict`')

    return mod.psi, mod.subs_dict


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python verify_engine.py <candidate.py>')
        print('       python verify_engine.py <candidate.py> --json')
        sys.exit(1)

    candidate_path = sys.argv[1]
    json_mode = '--json' in sys.argv

    psi_expr, subs = load_candidate(candidate_path)
    results, report = run_verification(psi_expr, subs)

    if json_mode:
        print(json.dumps(results, indent=2))
    else:
        print(report)
