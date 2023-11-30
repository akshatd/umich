#!/usr/bin/env python

from matplotlib import pyplot as plt
import numpy as np
import scipy.optimize as opt

import functions as fn
from gradfree import nelder_mead

if __name__ == "__main__":
    # 6.3
    print(f"6.3) Optimums")
    print("dims\tmy NM fev\tNM fx*\t\tScipy NM fev\tScipy NM fx*\tBFGS FD fev\tBFGS FD fx*\tBFGS AG f+jev\tBFGS AG fx*")
    dims = [2, 4, 8, 16, 32, 64]
    # dims = [2, 4, 8, 16, 32, 64, 128]
    # dims = [2, 4, 8, 16]
    print_dict = {
        'dims': [],
        'nm fx': [],
        'scipy nm fx': [],
        'bfgs fd fx': [],
        'bfgs ag fx': [],
        'nm fev': [],
        'scipy nm fev': [],
        'bfgs fd fev': [],
        'bfgs ag fev': [],
        'nm conv': [],
        'scipy nm conv': [],
        'bfgs fd conv': [],
        'bfgs ag conv': [],
    }

    for dim in dims:
        print_dict['dims'].append(dim)
        x0 = np.zeros(dim)

        # my NM
        wrapped_f = fn.FevWrapper(fn.rosenbrock_nd_f)
        out = nelder_mead(wrapped_f, x0, max_iter=10000)
        xopt = out['simplex'][-1][0]
        print_dict['nm fx'].append(xopt.fx)
        print_dict['nm fev'].append(wrapped_f.get_fev())
        print_dict['nm conv'].append(out['success'])

        # scipy NM
        res_sp_nm = opt.minimize(fn.rosenbrock_nd_f, x0, method='Nelder-Mead')
        print_dict['scipy nm fx'].append(res_sp_nm.fun)
        print_dict['scipy nm fev'].append(res_sp_nm.nfev)
        print_dict['scipy nm conv'].append(res_sp_nm.status == 0)

        # scipy BFGS FD
        res_sp_bfgs_fd = opt.minimize(
            fn.rosenbrock_nd_f, x0, method='BFGS', jac=False)
        print_dict['bfgs fd fx'].append(res_sp_bfgs_fd.fun)
        print_dict['bfgs fd fev'].append(res_sp_bfgs_fd.nfev)
        print_dict['bfgs fd conv'].append(res_sp_bfgs_fd.status == 0)

        # scipy BFGS AG
        res_sp_bfgs_ag = opt.minimize(
            fn.rosenbrock_nd_f, x0, method='BFGS', jac=fn.rosenbrock_nd_df)
        print_dict['bfgs ag fx'].append(res_sp_bfgs_ag.fun)
        print_dict['bfgs ag fev'].append(
            res_sp_bfgs_ag.nfev + res_sp_bfgs_ag.njev)
        print_dict['bfgs ag conv'].append(res_sp_bfgs_ag.status == 0)

        print(
            f"{dim}\t{wrapped_f.get_fev()}\t\t{out['simplex'][-1][0].fx: .5e}\t{res_sp_nm.nfev}\t\t{res_sp_nm.fun: .5e}\t{res_sp_bfgs_fd.nfev}\t\t{res_sp_bfgs_fd.fun: .5e}\t{res_sp_bfgs_ag.nfev+res_sp_bfgs_ag.njev}\t\t{res_sp_bfgs_ag.fun: .5e}")

    # plot all the fevs vs dims
    plt.plot(dims, print_dict['nm fev'], label="My Nelder-Mead")
    plt.plot(dims, print_dict['scipy nm fev'], label="Scipy Nelder-Mead")
    plt.plot(dims, print_dict['bfgs fd fev'], label="BFGS Finite Difference")
    plt.plot(dims, print_dict['bfgs ag fev'], label="BFGS Analytical Gradient")
    plt.legend()
    plt.show()

    # print like the table i need in markdown
    # print(f"| dims | {' | '.join(f'{x}' for x in print_dict['dims'])} |")
    # print(f"| - | {' - |'*len(dims)}")
    # print(
    #     f"| NM fx | {' | '.join(f'{x: .3e}' for x in print_dict['nm fx'])} |")
    # print(
    #     f"| scipy NM fx | {' | '.join(f'{x: .3e}' for x in print_dict['scipy nm fx'])} |")
    # print(
    #     f"| BFGS FD fx | {' | '.join(f'{x: .3e}' for x in print_dict['bfgs fd fx'])} |")
    # print(
    #     f"| BFGS AG fx | {' | '.join(f'{x: .3e}' for x in print_dict['bfgs ag fx'])} |")
    # print(f"| NM fev | {' | '.join(f'{x}' for x in print_dict['nm fev'])} |")
    # print(
    #     f"| scipy NM fev | {' | '.join(f'{x}' for x in print_dict['scipy nm fev'])} |")
    # print(
    #     f"| BFGS FD fev | {' | '.join(f'{x}' for x in print_dict['bfgs fd fev'])} |")
    # print(
    #     f"| BFGS AG fev | {' | '.join(f'{x}' for x in print_dict['bfgs ag fev'])} |")
    # print(f"| NM conv | {' | '.join(f'{x}' for x in print_dict['nm conv'])} |")
    # print(
    #     f"| scipy NM conv | {' | '.join(f'{x}' for x in print_dict['scipy nm conv'])} |")
    # print(
    #     f"| BFGS FD conv | {' | '.join(f'{x}' for x in print_dict['bfgs fd conv'])} |")
    # print(
    #     f"| BFGS AG conv | {' | '.join(f'{x}' for x in print_dict['bfgs ag conv'])} |")
