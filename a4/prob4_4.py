import numpy as np
import matplotlib.pyplot as plt


def plot_constrained_opt(fx, constr1, guesses, title):
    plot_spread = 3
    # def plot_constrained_opt(fx, opt, title):
    x1, x2 = guesses[-1]
    range_x1 = np.linspace(x1-plot_spread, x1+plot_spread, 1000)
    range_x2 = np.linspace(x2-plot_spread, x2+plot_spread, 1000)
    mesh_x1, mesh_x2 = np.meshgrid(range_x1, range_x2)
    data = fx([mesh_x1, mesh_x2])
    data_constr1 = constr1([mesh_x1, mesh_x2])
    _, ax = plt.subplots()
    levels = np.linspace(np.min(data), np.max(data), 30)
    ax.contour(mesh_x1, mesh_x2, data, levels=levels)
    # ax.contour(mesh_x1, mesh_x2, data)
    # ax.contourf(
    #     mesh_x1, mesh_x2, data_constr1, levels=[0, 22263044], colors='r')
    ax.contour(mesh_x1, mesh_x2, data_constr1, levels=[0], colors='k')

    x, y = np.array(guesses).T
    ax.plot(x, y, '-o')
    ax.annotate("optimum", xy=(x1, x2))
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    plt.title(f'{title}')
    plt.show()


def pf_5_4(x):
    return x[0] + 2*x[1]

# plotting


def ph_5_4(x):
    h1 = 1/4*x[0]**2 + x[1]**2 - 1

    return h1


def f_5_4(x):
    return float(x[0] + 2*x[1]), np.array([1, 2])

# equality constraints


def h_5_4(x):
    h1 = 1/4*x[0]**2 + x[1]**2 - 1
    dx_h1 = np.array([1/2*x[0], 2*x[1]])

    return np.array([h1]), np.array([dx_h1])


def QNSQP(x0, tol_opt, tol_feas, func, func_h, uh):
    a_init = 1
    f, dx_f = func(x0)
    dx_f_prev = dx_f
    h, dx_h = func_h(x0)
    nx = len(x0)
    # nh = len
    lambdas = np.zeros(h.shape)
    dx_lagr = dx_f + dx_h.T@lambdas
    x_k = x0
    x_k_prev = x_k
    infnorm_lagr = np.linalg.norm(dx_lagr, np.inf)
    infnorm_h = np.linalg.norm(h, np.inf)
    k = 0

    guesses = [x_k]
    print(f"SQP start, lambda:{lambdas} guess:{x_k}")

    while (infnorm_lagr > tol_opt or infnorm_h > tol_feas) and k < 3:
        if k == 0 or np.dot(dx_f, dx_f_prev) > 10:
            # hess_lagr = 1/np.linalg.norm(dx_f) * np.identity(len(dx_f_prev))
            hess_lagr = np.identity(nx)
        else:
            # 5.91
            s_k = x_k - x_k_prev
            # 5.48
            dx_lagr = dx_f + dx_h.T@lambdas
            dx_lagr_prev = dx_f_prev + dx_h_prev.T@lambdas
            y_k = dx_lagr - dx_lagr_prev
            sty = s_k.T@y_k
            stHLs = s_k.T@hess_lagr@s_k
            if sty < 0.2 * stHLs:
                theta_k = (0.8 * stHLs) / (stHLs - sty)
            else:
                theta_k = 1
            r_k = theta_k*y_k + (1-theta_k)*hess_lagr@s_k
            hess_lagr = hess_lagr - (np.outer(hess_lagr@s_k, s_k)@hess_lagr) / (
                s_k.T@hess_lagr@s_k) + (np.outer(r_k, r_k))/(r_k.T@s_k)

        # solve QP subproblem for p_x,p_lambda
        # hess_lagr dh.T   | p_x      | -dx_lagr
        # dh        0      | p_lambda | -h
        col0 = np.vstack((hess_lagr, dx_h))
        col1 = np.vstack(
            (dx_h.T, np.zeros((dx_h.shape[0], dx_h.shape[0]))))
        lhs = np.hstack((col0, col1))

        rhs = np.hstack((-dx_lagr, -h))
        sol = np.linalg.solve(lhs, rhs)
        p_x = sol[0:nx]
        p_lambda = sol[nx:]

        lambdas += p_lambda
        a = linsearch_bktrk_constr(func, x_k, p_x, f, np.dot(dx_f, p_x),
                                   a_init, 1e-4, 0.5, func_h, uh)
        x_k_prev = x_k
        x_k = x_k + a*p_x
        print(f"SQP k:{k}, lambda:{lambdas} guess:{x_k}")
        guesses.append(x_k)
        dx_f_prev = dx_f
        f, dx_f = func(x_k)
        dx_h_prev = dx_h
        h, dx_h = func_h(x_k)
        dx_lagr = dx_f + dx_h.T@lambdas

        infnorm_lagr = np.linalg.norm(dx_lagr, np.inf)
        infnorm_h = np.linalg.norm(h, np.inf)
        k += 1
    return guesses


def linsearch_bktrk_constr(func, guess, dir, phi_0, dphi_0, step_init, suffdec, bktrk, func_h, uh):
    # backtracking line search
    step = step_init
    # if constr is not None:
    #     while constr(guess + dir*step) > 0:
    #         step = bktrk * step

    # phi_step, _, df_step = xphi(func, guess, dir, step)
    phi_step = merit_fn(func, guess, dir, step, func_h, uh)
    print(f"** backtrack ** step: {step}, phi_step: {phi_step}")
    # steps = [step]
    while phi_step > (phi_0 + suffdec * step * dphi_0):
        step = bktrk * step
        # steps.append(step)
        # if constr is not None:
        #     while constr(guess + dir*step) > 0:
        #         step = bktrk * step
        # phi_step, _, df_step = xphi(func, guess, dir, step)
        phi_step = merit_fn(func, guess, dir, step, func_h, uh)
        # print(f"** backtrack ** step: {step}, fx: {phi_step}")
    return step


def merit_fn(f, x0, dir, step, f_h, uh):
    x_step = x0 + dir*step
    h, _ = f_h(x_step)
    fx, _ = f(x_step)
    return fx + uh*np.linalg.norm(h, 1)


if __name__ == "__main__":
    x0 = np.array([2, 1])
    tol_opt = 1e-3
    tol_feas = 1e-3
    uh = 1
    # print(f"fx0 = {f_5_2(x0)}, hx0 = {h_5_2(x0)}")
    guesses = QNSQP(x0, tol_opt, tol_feas, f_5_4, h_5_4, uh)

    plot_constrained_opt(pf_5_4, ph_5_4, guesses,
                         "Ex 4.5 contour with constraints and optimization path")
