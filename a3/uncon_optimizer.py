"""
This is a template for Assignment 3: unconstrained optimization

You can (and should) call other functions or import functions from other files,
but make sure you do not change the function signature (i.e., function name `uncon_optimizer`, inputs, and outputs) in this file.
The autograder will import `uncon_optimizer` from this file. If you change the function signature, the autograder will fail.
"""

import numpy as np


def uncon_optimizer(func, x0, epsilon_g, options=None):
    """An algorithm for unconstrained optimization.

    Parameters
    ----------
    func : function handle
        Function handle to a function of the form: f, g = func(x)
        where f is the function value and g is a numpy array containing
        the gradient. x are design variables only.
    x0 : ndarray
        Starting point
    epsilon_g : float
        Convergence tolerance.  you should terminate when
        np.max(np.abs(g)) <= epsilon_g.  (the infinity norm of the gradient)
    options : dict
        A dictionary containing options.  You can use this to try out different
        algorithm choices.  I will not pass anything in on autograder,
        so if the input is None you should setup some defaults.

    Returns
    -------
    xopt : ndarray
        The optimal solution
    fopt : float
        The corresponding optimal function value
    output : dictionary
        Other miscelaneous outputs that you might want, for example an array
        containing a convergence metric at each iteration.

        `output` must includes the alias, which will be used for mini-competition for extra credit.
        Do not use your real name or uniqname as an alias.
        This alias will be used to show the top-performing optimizers *anonymously*.
    """

    # TODO: set your alias for mini-competition here
    output = {}
    output['alias'] = 'akshatdy'

    if options is None:
        # TODO: set default options here.
        # You can pass any options from your subproblem runscripts, but the autograder will not pass any options.
        # Therefore, you should sse the  defaults here for how you want me to run it on the autograder.
        options = {}
        options["direction"] = "bfgs"
        options["linsearch"] = "bracket"
        options["step_init"] = 1
        options["suffdec"] = 1e-4
        options["bktrk"] = 0.7
        options["suffcur"] = 0.9
        options["stepinc"] = 2

    # TODO: Your code goes here!
    it = 0
    guess = x0
    guess_prev = guess
    step = options["step_init"]

    f, df = func(guess)
    df_prev = df

    # for direction
    dir_prev = dir_steepdesc(df)

    inv_hess_prev = 1/np.linalg.norm(df) * np.identity(len(x0))

    # for line search
    while np.linalg.norm(df, np.inf) > epsilon_g:
        print(f"it: {it}, step: {step}, guess: {guess}, f: {f}, df: {df}")
        dir, inv_hess_prev = get_dir(
            options["direction"], df, df_prev, it, dir_prev, guess, guess_prev, inv_hess_prev)
        step_init = step*(np.dot(df_prev, dir_prev))/(np.dot(df, dir))
        step = get_step(options["linsearch"], func, guess, dir, step_init,
                        options["suffdec"], options["bktrk"], options["suffcur"], options["stepinc"])

        guess_prev = guess
        guess = guess + step * dir
        df_prev = df
        dir_prev = dir

        f, df = func(guess)
        it += 1

    return guess, f, output

# direction functions


def get_dir(dir_option, df, df_prev, it, dir_prev, x, x_prev, inv_hess_prev):
    if dir_option == "steepdesc":
        return dir_steepdesc(df), 0
    elif dir_option == "conjgrad":
        return dir_conjgrad(df,  df_prev, it, dir_prev), 0
    # elif dir_option == "newton":
    #     return dir_newton(f, x0)
    elif dir_option == "bfgs":
        return dir_bfgs(df, df_prev, it, dir_prev, x, x_prev, inv_hess_prev)
    else:
        return dir_steepdesc(df), 0


def dir_steepdesc(df):
    return -df/(np.linalg.norm(df))


def dir_conjgrad(df, df_prev, it, dir_prev):
    if it == 0:
        return -(df/(np.linalg.norm(df)))
    else:
        return -(df/(np.linalg.norm(df))) + (max(0, conjgrad_bias(df, df_prev)) * dir_prev)


def conjgrad_bias(df, df_prev):
    # return np.dot(df, df)/np.dot(df_prev, df_prev) # fletcher
    return np.dot(df, (df-df_prev))/np.dot(df_prev, df_prev)  # polak


# def dir_newton():
#     pass


def dir_bfgs(df, df_prev, it, dir_prev, x, x_prev, inv_hess_prev):
    id = np.identity(len(dir_prev))
    if it == 0 or np.dot(df, dir_prev):
        inv_hess = 1/np.linalg.norm(df) * id
    else:
        s = x - x_prev
        y = df - df_prev
        sigma = 1/(np.dot(s, y))
        id - sigma*np.outer(s, y)
        inv_hess = (id - sigma*np.outer(s, y)) * inv_hess_prev * \
            (id - sigma*np.outer(y, s)) + (sigma * np.outer(s, s))
    return -np.matmul(inv_hess, df), inv_hess


# line search functions

def get_step(lin_option, func, x, dir, step_init, suffdec, bktrk, suffcur, stepinc):
    if lin_option == "backtrack":
        return linsearch_bktrk(func, x, dir, step_init, suffdec, bktrk)
    elif lin_option == "bracket":
        return linsearch_bracket(func, x, dir, step_init, suffdec, suffcur, stepinc)
    else:
        return linsearch_bktrk(func, x, dir, step_init, suffdec, bktrk)


def linsearch_bktrk(func, guess, dir, step_init, suffdec, bktrk):
    # backtracking line search
    step = step_init
    # steps = [step_init]
    # phi_0 = phi(f, guess, dir, 0)
    # dphi_0 = dphi(df, guess, dir, 0)
    phi_0, dphi_0 = xphi(func, guess, dir, 0)
    phi_step, _ = xphi(func, guess, dir, step)
    # phi_list = [phi_step]
    print(f"** pinpoint ** step: {step}, fx: {phi_step}")
    while phi_step > (phi_0 + suffdec * step * dphi_0):
        step = bktrk * step
        phi_step, _ = xphi(func, guess, dir, step)
        print(f"** pinpoint ** step: {step}, fx: {phi_step}")
        # steps.append(step)
        # phi_list.append(phi_step)
    return step


# bracketing
def linsearch_bracket(func, guess, dir, step_init, suffdec, suffcur, stepinc):
    # phi_0 = phi(f, guess, dir, 0)
    # dphi_0 = dphi(df, guess, dir, 0)
    phi_0, dphi_0 = xphi(func, guess, dir, 0)
    step_1 = 0
    step_2 = step_init
    phi_1 = phi_0
    first = True
    while True:
        # phi_2 = phi(f, guess, dir, step_2)
        # dphi_2 = dphi(df, guess, dir, step_2)
        phi_2, dphi_2 = xphi(func, guess, dir, step_2)
        print(
            f"** bracket ** step_1: {step_1}, step_2: {step_2}, phi_1: {phi_1}, phi_2: {phi_2}")
        if (phi_2 > phi_0 + suffdec * step_2 * phi_0) or (not first and phi_2 > phi_1):
            # the end of the bracket is above the start
            step = pinpoint(func, guess, dir, step_1, step_2, suffdec, suffcur)
            # return step, xphi(func, guess, dir, step)
            return step
        if abs(dphi_2) <= -suffcur * dphi_0:
            # the gradient is already low enough, return
            step = step_2
            # return step, xphi(func, guess, dir, step)
            return step
        elif dphi_2 >= 0:
            # the gradient is increasing, can pinpoint
            step = pinpoint(func, guess, dir, step_2, step_1, suffdec, suffcur)
            # return step, xphi(func, guess, dir, step)
            return step

        else:
            # no valid bracket found, move forward and repeat
            step_1 = step_2
            step_2 = stepinc*step_2
        first = False


def pinpoint(func, guess, dir, step_low, step_high, suffdec, suffcur):
    # phi_0 = phi(f, guess, dir, 0)
    # dphi_0 = dphi(df, guess, dir, 0)
    phi_0, dphi_0 = xphi(func, guess, dir, 0)
    # phi_low = phi(f, guess, dir, step_low)
    # dphi_low = dphi(df, guess, dir, step_low)
    phi_low, dphi_low = xphi(func, guess, dir, step_low)
    # phi_high = phi(f, guess, dir, step_high)
    # dphi_high = dphi(df, gues, dir, step_high)
    phi_high, _ = xphi(func, guess, dir, step_high)
    it = 0
    while True:
        # interpolate to find the min
        step = quad_interp_min(step_low, step_high,
                               phi_low, phi_high, dphi_low)
        print(
            f"** pinpoint ** it: {it}, step: {step}, phi_low: {phi_low}, phi_high: {phi_high}")
        # phi_step = phi(f, guess, dir, step)
        # dphi_step = dphi(df, guess, dir, step)
        phi_step, dphi_step = xphi(func, guess, dir, step)
        if (phi_step > phi_0 + suffdec*step*dphi_0) or (phi_step > phi_low):
            # if the interpolated step is higher, make it the new high
            step_high = step
            phi_high = phi_step
            # dphi_high = dphi(df, start, dir, step_high)
        else:
            # if the interpolated step is lower, check its gradient
            if abs(dphi_step) <= -suffcur*dphi_0:
                # the gradient is low enough, exit
                return step
            elif dphi_step * (step_high-step_low) >= 0:
                # step predicts an increase, from here
                # since this is already below phi_0, relocate high to the prev low
                step_high = step_low
            step_low = step
        it += 1

# interpolation


def quad_interp_min(x1, x2, fx1, fx2, d_fx1):
    top = (2*x1*(fx2-fx1)+d_fx1*(x1**2 - x2**2))
    bottom = 2*((fx2-fx1)+d_fx1*(x1-x2))
    interp_min = top/bottom
    # see if ans is in between x1 and x2
    if np.linalg.norm(interp_min) < min(np.linalg.norm(x1), np.linalg.norm(x2)) or np.linalg.norm(interp_min) > max(np.linalg.norm(x1), np.linalg.norm(x2)):
        interp_min = (x2+x1)/2

    print(f"** interp ** x1: {x1}, x2: {x2}, min: {interp_min}")
    return interp_min


def normalized(v):
    return v / np.linalg.norm(v)


def phi(f, start, dir, step):
    # function in a specific direction
    return f(start + dir*step)


def dphi(df, start, dir, step):
    # directional derivative
    # dot prod to know how much the fn is expected to decrease in a particular dir
    return np.dot(df(start + dir*step), dir)


def xphi(f, start, dir, step):
    # function , directional derivative in a specific direction
    phi, dphi = f(start + dir*step)
    return phi, np.dot(dphi, dir)
