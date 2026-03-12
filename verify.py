import sympy as sp


# ============================================================
# Symbols
# ============================================================
x, t = sp.symbols( 'x t', real = True )
c = sp.symbols( 'c', positive = True, real = True )

x0 = sp.symbols( 'x0', real = True )
alpha, s, lam = sp.symbols( 'alpha s lam', real = True )


# ============================================================
# Test choice
# ============================================================
psi = t - ( x + x0 ) ** 2

subs_dict = {
    alpha : 2,
    x0    : c / 2,
    s     : -2,
    lam   : - c ** 2,
}


# ============================================================
# Definitions
# ============================================================
phi = sp.exp( lam * psi )

def square( u ):
    return sp.diff( u, t, 2 ) - c ** 2 * sp.diff( u, x, 2 )

def tilde_square( u ):
    return sp.diff( u, t ) ** 2 - c ** 2 * sp.diff( u, x ) ** 2

L = lam ** 2 * phi * tilde_square( psi ) - ( alpha - 1 ) * lam * phi * square( psi )

L1 = c ** 2 * sp.diff( phi, x, 2 ) + sp.diff( phi, t, 2 )

L2 = (
    sp.Rational( 1, 2 ) * (
        ( alpha - 1 ) * s * lam * square( phi * square( psi ) )
        - s * lam ** 2 * square( phi * tilde_square( psi ) )
    )
    + (
        s ** 3 * lam ** 3 * ( alpha - 1 ) * phi ** 3 * tilde_square( psi ) * square( psi )
        - s ** 3 * lam ** 4 * phi ** 3 * tilde_square( psi )**2
        + s ** 3 * lam ** 3 * (
            sp.diff( phi ** 3 * tilde_square( psi ) * sp.diff( psi, t ), t )
            + c ** 2 * sp.diff( phi ** 3 * tilde_square( psi ) * sp.diff( psi, x ), x )
        )
    )
)


# ============================================================
# Substitute the test parameters
# ============================================================
psi_test = sp.simplify( psi.subs( subs_dict ) )
phi_test = sp.simplify( phi.subs( subs_dict ) )
L_test = sp.simplify( sp.expand( L.subs( subs_dict ) ) )
L1_test = sp.simplify( sp.expand( L1.subs( subs_dict ) ) )
L2_test = sp.simplify( sp.expand( L2.subs( subs_dict ) ) )


# ============================================================
# Utility functions
# ============================================================
def normalize_positive_factors( expr ):
    """
    Remove factors that are always positive under the current assumptions.
    This often turns expressions like exp(...) * polynomial into just polynomial.
    """
    expr = sp.factor( sp.simplify( expr ) )

    if expr == 0:
        return sp.Integer( 0 )

    if isinstance( expr, sp.Mul ):
        kept = []
        for factor in expr.args:
            if factor.is_positive is True:
                continue
            kept.append( factor )
        if not kept:
            return sp.Integer( 1 )
        return sp.factor( sp.Mul( * kept ) )

    return expr


def truth_value_from_sign( expr, relation = '>=0' ):
    """
    Return True / False / 'unknown' for a sign condition.

    relation options:
        '>=0', '<=0', '>0', '<0', '==0'
    """
    expr_simplified = sp.simplify( expr )
    expr_normalized = normalize_positive_factors( expr_simplified )

    if relation == '>=0':
        if expr_normalized.is_nonnegative is True:
            return True
        if expr_normalized.is_negative is True:
            return False

    elif relation == '<=0':
        if expr_normalized.is_nonpositive is True:
            return True
        if expr_normalized.is_positive is True:
            return False

    elif relation == '>0':
        if expr_normalized.is_positive is True:
            return True
        if expr_normalized.is_nonpositive is True:
            return False

    elif relation == '<0':
        if expr_normalized.is_negative is True:
            return True
        if expr_normalized.is_nonnegative is True:
            return False

    elif relation == '==0':
        if sp.simplify( expr_normalized ) == 0:
            return True
        if expr_normalized.is_zero is False:
            return False

    return 'unknown'


def format_status( value ):
    if value is True:
        return 'True'
    if value is False:
        return 'False'
    return 'unknown'


def check_limit_is_pos_infinity( expr, var ):
    """
    Return True / False / 'unknown' for limit(expr, var -> +oo) = +oo.
    """
    try:
        lim = sp.limit( sp.simplify( expr ), var, sp.oo )
    except Exception:
        return 'unknown', None

    if lim == sp.oo:
        return True, lim
    if lim in ( - sp.oo, sp.zoo ) or lim.is_finite is True:
        return False, lim
    return 'unknown', lim


# ============================================================
# Display main symbolic expressions
# ============================================================
print( 'psi =' )
sp.pprint( psi_test )
print()

print( 'phi =' )
sp.pprint( phi_test )
print()

print( 'L psi =' )
sp.pprint( sp.factor( L_test ) )
print()

print( 'L1 psi =' )
sp.pprint( sp.factor( L1_test ) )
print()

print( 'L2 psi =' )
sp.pprint( sp.factor( L2_test ) )
print()


# ============================================================
# Necessary condition 1:
#     -L1 psi <= L psi <= L1 psi
# equivalent to
#     L + L1 >= 0
#     L1 - L >= 0
# ============================================================
cond_1a_expr = sp.simplify( L_test - L1_test )
cond_1b_expr = sp.simplify( - L1_test - L_test )

cond_1a = truth_value_from_sign( cond_1a_expr, '>0' )
cond_1b = truth_value_from_sign( cond_1b_expr, '>0' )

cond_1 = (
    True if ( cond_1a is True and cond_1b is True ) else
    False if ( cond_1a is False or cond_1b is False ) else
    'unknown'
)

print( 'Condition 1a: L psi - L1 psi =' )
sp.pprint( sp.factor( cond_1a_expr ) )
print( 'Condition 1a status =', format_status( cond_1a ) )
print()

print( 'Condition 1b: - L1 psi - L psi =' )
sp.pprint( sp.factor( cond_1b_expr ) )
print( 'Condition 1b status =', format_status( cond_1b ) )
print()

print( 'Necessary condition 1 status =', format_status( cond_1 ) )
print()


# ============================================================
# Necessary condition 2:
#     limit_{x -> +infty} lam * psi = +infty
# ============================================================
limit_expr = sp.simplify( ( lam * psi ).subs( subs_dict ) )
cond_2, limit_value = check_limit_is_pos_infinity( limit_expr, x )

print( 'lambda * psi =' )
sp.pprint( limit_expr )
print()

print( 'limit_{ x -> +infty } lambda * psi =' )
sp.pprint( limit_value )
print( 'Necessary condition 2 status =', format_status( cond_2 ) )
print()


# ============================================================
# Necessary condition 3:
#     L2 psi >= 0
# ============================================================
cond_3_expr = sp.simplify( L2_test )
cond_3 = truth_value_from_sign( cond_3_expr, '>0' )

print( 'L2 psi =' )
sp.pprint( sp.factor( cond_3_expr ) )
print()

print( 'L2 psi / phi^3 =' )
sp.pprint( sp.factor( sp.simplify( cond_3_expr / phi_test ** 3 ) ) )
print( 'Necessary condition 3 status =', format_status( cond_3 ) )
print()


# ============================================================
# Sufficient condition:
#     (L1 psi)^2 - (L psi)^2 >= c^2 (phi_xt)^2
# equivalent to
#     (L1 psi)^2 - (L psi)^2 - c^2 (phi_xt)^2 >= 0
# ============================================================
phi_xt_test = sp.simplify( sp.diff( phi_test, x, t ) )

sufficient_expr = sp.simplify(
    L1_test ** 2 - L_test ** 2 - c ** 2 * phi_xt_test ** 2
)

sufficient_status = truth_value_from_sign( sufficient_expr, '>=0' )

print( 'phi_xt =' )
sp.pprint( sp.factor( phi_xt_test ) )
print()

print( 'Sufficient condition expression =' )
sp.pprint( sp.factor( sufficient_expr ) )
print()

print( 'Sufficient condition expression / phi^2 =' )
sp.pprint( sp.factor( sp.simplify( sufficient_expr / phi_test ** 2 ) ) )
print( 'Sufficient condition status =', format_status( sufficient_status ) )
print()


# ============================================================
# Overall summary
# ============================================================
overall_necessary = (
    True if all( v is True for v in [ cond_1, cond_2, cond_3 ] ) else
    False if any( v is False for v in [ cond_1, cond_2, cond_3 ] ) else
    'unknown'
)

print( '================ SUMMARY ================' )
print( 'Necessary condition 1  :', format_status( cond_1 ) )
print( 'Necessary condition 2  :', format_status( cond_2 ) )
print( 'Necessary condition 3  :', format_status( cond_3 ) )
print( 'All necessary conditions:', format_status( overall_necessary ) )
print( 'Sufficient condition   :', format_status( sufficient_status ) )
