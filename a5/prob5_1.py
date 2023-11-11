#!/usr/bin/env python
import math
import numpy as np
import functions as fn
import plots


def finite_diff_fwd(f, x, h):
    return (f(x + h) - f(x))/h


def finite_diff_ctr(f, x, h):
    return (f(x+h) - f(x-h))/(2*h)


def complex_step(f, x, h):
    return np.imag(f(complex(x, h)))/h


if __name__ == "__main__":
    print("Problem 5.1.a")

    steps = [10**-s for s in range(1, 25)]
    # steps = [10**-s for s in range(1, 325)]
    x = 1.5
    # fx_exact = 4.4977800539461619
    dfx_exact = 4.0534278938986201
    # print(f"Exact: {fx_exact} \t \t {dfx_exact}")
    err_findiff_fwd = []
    err_findiff_ctr = []
    err_cplx = []
    for h in steps:
        # print(f"{h} \t {finite_diff_fwd(fn.p51_f, x, h)} \t {finite_diff_ctr(fn.p51_f, x, h)} \t {complex_step(fn.p51_f, x, h)}")
        err_findiff_fwd.append(finite_diff_fwd(fn.p51_f, x, h))
        err_findiff_ctr.append(finite_diff_ctr(fn.p51_f, x, h))
        err_cplx.append(complex_step(fn.p51_f, x, h))

    err_findiff_fwd = np.array(err_findiff_fwd)
    err_findiff_ctr = np.array(err_findiff_ctr)
    err_cplx = np.array(err_cplx)

    err_findiff_fwd = np.abs(err_findiff_fwd - dfx_exact)
    err_findiff_ctr = np.abs(err_findiff_ctr - dfx_exact)
    err_cplx = np.abs(err_cplx - dfx_exact)
    err_cplx = np.where(err_cplx == 0, 1e-16, err_cplx)

    print(
        f"Optimal step size:\n- Forward difference: {math.ulp(fn.p51_f(x))**(1/2)}\n- Central difference: {math.ulp(fn.p51_f(x))**(1/3)}")

    plots.plot_step_error(
        err_findiff_fwd, err_findiff_ctr, err_cplx, steps, "(Realistic step size) Complex-step accuracy compared with ﬁnite differences")
