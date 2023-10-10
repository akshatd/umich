#!/usr/bin/env python
# coding: utf-8

# ### 2.2
#
# Analytically, we get partial derivatives as
#
# - wrt $x_1$: $4x_1^3 + 9x_1^2 − 6x_2$
# - wrt $x_2$: $6x_2 − 6x_1 −2$
#
# Solving
#
# - $4x_1^3 + 9x_1^2 − 6x_2 = 0$
# - $6x_2 − 6x_1 −2 = 0$
#
# The roots are $(x_1, x_2)$
#
# To classify them, we calculate the Hessians at the points and use their eigenvalues
#
# - $(- \sqrt3 - 1), (-\sqrt3 - 2/3)$ : Global minimum (-2.73205, -2.39871)
# - $(-1 + \sqrt3) , (-2/3 + \sqrt3)$ : Local minimum (0.73205, 1.06538)
# - $-1/4, 1/12$ : Saddle Point (-0.25, 0.08333)
#
# ![equations](2_2.png)
#

# In[8]:


# import required modules
from typing import Callable

import numpy.typing as npt

import numpy as np
import matplotlib.pyplot as plt

# function from the problem


def function2(x: npt.ArrayLike) -> float:
    return pow(x[0], 4) + 3 * pow(x[0], 3) + 3 * \
        pow(x[1], 2) - 6 * x[0] * x[1] - 2 * x[1]


def prep_data(function: Callable[[float,
                                  float],
                                 float],
              range_x1: tuple[float,
                              float,
                              float],
              range_x2: tuple[float,
                              float,
                              float]) -> tuple[npt.ArrayLike,
                                               npt.ArrayLike,
                                               npt.ArrayLike]:
    x1 = np.linspace(range_x1[0], range_x1[1], range_x1[2])
    x2 = np.linspace(range_x2[0], range_x2[1], range_x2[2])
    x1, x2 = np.meshgrid(x1, x2)
    fx = function([x1, x2])
    return x1, x2, fx


def plot_data(x1: npt.ArrayLike, x2: npt.ArrayLike, fx: npt.ArrayLike) -> None:
    _, ax = plt.subplots()
    levels = np.linspace(np.min(fx), np.max(fx), 30)
    CS = ax.contour(x1, x2, fx, levels=levels)
    ax.clabel(CS, inline=True, fontsize=10)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    plt.show()


RANGE_X1 = (-5, 3, 1000)
RANGE_X2 = (-5, 3, 1000)

# plot the function contour
x1, x2, fx = prep_data(function2, RANGE_X1, RANGE_X2)
plot_data(x1, x2, fx)


# After plotting the results, all the critical points match what is seen on the contour plot
#
