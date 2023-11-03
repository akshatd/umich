#!/usr/bin/env python

from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import numpy as np

import functions as fn


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
    ax.contour(mesh_x1, mesh_x2, data, levels=levels)
    ax.contourf(
        mesh_x1, mesh_x2, data_constr1, levels=[0, 22263044], colors='r')
    ax.contour(mesh_x1, mesh_x2, data_constr1, levels=[0], colors='k')
    ax.contourf(
        mesh_x1, mesh_x2, data_constr2, levels=[0, 12888888], colors='r')
    ax.contour(mesh_x1, mesh_x2, data_constr2, levels=[0], colors='k')
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
    solution = fsolve(fn.p42_dL, x_initial_guesses)
    print('The solution of the system is ', solution)

    plot_constrained_opt(fn.p42_f, fn.p42_g1, fn.p42_g2,
                         solution[0:2], "Contour plot of the cross-sectional area with stress constraints")
