#!/usr/bin/env python

import numpy as np

import functions as fn
from gradfree import nelder_mead, plot_nelder_mead


if __name__ == "__main__":
    np.set_printoptions(precision=15, sign=' ', suppress=True)
    x0 = [-1.25, 1.5]
    # 6.2.a
    print(f"6.2.a) Nelder-Mead optimum")
    print("iters\toptimal x\t\t\t\toptimal fx")
    out = nelder_mead(fn.bean, x0, max_iter=100)
    xopt = out['simplex'][-1][0]
    print(f"{out['iters']}\t{xopt}")
    plot_nelder_mead(fn.bean, out['simplex'],
                     "Nelder-Mead applied to the bean function")

    # 6.2.b
    print(f"\n6.2.b) Nelder-Mead optimum with noise")
    print("noise\titers\toptimal x\t\t\t\toptimal fx")

    noises = [10**(-exp) for exp in range(1, 10)]
    for noise in noises:
        def bean_noisy(x): return fn.bean_noisy(x, noise)
        out = nelder_mead(bean_noisy, x0, max_iter=100)
        xopt = out['simplex'][-1][0]
        print(f"{noise}\t{out['iters']}\t{xopt}")
        plot_nelder_mead(bean_noisy, out['simplex'],
                         f"Nelder-Mead applied to the bean function with noise {noise}")

    # 6.2.c
    print(f"\n6.2.c) Nelder-Mead optimum with checkerboard steps")
    print("step\titers\toptimal x\t\t\t\toptimal fx")

    steps = [0.5*mult for mult in range(1, 10)]
    for step in steps:
        def bean_check(x): return fn.bean_check(x, step)
        out = nelder_mead(bean_check, x0, max_iter=100)
        xopt = out['simplex'][-1][0]
        print(f"{step}\t{out['iters']}\t{xopt}")
        plot_nelder_mead(bean_check, out['simplex'],
                         f"Nelder-Mead applied to the bean function with step {step}")
