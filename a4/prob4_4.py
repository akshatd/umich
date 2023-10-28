import numpy as np


def f_5_2(x):
    return float(x[0] + 2*x[1]), np.array([1, 2])


# equality constraints
def h_5_2(x):
    h1 = 1/4*x[0]**2 + x[1]**2 - 1
    dx_h1 = np.array([1/2*x[0], 2*x[1]])

    return np.array([h1]), np.array([dx_h1])


def lagr_5_2(x, lamb, h):
    return f_5_2(x) + lamb.T * np.array([hx(x) for hx in h])


def linsearch_bktrk_constr(func, guess, dir, phi_0, dphi_0, step_init, suffdec, bktrk, func_h, uh):
    # backtracking line search
    step = step_init
    # if constr is not None:
    #     while constr(guess + dir*step) > 0:
    #         step = bktrk * step

    # phi_step, _, df_step = xphi(func, guess, dir, step)
    phi_step = merit_fn(func, guess, dir, step,  func_h, uh)
    print(f"** backtrack ** step: {step}, phi_step: {phi_step}")
    while phi_step > (phi_0 + suffdec * step * dphi_0):
        step = bktrk * step
        # if constr is not None:
        #     while constr(guess + dir*step) > 0:
        #         step = bktrk * step
        # phi_step, _, df_step = xphi(func, guess, dir, step)
        phi_step = merit_fn(func, guess, dir, step, func_h, uh)
        print(f"** backtrack ** step: {step}, fx: {phi_step}")
    return step


def merit_fn(f, x0, dir, step, f_h, uh):
    x_step = x0 + dir*step
    h, _ = f_h(x_step)
    fx, _ = f(x_step)
    return fx + uh*np.linalg.norm(h, 1)


def QNSQP(x0, tol_opt, tol_feas, func, func_h, uh):
    a_init = 1
    f, dx_f = func(x0)
    dx_f_prev = dx_f
    h, dx_h = func_h(x0)
    lambdas = np.zeros(h.shape)
    dx_lagr = dx_f + dx_h.T@lambdas
    guess = x0
    guess_prev = guess
    infnorm_lagr = np.linalg.norm(dx_lagr, np.inf)
    infnorm_h = np.linalg.norm(h, np.inf)
    k = 0
    while infnorm_lagr > tol_opt or infnorm_h > tol_feas:
        if k == 0 or np.dot(dx_f, dx_f_prev) > 10:
            # hess_lagr = 1/np.linalg.norm(dx_f) * np.identity(len(dx_f_prev))
            hess_lagr = np.identity(len(dx_f_prev))
        else:
            # 5.91
            s_k = guess - guess_prev
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
            hess_lagr = hess_lagr_prev - (np.outer(hess_lagr_prev@s_k, s_k)@hess_lagr_prev) / (
                s_k.T@hess_lagr_prev@s_k) + (np.outer(r_k, r_k))/(r_k.T@s_k)

        # solve QP subproblem for p_x,p_lambda
        # hess_lagr dh.T   | p_x      | -dx_lagr
        # dh        0      | p_lambda | -h
        col0 = np.vstack((hess_lagr, dx_h))
        col1 = np.vstack(
            (dx_h.T, np.zeros((dx_h.shape[0], dx_h.shape[0]))))
        lhs = np.hstack((col0, col1))

        rhs = np.hstack((-dx_lagr, -h))
        sol = np.linalg.solve(lhs, rhs)
        p_x = sol[0:len(dx_lagr)]
        p_lambda = sol[len(dx_lagr):]

        lambdas += p_lambda
        a = linsearch_bktrk_constr(func, guess, p_x, f, np.dot(dx_f, p_x),
                                   a_init, 1e-4, 0.5, func_h, uh)
        guess_prev = guess
        guess = guess + a*p_x
        # f_prev = f
        dx_f_prev = dx_f
        f, dx_f = func(guess)
        dx_h_prev = dx_h
        h, dx_h = func_h(guess)
        dx_lagr = dx_f + dx_h.T@lambdas
        hess_lagr_prev = hess_lagr

        infnorm_lagr = np.linalg.norm(dx_lagr, np.inf)
        infnorm_h = np.linalg.norm(h, np.inf)
        k += 1


if __name__ == "__main__":
    x0 = np.array([2, 1])
    tol_opt = 1e-3
    tol_feas = 1e-3
    uh = 1
    print(f"fx0 = {f_5_2(x0)}, hx0 = {h_5_2(x0)}")
    QNSQP(x0, tol_opt, tol_feas, f_5_2, h_5_2, uh)
