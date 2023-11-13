#!/usr/bin/env python

import functions as fn
from prob5_1 import finite_diff_fwd


def newton_iter(f, df, x0: float, diff_stop: float, max_iters: int) -> (list[int], list[float], list[float]):
    iter_list = []
    value_list = []
    diff_list = []
    diff = 1
    iters = 0
    x = x0
    while (abs(diff) > diff_stop and iters < max_iters):
        iters += 1
        x_next = x - f(x) / df(x)
        diff = x - x_next
        iter_list.append(iters)
        value_list.append(x)
        diff_list.append(diff)
        x = x_next
    return iter_list, value_list, diff_list


def p52_f(M):
    def f(E): return fn.kepler_f(E, M)
    def df(E): return fn.kepler_df(E)

    NEWTON_DIFF = 1e-6
    NEWTON_MAX_ITERS = 1000

    x0 = 1  # initial guess for E
    _, values, _ = newton_iter(f, df, x0, NEWTON_DIFF, NEWTON_MAX_ITERS)
    E = values[-1]

    return fn.p52_f(E, M)


def p52_df(M):
    def f(E): return fn.kepler_f(E, M)
    def df(E): return fn.kepler_df(E)

    NEWTON_DIFF = 1e-6
    NEWTON_MAX_ITERS = 1000

    x0 = 1  # initial guess for E
    _, values, _ = newton_iter(f, df, x0, NEWTON_DIFF, NEWTON_MAX_ITERS)
    E = values[-1]

    return fn.p52_dfdm(E)


if __name__ == "__main__":
    finite_diff_h = 1e-07
    for M in [0.5, 1, 1.5, 2, 3]:
        print(
            f"at M={M}, df/dM is:\n- UDE:\t{p52_df(M)}\n- FD:\t{finite_diff_fwd(p52_f, M, finite_diff_h)}")
