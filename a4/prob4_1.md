$$
\newcommand{\d}{\mathop{}\!{d}}
\newcommand{\p}{\mathop{}\!{\partial}}
\newcommand{\L}{\mathcal{L}}
$$

## AE588 Assignment 4 - akshatdy

### 4.1

Minimize/Maximize $f(x_1, x_2) = x_1x_2$

Subject to $h(x_1, x_2) = 2x_1 + 2x_2 - 4 = 0$

Lagrangian of the problem:

$$
{\L}(x_1, x_2, \lambda) = x_1 x_2 + \lambda(2x_1 + 2x_2 -4)
\\
\implies
{\L}(x_1, x_2, \lambda) = x_1 x_2 + \lambda 2x_1 +  \lambda 2x_2 - \lambda 4
$$

Differentiating this to get the first-order optimality conditions

$$
\frac{\p\L}{\p x_1} = x_2 + 2 \lambda = 0
\\
\frac{\p\L}{\p x_2} = x_1 + 2 \lambda = 0
\\
\frac{\p\L}{\p \lambda} = 2 x_1 + 2 x_2 - 4 = 0
$$

Solving these three equations for the three unknowns ($x_1 , x_2 , \lambda$), we obtain:

$$
x_A =
\begin{bmatrix}
   x_1 \\
   x_2
\end{bmatrix} =
\begin{bmatrix}
   1 \\
   1
\end{bmatrix},
\lambda_A = \frac{1}{2}
\\
$$

Checking the Hessian

$$
H =
\begin{bmatrix}
   0 & 1 \\
   1 & 0
\end{bmatrix}
$$

The hessian is not positive definite since the eigenvalues are not all positve, so this is the maximum

The units of the lambda is $m^2/m$, which is the change of area (in $m^2$) of the rectangle for a given a change in the perimeter constraint in $m$
