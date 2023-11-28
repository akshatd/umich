import numpy as np
from scipy.interpolate import RegularGridInterpolator


class FevWrapper:
    def __init__(self, f):
        self._f = f
        self._fev = 0

    def __call__(self, x):
        self._fev += 1
        return self._f(x)

    def get_fev(self):
        """
        Returns the number of function calls made.
        """
        return self._fev


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
    g : ndarray, shape (2,)
        objective gradient
    """

    x1 = x[0]
    x2 = x[1]

    f = (1. - x1)**2 + (1. - x2)**2 + 0.5 * (2 * x2 - x1**2)**2

    g = np.zeros(2)
    g[0] = -2. * (1 - x1) - 2. * x1 * (2 * x2 - x1**2)
    g[1] = -2. * (1 - x2) + 2. * (2 * x2 - x1**2)

    return f, g


def bean_f(x):
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


def bean_df(x):
    """
    Bean function from Appendix D of the book

    Parameters
    ----------
    x : ndarray, shape (2,)
        design variables

    Returns
    -------
    g : ndarray, shape (2,)
        objective gradient
    """

    x1 = x[0]
    x2 = x[1]

    g = np.zeros(2)
    g[0] = -2. * (1 - x1) - 2. * x1 * (2 * x2 - x1**2)
    g[1] = -2. * (1 - x2) + 2. * (2 * x2 - x1**2)

    return g


class BeanNoisyPredictable:
    def __init__(self, noise, x0=[0, 0], span=5, grid=100) -> None:
        self.noise = self.__generate_noise_mesh(noise, x0, span, grid)

    def __generate_noise_mesh(self, noise, x0, span, grid):
        x1 = np.linspace(x0[0]-span, x0[0]+span, grid)
        x2 = np.linspace(x0[1]-span, x0[1]+span, grid)
        noise_mesh = np.random.normal(0, noise, (grid, grid))
        return RegularGridInterpolator((x1, x2), noise_mesh)

    def f(self, x):
        return bean_f(x) + self.noise(x)[0]

    def df(self, x):
        fd_step = 1e-6
        noise_g = np.zeros(2)

        h = [fd_step, 0]
        noise_g[0] = (self.noise(x+h) - self.noise(x-h))/(2*h)

        h = [0, fd_step]
        noise_g[1] = (self.noise(x+h) - self.noise(x-h))/(2*h)

        return bean_df(x) + noise_g

    def f_and_df(self, x):
        return self.f(x), self.df(x)


def bean_check_f(x, step):
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


def p62d_f(x):
    return np.abs(x[0]) + 2*np.abs(x[1]) + x[2]**3
