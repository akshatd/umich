import numpy as np

from uncon_optimizer import uncon_optimizer
import prob4_2 as prob


# all the funcs must provide gradient!

def constraint_5_4(x):
    return 1/4*x[0]**2 + x[1]**2 - 1

# uh = equality penalty parameter
# ug = inequality penalty parameter


def pen_ext_quad_5_4(x, ug):
    fx = x[0] + 2*x[1]
    d_fx = np.array([1, 2])
    gfx = ug/2*max(0, 1/4*x[0]**2 + x[1]**2 - 1)**2
    d_gfx = np.zeros(2)
    d_gfx[0] = 1/8*ug*x[0]*(x[0]**2 + 4*x[1]**2 - 4)
    d_gfx[1] = 1/2*ug*x[1]*(x[0]**2 + 4*x[1]**2 - 4)
    return fx+gfx, d_fx+d_gfx


def pen_int_5_4(x, ug):
    fx = x[0] + 2*x[1]
    d_fx = np.array([1, 2])
    gfx = ug/2*max(0, 1/4*x[0]**2 + x[1]**2 - 1)**2
    d_gfx = np.zeros(2)
    d_gfx[0] = 1/8*ug*x[0]*(x[0]**2 + 4*x[1]**2 - 4)
    d_gfx[1] = 1/2*ug*x[1]*(x[0]**2 + 4*x[1]**2 - 4)
    return fx+gfx, d_fx+d_gfx


class Penalizer:
    def __init__(self, uh, ug, type):
        self.uh = uh
        self.ug = ug
        self.type = type

    def __call__(self, x):
        if self.type == "ext":
            return pen_ext_quad_5_4(x, self.ug)
        else:
            return pen_int_5_4(x, self.ug)


def con_optimizer(x0, epsilon_g, options=None):
    if options is None:
        options = {}

    if "uh" not in options:
        options["uh"] = 1
    if "ug" not in options:
        options["ug"] = 1
    if "p" not in options:
        options["p"] = 2
    if "pen" not in options:
        options["pen"] = "ext"

    it = 0
    guess = x0
    guess_prev = guess

    # f, df = func(guess)
    # df_infnorm = np.linalg.norm(df, np.inf)
    # for direction
    # df_prev = df
    # dir_prev = dir_steepdesc(df)
    # inv_hess = 1/np.linalg.norm(df) * np.identity(len(x0))

    uh = options['uh']
    ug = options['ug']

    # lists to keep track of function values
    # infnorm = [df_infnorm]
    guesses = [guess]
    while abs(constraint_5_4(guess)) > epsilon_g:
        func_pen = Penalizer(uh, ug, options["pen"])
        guess, f, output = uncon_optimizer(func_pen, guess_prev, epsilon_g)
        print(ug, guess, abs(constraint_5_4(guess)))
        guesses.append(guess)
        uh = options["p"]*uh
        ug = options["p"]*ug
        guess_prev = guess
        it += 1


if __name__ == "__main__":
    x0 = np.array([0, 0])
    epsilon_g = 10e-6
    con_optimizer(x0, epsilon_g)
