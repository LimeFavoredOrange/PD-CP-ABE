'''
Contains all the auxillary functions to do linear secret sharing (LSS) over an access structure. Mainly, we represent the 
access structure as a binary tree. This could also support matrices for representing access structures.
'''
from charm.core.math.pairing import ZR

def generatePolynomial(threshold, secret, group):
    """
    Generate a polynomial of degree threshold - 1 with the constant term being the secret

    Args:
        threshold (int): the threshold for the current linkNode
        secret (ZR): the secret value to be shared
        group (PairingGroup): the bilinear group used for the scheme

    Returns:
        coeff(list): a list to represent a polynomial
    """
    coeff = [secret]
    for i in range(1, threshold):
        coeff.append(group.random(ZR))
    return coeff


def calculatePolynomial(coeff, x, group):
    """
    Calculate the polynomial at x.

    Args:
        coeff (list): a list to represent a polynomial
        x (ZR): a value to evaluate the polynomial at
        group (PairingGroup): the bilinear group used for the scheme

    Returns:
        result(ZR): the result of the polynomial at x
    """
    result = group.init(ZR, 0)
    x = group.init(ZR, x)
    for i in range(0, len(coeff)):
        temp = int(coeff[i]) * (int(x) ** i)
        temp = group.init(ZR, temp)

        result += temp
    return result