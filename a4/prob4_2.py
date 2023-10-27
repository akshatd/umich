from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import numpy as np

h = .25
b = .125
sigma_yield = 200000000
tau_yeild = 116000000
P = 100000
l = 1


def func(x):
    return 2*b*x[0] + h*x[1]


def I(x):
    return (3*x[0] + 16*x[0]**3 + x[1])/768


def constraint1(x):
    return P*l*h/(2*I(x)) - sigma_yield


def constraint2(x):
    return 1.5*P/(h*x[1]) - tau_yeild


def diffeq(vars):
    x1, x2, sigma1, sigma2, s1, s2 = vars
    # s1 = 0
    # s2 = 0
    dx1 = 2*b - 384*sigma1*P*l*h*(3 + 48*x1**2)/(3*x1 + 16*x1**3 + x2)**2
    dx2 = h - 384*sigma1*P*l*h / \
        (3*x1 + 16*x1**3 + x2)**2 - 1.5*sigma2*P/(h*x2**2)
    dsig1 = 384*P*l*h/(3*x1 + 16*x1**3 + x2) - sigma_yield + s1**2
    dsig2 = 1.5*P/(h*x2) - tau_yeild + s2**2
    ds1 = 2*sigma1*s1
    ds2 = 2*sigma2*s2
    return [dx1, dx2, dsig1, dsig2, ds1, ds2]


def plot_constrained_opt(fx, constr1, constr2, opt, title):
    plot_spread = 0.1
    # def plot_constrained_opt(fx, opt, title):
    x1, x2 = opt
    range_x1 = np.linspace(x1-plot_spread*x1, x1+plot_spread*x1, 1000)
    range_x2 = np.linspace(x2-plot_spread*x2, x2+plot_spread*x2, 1000)
    mesh_x1, mesh_x2 = np.meshgrid(range_x1, range_x2)
    data = fx([mesh_x1, mesh_x2])
    data_constr1 = constr1([mesh_x1, mesh_x2])
    data_constr2 = constr2([mesh_x1, mesh_x2])
    _, ax = plt.subplots()
    levels = np.linspace(np.min(data), np.max(data), 30)
    cnt_fx = ax.contour(mesh_x1, mesh_x2, data, levels=levels)
    ax.clabel(cnt_fx, inline=True, fontsize=10)
    cnt_constr1 = ax.contour(mesh_x1, mesh_x2, data_constr1, levels=[0])
    ax.clabel(cnt_constr1, inline=True, fontsize=10)
    cnt_constr2 = ax.contour(mesh_x1, mesh_x2, data_constr2, levels=[0])
    ax.clabel(cnt_constr2, inline=True, fontsize=10)
    ax.plot(x1, x2, '-o')
    ax.annotate("optimum", xy=(x1, x2))
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    plt.title(f'{title}')
    plt.show()


if __name__ == "__main__":
    # Initial guesses for variables
    x_initial_guesses = [0.01, 0.01, 0, 0, 0, 0]

    # Use fsolve to solve the system of equations
    solution = fsolve(diffeq, x_initial_guesses)
    print('The solution of the system is ', solution)

    plot_constrained_opt(func, constraint1, constraint2,
                         solution[0:2], "Contour plot of the cross-sectional area with stress constraints")
