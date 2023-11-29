#!/usr/bin/env python

import numpy as np
import scipy.optimize as opt

import functions as fn
from gradfree import nelder_mead

if __name__ == "__main__":
    # 6.3.a
    print(f"6.3.a) Nelder-Mead optimum")
    print("dims\tmy NM fev\tNM fx*\t\tScipy NM fev\tScipy NM fx*\tBFGS FD fev\tBFGS FD fx*\tBFGS AG f+jev\tBFGS AG fx*")
    dims = [2, 4, 8, 16, 32, 64, 128]
    # dims = [2, 4, 8, 16]
    for dim in dims:
        x0 = np.zeros(dim)

        # my NM
        wrapped_f = fn.FevWrapper(fn.rosenbrock_nd_f)
        out = nelder_mead(wrapped_f, x0, max_iter=10000)
        xopt = out['simplex'][-1][0]

        # scipy NM
        res_sp_nm = opt.minimize(fn.rosenbrock_nd_f, x0, method='Nelder-Mead')

        # scipy BFGS FD
        res_sp_bfgs_fd = opt.minimize(
            fn.rosenbrock_nd_f, x0, method='BFGS', jac=False)

        # scipy BFGS AG
        res_sp_bfgs_ag = opt.minimize(
            fn.rosenbrock_nd_f, x0, method='BFGS', jac=fn.rosenbrock_nd_df)
        print(
            f"{dim}\t{wrapped_f.get_fev()}\t\t{out['simplex'][-1][0].fx: .5e}\t{res_sp_nm.nfev}\t\t{res_sp_nm.fun: .5e}\t{res_sp_bfgs_fd.nfev}\t\t{res_sp_bfgs_fd.fun: .5e}\t{res_sp_bfgs_ag.nfev+res_sp_bfgs_ag.njev}\t\t{res_sp_bfgs_ag.fun: .5e}")
