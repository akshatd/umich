#!/usr/bin/env python
import numpy as np
import math
import scipy.optimize as opt


def p51_f(x):
    return np.exp(x)/(np.sqrt(np.sin(x)**3 + np.cos(x)**3))


if __name__ == "__main__":
    print(f"grad of p51_f = {np.gradient(p51_f)}")
