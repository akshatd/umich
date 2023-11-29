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

# 6.2.a


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

# 6.2.b


class BeanNoisyPredictable:
    """
    A class representing a bean with noisy and predictable behavior.

    Parameters:
    - noise (float): The standard deviation of the noise added to the bean's behavior.
    - x0 (list, optional): The initial position of the bean. Defaults to [0, 0].
    - span (float, optional): The span of the bean's behavior. Defaults to 10.
    - grid (int, optional): The number of points in the grid used to generate the noise mesh. Defaults to 1000.
    """

    def __init__(self, noise, x0=[0, 0], span=10, grid=1000) -> None:
        self.noise = self.__generate_noise_mesh(noise, x0, span, grid)

    def __generate_noise_mesh(self, noise, x0, span, grid):
        x1 = np.linspace(x0[0]-span, x0[0]+span, grid)
        x2 = np.linspace(x0[1]-span, x0[1]+span, grid)
        noise_mesh = np.random.normal(0, noise, (grid, grid))
        return RegularGridInterpolator((x1, x2), noise_mesh)

    def f(self, x):
        """
        Calculate the value of the bean's behavior at a given position.

        Parameters:
        - x (list): The position at which to evaluate the bean's behavior.

        Returns:
        - float: The value of the bean's behavior at the given position.
        """
        return bean_f(x) + self.noise(x)[0]

    def df(self, x):
        """
        Calculate the gradient of the bean's behavior at a given position.

        Parameters:
        - x (list): The position at which to evaluate the gradient.

        Returns:
        - numpy.ndarray: The gradient of the bean's behavior at the given position.
        """
        fd_step = 1e-6
        noise_g = np.zeros(2)

        h = [fd_step, 0]
        noise_g[0] = (self.noise(x+h) - self.noise(x-h))/(2*fd_step)

        h = [0, fd_step]
        noise_g[1] = (self.noise(x+h) - self.noise(x-h))/(2*fd_step)

        return bean_df(x) + noise_g

    def fdf(self, x):
        """
        Calculate the value and gradient of the bean's behavior at a given position.

        Parameters:
        - x (list): The position at which to evaluate the bean's behavior and gradient.

        Returns:
        - tuple: A tuple containing the value and gradient of the bean's behavior at the given position.
        """
        return self.f(x), self.df(x)

# 6.2.c


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


def bean_check_df(x):
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
    g : ndarray, shape (2,)
        objective gradient
    """

    x1 = x[0]
    x2 = x[1]

    g = np.zeros(2)
    g[0] = -2. * (1 - x1) - 2. * x1 * (2 * x2 - x1**2)
    g[1] = -2. * (1 - x2) + 2. * (2 * x2 - x1**2)

    return g


# 6.2.d
def p62d_f(x):
    return np.abs(x[0]) + 2*np.abs(x[1]) + x[2]**2


def p62d_df(x):
    g = np.zeros(3)
    g[0] = x[0]/np.abs(x[0])
    g[1] = 2*x[1]/np.abs(x[1])
    g[2] = 2*x[2]
    return g

# 6.3


def rosenbrock_nd_f(x):
    """
    Rosenbrock function from Appendix D of the book

    Parameters
    ----------
    x : ndarray
        design variables

    Returns
    -------
    f : float
        function value
    """
    n = len(x)
    f = 0
    for i in range(n - 1):
        f += 100*(x[i + 1] - x[i]**2)**2 + (1 - x[i])**2

    return f


def rosenbrock_nd_df(x):
    """
    Rosenbrock function from Appendix D of the book
    Partial derivatives from https://math.stackexchange.com/questions/4464953/partial-derivatives-of-the-multidimensional-rosenbrock-function
    Also available at https://docs.scipy.org/doc/scipy/tutorial/optimize.html#broyden-fletcher-goldfarb-shanno-algorithm-method-bfgs

    Parameters
    ----------
    x : ndarray
        design variables

    Returns
    -------
    g : ndarray
        objective gradient
    """
    n = len(x)

    g = np.zeros(n)
    for i in range(n):
        if i == 0:  # no n-1 term
            g[i] = -400*x[i]*(x[i+1]-x[i]**2) + 2*(x[i]-1)
        elif i == n-1:  # no n+1 term
            g[i] = 200*(x[i]-x[i-1]**2)
        else:
            g[i] = -400*x[i]*(x[i+1]-x[i]**2) + 2 * \
                (x[i]-1) + 200*(x[i]-x[i-1]**2)

    return g
