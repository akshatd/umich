
def bean(x):
    """
    Bean function from Appendix D of the book

    Parameters
    ----------
    x : ndarray, shape (2,)
        design variables

    Returns
    -------
    f : float
        function value
    """

    x1 = x[0]
    x2 = x[1]

    return (1. - x1)**2 + (1. - x2)**2 + 0.5 * (2 * x2 - x1**2)**2
