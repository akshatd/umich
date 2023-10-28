import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import check_grad, minimize

from uncon_optimizer import uncon_optimizer
import prob4_2 as prob


def plot_constrained_opt(fx, constr1, opt, title):
    plot_spread = 3
    # def plot_constrained_opt(fx, opt, title):
    x1, x2 = opt
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
    # ax.contour(mesh_x1, mesh_x2, data_constr1, levels=[0], colors='k')

    ax.plot(x1, x2, '-o')
    ax.annotate("optimum", xy=(x1, x2))
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    plt.title(f'{title}')
    plt.show()


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
    return x[0] + 2 * x[1] - ug*np.log(-1/4*x[0]**2 - x[1]**2 + 1), [
        1 - (2*ug*x[0] / (x[0]**2 + 4*x[1]**2 - 4)),
        2 - (8*ug*x[1] / (x[0]**2 + 4*x[1]**2 - 4))
    ]


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


def con_optimizer(x0, epsilon_g, options=None, opt_options=None):
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

    uh = options['uh']
    ug = options['ug']

    # lists to keep track of function values
    constr_dist = abs(constraint_5_4(guess))
    constr_dists = [constr_dist]
    guesses = [guess]
    if opt_options is None:
        opt_options = {}
        opt_options = {
            'step_init': 0.5,
            'constraint': constraint_5_4
        }

    while constr_dist > epsilon_g:
        func_pen = Penalizer(uh, ug, options["pen"])
        # print(
        #     f"Constrained Optimizer loop {it} with u:{ug}, guess: {guess}, f: {func_pen(guess)}, constraint dist: {constr_dist}")
        guess, f, output = uncon_optimizer(
            func_pen, guess_prev, epsilon_g, opt_options)
        guesses.append(guess)
        constr_dist = abs(constraint_5_4(guess))
        constr_dists.append(constr_dist)
        uh = options["p"]*uh
        ug = options["p"]*ug
        guess_prev = guess
        it += 1
    return guess


if __name__ == "__main__":
    x0 = np.array([-2, -1])
    epsilon_g = 1e-5
    options = {
        'uh': 1,
        'ug': 0.5,
        'p': 1.8,
        'pen': 'ext'
    }
    opt_options = {
        'step_init': 1,
    }
    print(con_optimizer(x0, epsilon_g, options, opt_options))

    x0 = np.array([-1, 0])
    epsilon_g = 1e-5
    options = {
        'uh': 1,
        'ug': 3,
        'p': 0.5,
        'pen': 'int'
    }
    opt_options = {
        'step_init': 1,
        'linsearch': 'backtrack',
        'constraint': constraint_5_4
    }
    print(con_optimizer(x0, epsilon_g, options, opt_options))
    # plot_constrained_opt(func, constraint_5_4, x0,
    #                      "Contour plot of the cross-sectional area with stress constraints")

    # print(check_grad(func, grad, [0, 0]))
    # print(check_grad(func, grad, [-0.5, 0.5]))
