#!/usr/bin/env python

import numpy as np
import scipy.optimize as opt

import functions as fn
from gradfree import nelder_mead, plot_nm, plot_nm_bfgs


if __name__ == "__main__":
    np.set_printoptions(precision=15, sign=' ', suppress=True)
    x0 = [-1.25, 1.5]
    # 6.2.a
    print(f"6.2.a) Nelder-Mead optimum")
    print("NM iters\tNM fev\tNM x*\t\t\t\t\tNM fx*")
    wrapped_f = fn.FevWrapper(fn.bean_f)
    out = nelder_mead(wrapped_f, x0, max_iter=100)
    xopt = out['simplex'][-1][0]
    print(f"{out['iters']}\t\t{wrapped_f.get_fev()}\t{xopt}")
    plot_nm(fn.bean_f, out['simplex'],
            "Nelder-Mead applied to the bean function")

    # 6.2.b
    print(f"\n6.2.b) Nelder-Mead optimum with noise")
    print("noise\tNM iters\tNM fev\tNM x*\t\t\t\t\tNM fx*\t\t\tBFGS fev\tBFGS x*\t\t\t\t\tBFGS fx*")

    noises = [10**(-exp) for exp in reversed(range(1, 10))]
    for noise in noises:
        bean_noisy_obj = fn.BeanNoisyPredictable(noise)

        def bean_noisy_f(x): return bean_noisy_obj.f(x)
        wrapped_f = fn.FevWrapper(bean_noisy_f)
        out = nelder_mead(wrapped_f, x0, max_iter=100)
        xopt = out['simplex'][-1][0]

        def bean_noisy(x): return bean_noisy_obj.fdf(x)
        bfgs_progress = [x0]
        res = opt.minimize(bean_noisy, x0, jac=True, method='BFGS',
                           callback=lambda xk: bfgs_progress.append(xk))

        print(
            f"{noise}\t{out['iters']}\t\t{wrapped_f.get_fev()}\t{xopt}\t{res.nfev}\t\t{res.x}\t{res.fun}")
        plot_nm_bfgs(fn.bean_f, out['simplex'], bfgs_progress,
                     f"Nelder-Mead vs BFGS on the bean function with noise {noise}")

    # 6.2.c
    print(f"\n6.2.c) Nelder-Mead optimum with checkerboard steps")
    print("step\tNM iters\tNM fev\tNM x*\t\t\t\t\tNM fx*\t\t\tBFGS fev\tBFGS x*\t\t\t\t\tBFGS fx*")

    steps = [0.5*mult for mult in range(1, 10)]
    for step in steps:
        def bean_check_f(x): return fn.bean_check_f(x, step)
        wrapped_f = fn.FevWrapper(bean_check_f)
        out = nelder_mead(wrapped_f, x0, max_iter=1000)
        xopt = out['simplex'][-1][0]

        def bean_check_f(x): return fn.bean_check_f(x, step)
        bfgs_progress = [x0]
        res = opt.minimize(bean_check_f, x0, jac=fn.bean_check_df, method='BFGS',
                           callback=lambda xk: bfgs_progress.append(xk))

        print(
            f"{step}\t{out['iters']}\t\t{wrapped_f.get_fev()}\t{xopt}\t{res.nfev}\t\t{res.x}\t{res.fun}")
        plot_nm_bfgs(bean_check_f, out['simplex'], bfgs_progress,
                     f"Nelder-Mead vs BFGS on the bean function with step {step}")

    # 6.2.d
    x0 = [1, 1, 1]
    print(f"6.2.d) Nelder-Mead and BFGS optimum")
    print("NM iters\tNM fev\tNM x*\t\t\t\t\t\tNM fx*\t\tBFGS fev\tBFGS x*\t\t\t\tBFGS fx*")
    wrapped_f = fn.FevWrapper(fn.p62d_f)
    out = nelder_mead(wrapped_f, x0, max_iter=1000)
    xopt = out['simplex'][-1][0]

    bfgs_progress = [x0]
    res = opt.minimize(fn.p62d_f, x0, jac=fn.p62d_df, method='BFGS',
                       callback=lambda xk: bfgs_progress.append(xk))
    np.set_printoptions(precision=5, sign=' ', suppress=False)
    print(
        f"{out['iters']}\t\t{wrapped_f.get_fev()}\t{xopt.x}\t{xopt.fx:.5e}\t{res.nfev}\t\t{res.x}\t{res.fun:.5e}")
