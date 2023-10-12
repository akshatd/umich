import matplotlib.pyplot as plt
import not_tests_uncon_optimizer as tw


def plot_convergence(output):
    plt.xlabel('Iteration')
    plt.ylabel('Norm of gradient')
    plt.yscale('log')
    plt.title(f'{output["func_in"]}')
    plt.plot(output['infnorm'])
    plt.show()


if __name__ == '__main__':
    testwrapper = tw.TestsYouMustPass()
    print("\n\nBFGS with backtracking line search")
    testwrapper.set_options({"direction": "bfgs", "linsearch": "bracket"})

    testwrapper.test_slanted_quad()
    output = testwrapper.get_output()
    plot_convergence(output)

    testwrapper.test_bean()
    output = testwrapper.get_output()
    plot_convergence(output)

    testwrapper.test_rosenbrock()
    output = testwrapper.get_output()
    plot_convergence(output)
