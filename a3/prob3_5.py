import matplotlib.pyplot as plt
import numpy as np
import not_tests_uncon_optimizer as tw


def prep_data(function, range_x1, range_x2):
    x1 = np.linspace(range_x1[0], range_x1[1], range_x1[2])
    x2 = np.linspace(range_x2[0], range_x2[1], range_x2[2])
    x1, x2 = np.meshgrid(x1, x2)
    fx = function([x1, x2])
    return x1, x2, fx


def plot_data(x1, x2, fx, guesses, title):
    _, ax = plt.subplots()
    levels = np.linspace(np.min(fx), np.max(fx), 30)
    CS = ax.contour(x1, x2, fx, levels=levels)
    ax.clabel(CS, inline=True, fontsize=10)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    x, y = guesses.T
    ax.plot(x, y, '-o')
    plt.title(f'{title}')
    plt.show()


def plot_path(function, guesses, title):
    x, y = guesses.T
    RANGE_X1 = (min(x)-0.5, max(x)+0.5, 1000)
    RANGE_X2 = (min(y)-0.5, max(y)+0.5, 1000)
    x1, x2, fx = prep_data(function, RANGE_X1, RANGE_X2)
    plot_data(x1, x2, fx, guesses, title)


if __name__ == '__main__':
    testwrapper = tw.TestsYouMustPass()
    print("\n\nBFGS with backtracking line search")
    testwrapper.set_options({"direction": "bfgs", "linsearch": "bracket"})

    testwrapper.test_slanted_quad()
    output = testwrapper.get_output()
    plot_path(tw.slanted_quad, output["guesses"], output["func_in"])

    testwrapper.test_bean()
    output = testwrapper.get_output()
    plot_path(tw.bean, output["guesses"], output["func_in"])

    testwrapper.test_rosenbrock()
    output = testwrapper.get_output()
    plot_path(tw.rosenbrock, output["guesses"], output["func_in"])
