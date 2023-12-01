#!/usr/bin/env python

import numpy as np
import scipy.optimize as opt

import functions as fn
from gradfree import nelder_mead, plot_nm, plot_nm_bfgs


if __name__ == "__main__":
    np.set_printoptions(precision=13, sign=' ', suppress=True)
    x0 = [-1.25, 1.5]
    # 6.2.a
    print(f"6.2.a) Nelder-Mead optimum")
    print("NM conv\tNM fev\tNM it\tNM x*\t\t\t\t\tNM fx*")
    wrapped_f = fn.FevWrapper(fn.bean_f)
    out = nelder_mead(wrapped_f, x0, max_iter=100)
    xopt = out['simplex'][-1][0]
    print(f"{out['success']}\t{wrapped_f.get_fev()}\t{out['iters']}\t{xopt}")
    plot_nm(fn.bean_f, out['simplex'],
            "Nelder-Mead applied to the bean function")

    # setting baseline for part b and c
    res = opt.minimize(fn.bean_f, x0, method='BFGS', jac=fn.bean_df)
    baseline_x = res.x
    baseline_fx = res.fun

    # 6.2.b
    print(f"\n6.2.b) Nelder-Mead and BFGS optimum with noise")
    # not printing the NM opt success cos i have made sure to give enough iterations that it always passes
    print("noise\tNM fev\tNM x*\t\t\t\tNM fx*\t\tBFGS conv\tBFGS f+jev\tBFGS x*\t\t\t\tBFGS fx*")
    np.set_printoptions(precision=8, sign=' ', suppress=True)
    print_dict = {
        'noise': [],
        'nm x': [],
        'bfgs x': [],
        'nm fx': [],
        'bfgs fx': [],
        'nm fev': [],
        'bfgs fev': [],
    }
    # noises = [10**(-exp) for exp in reversed(range(1, 10))]
    noises = [10**(-exp) for exp in [9, 7, 4, 3, 1]]
    for noise in noises:
        print_dict['noise'].append(noise)
        bean_noisy_obj = fn.BeanNoisyPredictable(noise)

        wrapped_f = fn.FevWrapper(bean_noisy_obj.f)
        out = nelder_mead(wrapped_f, x0, max_iter=1000)
        xopt = out['simplex'][-1][0]
        print_dict['nm x'].append(np.abs(xopt.x - baseline_x))
        print_dict['nm fx'].append(abs(xopt.fx - baseline_fx))
        print_dict['nm fev'].append(wrapped_f.get_fev())

        bfgs_progress = [x0]
        res = opt.minimize(bean_noisy_obj.f, x0, jac=bean_noisy_obj.df, method='BFGS',
                           callback=lambda x: bfgs_progress.append(x))
        print_dict['bfgs x'].append(np.abs(res.x - baseline_x))
        print_dict['bfgs fx'].append(abs(res.fun - baseline_fx))
        print_dict['bfgs fev'].append(res.nfev + res.njev)
        print(
            f"{noise:.0e}\t{wrapped_f.get_fev()}\t{xopt.x}\t{xopt.fx: .9f}\t{res.status==0}\t\t{res.nfev+res.njev}\t\t{res.x}\t{res.fun:.8f}")
        plot_nm_bfgs(fn.bean_f, out['simplex'], bfgs_progress,
                     f"Nelder-Mead vs BFGS on the bean function with noise {noise}")

    # print like the table i need in markdown
    # print(f"| noise | {' | '.join(f'{x:.0e}' for x in print_dict['noise'])} |")
    # print(f"| - | {' - |'*len(noises)}")
    # print(
    #     f"| NM x1 | {' | '.join(f'{x[0]:.10e}' for x in print_dict['nm x'])} |")
    # print(
    #     f"| BFGS x1 | {' | '.join(f'{x[0]:.10e}' for x in print_dict['bfgs x'])} |")
    # print(
    #     f"| NM x2 | {' | '.join(f'{x[1]:.10e}' for x in print_dict['nm x'])} |")
    # print(
    #     f"| BFGS x2 | {' | '.join(f'{x[1]:.10e}' for x in print_dict['bfgs x'])} |")
    # print(
    #     f"| NM fx | {' | '.join(f'{x:.10e}' for x in print_dict['nm fx'])} |")
    # print(
    #     f"| BFGS fx | {' | '.join(f'{x:.10e}' for x in print_dict['bfgs fx'])} |")
    # print(f"| NM fev | {' | '.join(f'{x}' for x in print_dict['nm fev'])} |")
    # print(
    #     f"| BFGS fev | {' | '.join(f'{x}' for x in print_dict['bfgs fev'])} |")

    # 6.2.c
    print(f"\n6.2.c) Nelder-Mead optimum with checkerboard steps")
    # not printing the NM opt success cos i have made sure to give enough iterations that it always passes
    print("step\tNM fev\tNM x*\t\t\t\t\tNM fx*\t\t\tBFGS conv\tBFGS f+jev\tBFGS x*\t\t\t\t\tBFGS fx*")

    np.set_printoptions(precision=13, sign=' ', suppress=True)
    print_dict = {
        'step': [],
        'nm x': [],
        'bfgs x': [],
        'nm fx': [],
        'bfgs fx': [],
        'nm fev': [],
        'bfgs fev': [],
        'bfgs conv': [],
    }
    # steps = [0.5*mult for mult in range(1, 10)]
    steps = [4, 2, 1, .5]
    for step in steps:
        print_dict['step'].append(step)

        def bean_check_f(x): return fn.bean_check_f(x, step)
        wrapped_f = fn.FevWrapper(bean_check_f)
        out = nelder_mead(wrapped_f, x0, max_iter=1000)
        xopt = out['simplex'][-1][0]
        print_dict['nm x'].append(np.abs(xopt.x - baseline_x))
        print_dict['nm fx'].append(abs(xopt.fx - baseline_fx))
        print_dict['nm fev'].append(wrapped_f.get_fev())

        def bean_check_f(x): return fn.bean_check_f(x, step)
        bfgs_progress = [x0]
        res = opt.minimize(bean_check_f, x0, jac=fn.bean_check_df, method='BFGS',
                           callback=lambda x: bfgs_progress.append(x))

        print_dict['bfgs x'].append(np.abs(res.x - baseline_x))
        print_dict['bfgs fx'].append(abs(res.fun - baseline_fx))
        print_dict['bfgs fev'].append(res.nfev + res.njev)
        print_dict['bfgs conv'].append(res.status == 0)

        print(
            f"{step}\t{wrapped_f.get_fev()}\t{xopt}\t{res.status==0}\t\t{res.nfev+res.njev}\t\t{res.x}\t{res.fun}")
        plot_nm_bfgs(bean_check_f, out['simplex'], bfgs_progress,
                     f"Nelder-Mead vs BFGS on the bean function with step {step}")

    # print like the table i need in markdown
    # print(f"| step | {' | '.join(f'{x}' for x in print_dict['step'])} |")
    # print(f"| - | {' - |'*len(steps)}")
    # print(
    #     f"| NM x1 | {' | '.join(f'{x[0]:.10e}' for x in print_dict['nm x'])} |")
    # print(
    #     f"| BFGS x1 | {' | '.join(f'{x[0]:.10e}' for x in print_dict['bfgs x'])} |")
    # print(
    #     f"| NM x2 | {' | '.join(f'{x[1]:.10e}' for x in print_dict['nm x'])} |")
    # print(
    #     f"| BFGS x2 | {' | '.join(f'{x[1]:.10e}' for x in print_dict['bfgs x'])} |")
    # print(
    #     f"| NM fx | {' | '.join(f'{x:.10e}' for x in print_dict['nm fx'])} |")
    # print(
    #     f"| BFGS fx | {' | '.join(f'{x:.10e}' for x in print_dict['bfgs fx'])} |")
    # print(f"| NM fev | {' | '.join(f'{x}' for x in print_dict['nm fev'])} |")
    # print(
    #     f"| BFGS fev | {' | '.join(f'{x}' for x in print_dict['bfgs fev'])} |")
    # print(
    #     f"| BFGS conv | {' | '.join(f'{x}' for x in print_dict['bfgs conv'])} |")

    # 6.2.d
    x0 = [1, 1, 1]
    print(f"\n6.2.d) Nelder-Mead and BFGS optimum")
    print("Method\tconv\tfev\tx*\t\t\t\t\tfx*")
    wrapped_f = fn.FevWrapper(fn.p62d_f)
    out = nelder_mead(wrapped_f, x0, max_iter=1000)
    xopt = out['simplex'][-1][0]

    bfgs_progress = [x0]
    res = opt.minimize(fn.p62d_f, x0, jac=fn.p62d_df, method='BFGS',
                       callback=lambda xk: bfgs_progress.append(xk))
    print(
        f"NM\t{out['success']}\t{wrapped_f.get_fev()}\t{' '.join(f'{x: .5e}' for x in xopt.x)}\t{xopt.fx:.5e}")
    print(
        f"BFGS\t{res.status==0}\t{res.nfev+res.njev}\t{' '.join(f'{x: .5e}' for x in res.x)}\t{res.fun:.5e}")
