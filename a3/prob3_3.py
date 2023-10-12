import numpy as np
from scipy.optimize import minimize

import not_tests_uncon_optimizer as tw

if __name__ == '__main__':
    testwrapper = tw.TestsYouMustPass()

    print("Steepest descent with backtracking line search")
    testwrapper.set_options(
        {"direction": "steepdesc", "linsearch": "backtrack"})
    testwrapper.test_slanted_quad()
    testwrapper.test_bean()
    # this will fail, so need to catch
    try:
        testwrapper.test_rosenbrock()
    except:
        print("Rosenbrock failed as expected")

    print("\n\nBFGS with backtracking line search")
    testwrapper.set_options({"direction": "bfgs", "linsearch": "bracket"})
    testwrapper.test_slanted_quad()
    testwrapper.test_bean()
    testwrapper.test_rosenbrock()

    print("\n\nScipy")
    slanted_quad_x0 = np.array([0., 3.])
    res = minimize(tw.func_slanted_quad, slanted_quad_x0, jac=True)
    print(f"Slanted quad:\n{res.nfev}")

    bean_x0 = np.array([0., 0.])
    res = minimize(tw.func_bean, bean_x0, jac=True)
    print(f"Bean:\n{res.nfev}")

    rosenbrock_x0 = np.zeros(2)
    res = minimize(tw.func_rosenbrock, rosenbrock_x0, jac=True)
    print(f"Rosenbrock:\n{res.nfev}")
