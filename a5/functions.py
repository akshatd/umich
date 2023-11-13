#!/usr/bin/env python
import numpy as np
import math
import scipy.optimize as opt

# problem 5.1


class ADData:
    # good reference: https://kenndanielso.github.io/mlrefined/blog_posts/3_Automatic_differentiation/3_4_AD_forward_mode.html
    # Algorithmic Differentiation Data type
    def __init__(self, fx, dx=1):
        # dx of x is 1 by default, will help build other dx's on top of this
        self.fx = fx
        self.dx = dx

# overloads for AD, remember chain rule in dx for unary ops


def ad_exp(x: ADData) -> ADData:
    return ADData(np.exp(x.fx), x.dx * np.exp(x.fx))


def ad_sin(x: ADData) -> ADData:
    return ADData(np.sin(x.fx), x.dx * np.cos(x.fx))


def ad_cos(x: ADData) -> ADData:
    return ADData(np.cos(x.fx), x.dx * -np.sin(x.fx))


def ad_pow(x: ADData, pow) -> ADData:
    return ADData(x.fx**pow, x.dx * pow * x.fx**(pow-1))


def ad_add(x1: ADData, x2: ADData) -> ADData:
    return ADData(x1.fx + x2.fx, x1.dx + x2.dx)


def ad_mul(x1: ADData, x2: ADData) -> ADData:
    return ADData(x1.fx * x2.fx, x1.fx*x2.dx + x2.fx*x1.dx)


def p51_f(x):
    return np.exp(x)/(np.sqrt(np.sin(x)**3 + np.cos(x)**3))


def p51_f_ad(x: ADData) -> ADData:
    return ad_mul(ad_exp(x), ad_pow(ad_pow(ad_add(ad_pow(ad_sin(x), 3), ad_pow(ad_cos(x), 3)), 1/2), -1))


# problem 5.2

ECCENTRICITY = 0.7  # e, eccentricity


def kepler_f(E: float, M: float) -> float:
    # kepler's equation: E − e sin(E) = M;
    return E - ECCENTRICITY*np.sin(E) - M


def kepler_df(E: float) -> float:
    # kepler's equation's residual differentiated wrt to E (eccentric anomaly)
    # 1 - e cos(E)
    return 1.0 - ECCENTRICITY*np.cos(E)


def p52_dfdm(E):
    # from UDE
    return 1/(1-ECCENTRICITY*np.cos(E)) - 1


def p52_f(E, M):
    # from UDE
    return E - M


if __name__ == "__main__":
    print(f"grad of p51_f = {np.gradient(p51_f)}")
