import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

import not_tests_uncon_optimizer as tw


def plot_iters(x, y1, y2):
    plt.plot(x, y1, label="My BFGS")
    plt.plot(x, y2, label="Scipy")
    plt.legend()
    plt.xlabel("Dimensions")
    plt.ylabel("Iterations")
    plt.show()


if __name__ == '__main__':
    testwrapper = tw.TestsYouMustPass()

    print("\n\nBFGS with backtracking line search")
    testwrapper.set_options({"direction": "bfgs", "linsearch": "bracket"})
    dimensions = [2**i for i in range(1, 9)]
    my_iters = []
    scipy_iters = []
    for dims in dimensions:
        print(f"\n\n** Testing {dims} dimensions **")

        tw.set_dims(dims)
        testwrapper.test_rosenbrock_nd()
        output = testwrapper.get_output()
        my_iters.append(output["iterations"])
        # print(f"my iters: {output['iterations']}")

        rosenbrock_x0 = np.zeros(dims)
        res = minimize(tw.func_rosenbrock_nd, rosenbrock_x0, jac=True)
        scipy_iters.append(res.nit)
        # print(f"scipy iters: {res.nit}")

    plot_iters(dimensions, my_iters, scipy_iters)
