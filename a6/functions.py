import numpy as np


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


def bean_noisy(x, noise):
    """
    Bean function from Appendix D of the book with noise

    Parameters
    ----------
    x : ndarray, shape (2,)
        design variables
    noise : float
        standard deviation of gaussian noise to be added

    Returns
    -------
    f : float
        function value
    """

    x1 = x[0]
    x2 = x[1]

    f = (1. - x1)**2 + (1. - x2)**2 + 0.5 * (2 * x2 - x1**2)**2
    return f + np.random.normal(0, noise)


def bean_check(x, step):
    """
    Bean function from Appendix D of the book

    Parameters
    ----------
    x : ndarray, shape (2,)
        design variables
    step : float
        step for checkerboarding to be added

    Returns
    -------
    f : float
        function value
    """

    x1 = x[0]
    x2 = x[1]

    f = (1. - x1)**2 + (1. - x2)**2 + 0.5 * (2 * x2 - x1**2)**2
    check = step*np.ceil(np.sin(np.pi*x1) * np.sin(np.pi*x2))
    return f + check
