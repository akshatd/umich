---
geometry: "margin=2cm"
---

## 6.2

General notes:

- In my implementation of Nelder-Mead, I have adjusted the maximum iterations allowable to ensure that the optimizer always exits only when convergence critera for $\Delta_f$ and $\Delta_x$ are met.
- The convergence criteria for SciPy based optimizers have been left at their defaults.
- When using a gradient based method, I provide the function and gradient separately to SciPy. Hence, when calculating the total function calls (fev), I have added both the function and jacobian evaluations for the SciPy BFGS cases with analytical gradients.

### 6.2.a

Results for my Nelder-Mead implementation:

| fev | x\*                                | fx\*            |
| --- | ---------------------------------- | --------------- |
| 118 | [ 1.2134114738702 0.8241223344287] | 0.0919438164113 |

![Optimization path for Nelder-Mead on the Bean function](6.2.a.svg "6.2.a")

\pagebreak

### 6.2.b

Results comparing the optimization of a noisy bean function between:

- my implementation of Nelder-Mead
  - This was given enough iterations so that it never stops unless the other convergence critera are met
- Scipy BFGS and analytical gradient that is consistent with the noisy bean function
  - left at default settings so it may stop without meeting convergence criteria
  - function evaluations and jacobian evaluations are added to get a full picture of the total "function" calls since those are provided separately

The noise was varied from $1e^{-1}$ to $1e^{-9}$, but only certain important results are displayed here so the table can look nice

The results in the table are based on the difference between

- a baseline optimum given by BFGS with analytical gradients on smooth bean
- the optimum given by Nelder-Mead and BFGS on a noisy bean

| noise    | 1e-09            | 1e-07            | 1e-04            | 1e-03            | 1e-01            |
| -------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| NM x1    | 2.0163130543e-07 | 1.7823436629e-06 | 1.1398095279e-03 | 1.1137357362e-02 | 1.4233977454e-01 |
| BFGS x1  | 2.1221663982e-08 | 1.7827848480e-06 | 1.1387659005e-03 | 1.1137250698e-02 | 3.0250005917e-01 |
| NM x2    | 1.0921469717e-07 | 3.1169619389e-06 | 3.2864916927e-04 | 1.3311632814e-02 | 2.1351179809e-01 |
| BFGS x2  | 3.0562184006e-08 | 3.0765705131e-06 | 3.2676560626e-04 | 1.3310648521e-02 | 4.3373146544e-01 |
| NM fx    | 8.9171718620e-10 | 6.0122489765e-08 | 1.0421326057e-04 | 1.2019839886e-04 | 3.4746256407e-02 |
| BFGS fx  | 8.9175596074e-10 | 6.0122437681e-08 | 1.0421325524e-04 | 1.2019881706e-04 | 1.2929027499e-01 |
| NM fev   | 118              | 116              | 119              | 152              | 165              |
| BFGS fev | 22               | 22               | 24               | 128              | 260              |

We can see that in most cases with low noise, BFGS beats or matches the precision of Nelder-Mead, with a lot lower function evaluations. However, as the noise starts getting high, around $1e^{-3}$, BFGS starts to struggle, with a lot higher function evaluations and eventually at $1e^{-1}$, the result from BFGS is a lot worse than the result from Nelder-Mead.

This might happen because as the noise becomes higher, the gradient that BFGS uses gets more and more affected by the noise as it starts to converge towards the minimum, and is unable to proceed in the correct direction.

This behaviour can be seen if we trace the optimization path of Nelder-Mead with BFGS at an acceptable noise level, like $1e^{-4}$ and again at $1e^{-3}$, where you can see that it starts zig-zagging a lot more towards the end trying to find the optimum

![Noise of 1e-4](6.2.b.4.svg "6.2.b.4"){ width=550px }

![Noise of 1e-3](6.2.b.3.svg "6.2.b.3"){ width=550px }

From this, we can conclude that Nelder-Mead is better suited to situations where the noise is quite high proportional to the function and gradient value near the optimum.

\pagebreak

### 6.2.c

Results comparing the optimization of a bean function with checkerboard steps between:

- my implementation of Nelder-Mead
  - This was given enough iterations so that it never stops unless the other convergence critera are met
- Scipy BFGS and analytical gradient that is **same as** the smooth bean function
  - left at default settings so it may stop without meeting convergence criteria
  - function evaluations and jacobian evaluations are added to get a full picture of the total "function" calls since those are provided separately

The results in the table are based on the difference between

- a baseline optimum given by BFGS with analytical gradients on smooth bean
- the optimum given by Nelder-Mead and BFGS on a bean with checkerboard steps
