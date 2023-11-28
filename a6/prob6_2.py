#!/usr/bin/env python

import functions as fn
from gradfree import nelder_mead, plot_nelder_mead

if __name__ == "__main__":
    x0 = [-1, 1.5]
    opt, simplex = nelder_mead(fn.bean, x0, max_iter=100)
    print(f"Nelder-Mead optimum: {opt}")
    plot_nelder_mead(fn.bean, simplex,
                     "Nelder-Mead applied to the bean function")
