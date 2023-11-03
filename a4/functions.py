import numpy as np

# f_* are functions
# h_* are equality constraints
# g_* are inequality constraints
# df, dh, dg are derivatives, will output jacobians


# prob 4.2

h = .25
b = .125
sigma_yield = 200000000
tau_yeild = 116000000
P = 100000
l = 1


def p42_f(x):
    return 2*b*x[0] + h*x[1]


def p42_df(x):
    return np.array([2*b, h])


def p42_I_inv(x):
    return 768/(3*x[0] + 16*x[0]**3 + x[1])


def p42_dI_inv(x):
    u = (3*x[0] + 16*x[0]**3 + x[1])
    du = np.array([3 + 48*x[0]**2, 1])
    return -768*du/u**2


def p42_g1(x):
    return P*l*h*p42_I_inv(x)/2 - sigma_yield


def p42_dg1(x):
    return P*l*h*p42_dI_inv(x)/2


def p42_g2(x):
    return 1.5*P/(h*x[1]) - tau_yeild


def p42_dg2(x):
    return np.array([0, -1.5*P/(h*x[1]**2)])


def p42_dL(vars):
    x1, x2, sigma1, sigma2, s1, s2 = vars
    x = [x1, x2]
    dx = p42_df(x) + sigma1*p42_dg1(x) + sigma2*p42_dg2(x)
    dsig1 = p42_g1(x) + s1**2
    dsig2 = p42_g2(x) + s2**2
    ds1 = 2*sigma1*s1
    ds2 = 2*sigma2*s2

    return [dx[0], dx[1], dsig1, dsig2, ds1, ds2]


# prob 4.3

def e5_4_f(x):
    return x[0] + 2*x[1]


def e5_4_df(x):
    return np.array([1, 2])


def e5_4_g(x):
    return 1/4*x[0]**2 + x[1]**2 - 1


def e5_4_dg(x):
    return np.array([1/2*x[0], 2*x[1]])


if __name__ == "__main__":
    # Initial guesses for variables
    x_initial_guesses = [0.12345, 0.43534, 0.01231, 0.3242412, 1, 241]
    # x_initial_guesses = [0.01212345, 12.43534, 0.0, 0.3242412, 1, 0]
    print(p42_dL(x_initial_guesses))
