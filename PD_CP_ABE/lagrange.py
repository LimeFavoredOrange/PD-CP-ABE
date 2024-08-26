from charm.core.math.pairing import ZR


def lagrange_basis(group, points, i, x):
    """
    Computes the i-th Lagrange basis polynomial at x.
    
    Args:
    points (list of tuples): List of (x, y) points
    i (int): Index of the basis polynomial to compute
    x (float): The value at which to evaluate the basis polynomial
    
    Returns:
    float: The value of the i-th Lagrange basis polynomial at x
    """
    xi, _ = points[i]
    x = group.init(ZR, x)

    result = group.init(ZR, 1)
    for j, (xj, _) in enumerate(points):
        if i != j:
            result *= (x - xj) / (xi - xj)
    return result


def lagrange_polynomial(group, points):
    """
    Generates the Lagrange polynomial for the given set of points.
    
    Args:
    points (list of tuples): List of (x, y) points
    
    Returns:
    function: The Lagrange polynomial as a function
    """
    def polynomial(x):
        n = len(points)
        result = group.init(ZR, 0)
        for i in range(n):
            xi, yi = points[i]
            result += yi * lagrange_basis(group, points, i, x)
        
        return result
    
    return polynomial



def lagrange_basis_bilinear_mapping(group, points, i, x):
    """
    Computes the i-th Lagrange basis polynomial at x.
    
    Args:
    points (list of tuples): List of (x, y) points
    i (int): Index of the basis polynomial to compute
    x (float): The value at which to evaluate the basis polynomial
    
    Returns:
    float: The value of the i-th Lagrange basis polynomial at x
    """
    xi, _ = points[i]

    x = group.init(ZR, x)
    xi = group.init(ZR, xi)

    result = group.init(ZR, 1)
    for j, (xj, _) in enumerate(points):
        xj = group.init(ZR, xj)
        if i != j:
            result *= (x - xj) / (xi - xj)
    return result




def lagrange_polynomial_bilinear_mapping(group, points):
    """
    Generates the Lagrange polynomial for the given set of points.
    
    Args:
    points (list of tuples): List of (x, y) points
    
    Returns:
    function: The Lagrange polynomial as a function
    """

    def polynomial(x):
        n = len(points)

        result = group.init(ZR, 1)
        for i in range(n):
            xi, yi = points[i]
            result *= yi ** lagrange_basis_bilinear_mapping(group, points, i, 0)

        return result
    
    return polynomial
