import matplotlib.pyplot as plt


def plot_step_error(fd_fwd, fd_ctr, cplx, steps, title):
    _, ax = plt.subplots()

    ax.plot(steps, fd_fwd, '-o', label="Forward difference")
    ax.plot(steps, fd_ctr, '-o', label="Central difference")
    ax.plot(steps, cplx, '-o', label="Complex Step")
    ax.legend()
    ax.set_xlabel("Step size, h")
    ax.set_xscale('log')
    ax.set_ylabel("Relative error, e")
    ax.set_yscale('log')
    ax.invert_xaxis()
    ax.set_title(title)
    plt.show()
