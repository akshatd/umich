#!/usr/bin/env python
# coding: utf-8

# # AE588 Assignment 1
# ### 1.1

# In[13]:


# import required modules

from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


# In[14]:


# define constants
# RANGE = (5, 10, 0.1)
RANGE = (-20, 10, 0.1)


# In[15]:


# function from the problem
def function1(x: float) -> float:
    return 1 / 12 * pow(x, 4) + pow(x, 3) - 16 * pow(x, 2) + 4 * x + 12


# In[16]:


# another function to prepare the data that is going to be plotted
def prep_data(function: Callable[[float],
                                 float],
              range: tuple[float,
                           float,
                           float]) -> tuple[list[float],
                                            list[float]]:
    data: tuple[list[float], list[float]] = ([], [])
    for x in np.arange(range[0], range[1], range[2]):
        data[0].append(x)
        data[1].append(function(x))
    return data


# In[17]:


# simple function to plot data
def plot_data(data: tuple[list[float], list[float]]) -> None:
    plt.plot(data[0], data[1])
    plt.xticks(np.linspace(min(data[0]), max(data[0]), 15))
    plt.yticks(np.linspace(min(data[1]), max(data[1]), 20))
    plt.show()


# In[18]:


# main function so this can run outside of a jupyter notebook
if __name__ == "__main__":
    data = prep_data(function1, RANGE)
    plot_data(data)


# local minimum = -230 at x = 6.5
#
# global minimum = -2810 at x = -15
