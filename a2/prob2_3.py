#!/usr/bin/env python
# coding: utf-8

# # AE588 Assignment 2
#
# # 2.3
#

# In[26]:


import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

# example 4.8 functions and directions
DIR_4_8 = np.array([4, 0.75])


def dir_4_8(x: npt.ArrayLike) -> float:
    return DIR_4_8


def grad_4_8(x: npt.ArrayLike):
    return [
        0.6 *
        x[0]**5 -
        6 *
        x[0]**3 +
        10 *
        x[0] +
        0.5 *
        x[1],
        0.4 *
        x[1]**3 +
        6 *
        x[1] -
        9 +
        0.5 *
        x[0]]


def fn_4_8(x: npt.ArrayLike) -> float:
    return 0.1 * (x[0]**6) - 1.5 * (x[0]**4) + 5 * (x[0]**2) + 0.1 * \
        (x[1]**4) + 3 * (x[1]**2) - 9 * x[1] + 0.5 * x[0] * (x[1])


# In[27]:


# interpolation
def interpolation_min(func, func_grad, a_low, a_high):
    return (2 * a_low * (func(a_high) - func(a_low)) + func_grad(a_low) * (a_low**2 -
            a_high**2)) / (2 * (func(a_high) - func(a_low)) + func_grad(a_low) * (a_low - a_high))

# pinpointing


def pinpoint(
        func,
        func_grad,
        dir,
        a_low,
        a_high,
        phi_0,
        phi_low,
        phi_high,
        phi_0_grad,
        phi_low_grad,
        phi_high_grad,
        suff_dec,
        suff_cur):
    k = 0
    while True:
        a_p = interpolation_min(func, func_grad, a_low, a_high)
        print(
            f"after interpolation: a_low: {a_low}, a_high: {a_high}, a_p: {a_p}")
        phi_p = func(a_p)
        phi_p_grad = func_grad(a_p)
        print(f"k: {k}, a_low: {a_low}, a_high: {a_high}, phi_0: {phi_0}, phi_low: {phi_low}, phi_high: {phi_high}, phi_0_grad: {phi_0_grad}, phi_low_grad: {phi_low_grad}, phi_high_grad: {phi_high_grad}, suff_dec: {suff_dec}, suff_cur: {suff_cur}")
        if phi_p > phi_0 + suff_dec * \
                np.dot(a_p * phi_0_grad, dir) or phi_p > phi_low:
            a_high = a_p
            phi_high = phi_p
            # phi_high_grad = phi_p_grad
        else:
            if abs(np.dot(phi_p_grad, dir)) <= - \
                    suff_cur * np.dot(phi_0_grad, dir):
                a = a_p
                return a_p
            elif np.dot(phi_p_grad * (a_high - a_low), dir) >= 0:
                a_high = a_low
            a_low = a_p
        k = k + 1


# bracketing
# suff_dec = u1
# suff_cur = u2
# step_inc = 𝜎 or sigma
def bracket(
        func,
        func_grad,
        dir: npt.ArrayLike,
        guess: npt.ArrayLike,
        initial_step: float,
        suff_dec: float,
        suff_cur: float,
        step_inc: float):
    step = initial_step
    brkt_start = guess  # a1
    brkt_end = guess + initial_step  # a2
    func_0 = func(guess)  # phi 0
    func_grad_0 = func_grad(guess)  # phi 0 prime
    func_start = func_0  # phi 1
    func_start_grad = func_grad_0  # phi 1 prime
    # func_end = guess_diff # phi 2
    first = True
    while (True):
        print(f"step: {step}, brkt_start: {brkt_start}, brkt_end: {brkt_end}")
        func_end = func(brkt_end)  # phi 2
        # check if sufficient decrease conditions already met or the end is
        # higher than start
        if (func_end > (func_0 + suff_dec * step * np.dot(dir,
                                                          func_start_grad))) or (not first and func_end > func_start):
            step = pinpoint(
                func,
                func_grad,
                dir,
                brkt_start,
                brkt_end,
                func_0,
                func_end,
                func(brkt_start),
                func_grad_0,
                func_grad(brkt_start),
                func_grad(brkt_end),
                suff_dec,
                suff_cur)
            return step
        func_end_grad = func_grad(brkt_end)  # phi 2 prime
        # check if sufficient curvature conditions met
        if abs(func_end_grad) <= -suff_cur * func_grad_0:
            step = brkt_end
            return step
        # check if end gradient is positive, suggesting the min is within the
        # bracket
        elif func_end_grad >= 0:
            # step = pinpoint(...)
            step = pinpoint(
                func,
                func_grad,
                dir,
                brkt_end,
                brkt_start,
                func_0,
                func(brkt_start),
                func_end,
                func_grad_0,
                func_grad(brkt_end),
                func_grad(brkt_start),
                suff_dec,
                suff_cur)
            return step
        else:
            brkt_start = brkt_end
            brkt_end = brkt_start * step_inc
        first = False


# backtracking line search
def bktrk_lin_search(
        func,
        grad: npt.ArrayLike,
        dir: npt.ArrayLike,
        guess: npt.ArrayLike,
        initial_step: float,
        suff_dec: float,
        bktrk: float):
    step = initial_step
    steps = [initial_step]
    fn_list = [func(guess + (step * dir))]
    # print(f"step: {step}, fx: {func(guess + (step * dir))}")
    # step+dir = step in a particular dir
    # dot prod to know how much the fn is expected to decrease in a particular
    # dir
    while func(guess + (step * dir)) > (func(guess) +
                                        suff_dec * step * np.dot(grad, dir)):
        step = bktrk * step
        # print(f"step: {step}, fx: {func(guess + (step * dir))}")
        steps.append(step)
        fn_list.append(func(guess + (step * dir)))
    return steps, fn_list

# gradient optimization


def grad_opt(
        func,
        func_grad,
        func_dir,
        guess: npt.ArrayLike,
        tolerance: float,
        initial_step: float,
        suff_dec: float,
        bktrk: float):
    it = 0
    step = initial_step
    grad = func_grad(guess)
    val_list = [func(guess)]
    # gradient should tend towards 0, but wont here because we will never
    # change to the right direction
    while np.linalg.norm(func_grad(guess), np.inf) > tolerance:
        print(
            f"it: {it}, step: {step}, guess: {guess}, fx: {func(guess)}, grad: {func_grad(guess)}")
        dir = func_dir(guess)
        steps, fn_list = bktrk_lin_search(func, func_grad(
            guess), dir, guess, step, suff_dec, bktrk)
        step = steps[-1]
        guess = guess + step * dir
        it += 1
        val_list.append(func(guess))
        # print(f"backtrack: {fn_list}")
        # print(
        # f"it: {it}, step: {step}, guess: {guess}, fx: {func(guess)}, grad:
        # {func_grad(guess)}")

    # plot optimization fn vs iterations
    # plt.plot(val_list)
    # plt.xlabel("iteration")
    # plt.ylabel("f")
    # plt.title("Optimization: Function vs iterations")
    # plt.show()
    return guess, func(guess)


# 2.3.a) Graphs for Example 4.8
#

# In[30]:


# run optimization on 4.8 with defaults
SUFF_DEC = 1e-4  # u
BKTRK = 0.7  # p
TOLERANCE = 1e-6  # t
GUESS_4_8 = np.array([-1.25, 1.25])
INITIAL_STEP = 1.2
# grad opt wont work because the direction function isnt implemented
# x, fx = grad_opt(fn_4_8, grad_4_8, dir_4_8, GUESS_4_8, TOLERANCE,
#                  INITAL_STEP, SUFF_DEC, BKTRK)
steps, fx = bktrk_lin_search(fn_4_8, grad_4_8(GUESS_4_8), dir_4_8(
    GUESS_4_8), GUESS_4_8, INITIAL_STEP, SUFF_DEC, BKTRK)

print(
    f"final guess: {GUESS_4_8 + steps[-1]}, grad: {grad_4_8(GUESS_4_8 + steps[-1])}, dir grad: {np.dot(grad_4_8(GUESS_4_8 + steps[-1]), dir_4_8(GUESS_4_8))}")


# plot backtrack vs iterations
plt.plot(fx)
plt.xlabel("backtrack iteration")
plt.ylabel("f")
plt.title(f"Backtrack: Function vs iterations")
plt.show()


# plot backtrack vs step
plt.plot(steps, fx)
plt.xlabel("backtrack step")
plt.ylabel("f")
plt.title(f"Backtrack: Function vs steps")
plt.show()


# 2.3.a) Graphs for example 4.9
#

# In[29]:


# run bracketing on 4.9 with defaults
SUFF_DEC = 1e-4  # u1
SUFF_CUR = 0.9  # u2
STEP_INCR = 2
TOLERANCE = 1e-6  # t
GUESS_4_8 = np.array([-1.25, 1.25])
INITAL_STEP = 1.2
x, fx = bracket(fn_4_8, grad_4_8, dir_4_8(GUESS_4_8), GUESS_4_8,
                INITAL_STEP, SUFF_DEC, SUFF_CUR, STEP_INCR)
print(x, fx)
