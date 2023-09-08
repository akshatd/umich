# %% [markdown]
# ### 1.1

# %%
# import required modules

from typing import Callable

import matplotlib.pyplot as plt
from numpy import arange

# %%
# define constants
RANGE: tuple[float, float, float] = (-20, 10, 0.1)

# %%
# function from the problem


def function1(x: float) -> float:
    return 1/12*pow(x, 4) + pow(x, 3) - 16*pow(x, 2) + 4*x + 12

# %%
# another function to prepare the data that is going to be plotted


def prep_data(function: Callable[[float], float], range: tuple[float, float, float]) -> tuple[list[float], list[float]]:
    data: tuple[list[float], list[float]] = ([], [])
    for x in arange(range[0], range[1], range[2]):
        data[0].append(x)
        data[1].append(function(x))
    return data

# %%
# simple function to plot data


def plot_data(data: tuple[list[float], list[float]]) -> None:
    plt.plot(data[0], data[1])
    plt.show()


# %%
# main function so this can run outside of a jupyter notebook
if __name__ == "__main__":
    data = prep_data(function1, RANGE)
    plot_data(data)

# %% [markdown]
# From the plot, we can see that the global minimum of the function occurs at -15.25, with a value of -2810
