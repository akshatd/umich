#!/usr/bin/env python

import functions as fn
from gradfree import nelder_mead, plot_nelder_mead

if __name__ == "__main__":
    x0 = [-1, 1.5]
    # 6.2.a
    out = nelder_mead(fn.bean, x0, max_iter=1000)
    xopt = out['simplex'][-1][0]
    print(f"6.2.a) Nelder-Mead optimum in {out['iters']} iterations: {xopt}")
    plot_nelder_mead(fn.bean, out['simplex'],
                     "Nelder-Mead applied to the bean function")

    # 6.2.b
    noises = [10**(-exp) for exp in range(1, 10)]
    for noise in noises:
        out = nelder_mead(lambda x: fn.noisy_bean(x, noise), x0, max_iter=100)
        xopt = out['simplex'][-1][0]
        print(
            f"6.2.b) Nelder-Mead optimum in {out['iters']} iterations with noise {noise}: {xopt}")
        plot_nelder_mead(fn.bean, out['simplex'],
                         f"Nelder-Mead applied to the bean function with noise {noise}")
