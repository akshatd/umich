#!/usr/bin/env python

import numpy as np

import functions as fn
from gradfree import nelder_mead, plot_nelder_mead


if __name__ == "__main__":
    np.set_printoptions(precision=15, sign=' ', suppress=True)
    x0 = [-1.25, 1.5]
    # 6.2.a
    print(f"6.2.a) Nelder-Mead optimum")
    print("iters\tfev\toptimal x\t\t\t\toptimal fx")
    wrapped_f = fn.FevWrapper(fn.bean_f)
    out = nelder_mead(wrapped_f, x0, max_iter=100)
    xopt = out['simplex'][-1][0]
    print(f"{out['iters']}\t{wrapped_f.get_fev()}\t{xopt}")
    plot_nelder_mead(fn.bean_f, out['simplex'],
                     "Nelder-Mead applied to the bean function")

    # 6.2.b
    print(f"\n6.2.b) Nelder-Mead optimum with noise")
    print("noise\titers\tfev\toptimal x\t\t\t\toptimal fx")

    noises = [10**(-exp) for exp in range(1, 10)]
    for noise in noises:
        bean_noisy = fn.BeanNoisyPredictable(noise)
        def bean_noisy_f(x): return bean_noisy.f(x)
        wrapped_f = fn.FevWrapper(bean_noisy_f)
        out = nelder_mead(wrapped_f, x0, max_iter=100)
        xopt = out['simplex'][-1][0]
        print(f"{noise}\t{out['iters']}\t{wrapped_f.get_fev()}\t{xopt}")
        plot_nelder_mead(fn.bean_f, out['simplex'],
                         f"Nelder-Mead applied to the bean function with noise {noise}")

    # 6.2.c
    print(f"\n6.2.c) Nelder-Mead optimum with checkerboard steps")
    print("step\titers\toptimal x\t\t\t\toptimal fx")

    steps = [0.5*mult for mult in range(1, 10)]
    for step in steps:
        def bean_check(x): return fn.bean_check_f(x, step)
        wrapped_f = fn.FevWrapper(bean_check)
        out = nelder_mead(wrapped_f, x0, max_iter=1000)
        xopt = out['simplex'][-1][0]
        print(f"{step}\t{out['iters']}\t{wrapped_f.get_fev()}\t{xopt}")
        plot_nelder_mead(bean_check, out['simplex'],
                         f"Nelder-Mead applied to the bean function with step {step}")
