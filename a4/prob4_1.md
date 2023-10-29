# AE588 Assignment 4 - akshatdy

### 4.1

Maximize

$$
f(x_1, x_2) = x_1x_2
$$

Subject to

$$
h(x_1, x_2) = 2x_1 + 2x_2 - p = 0
$$

Lagrangian of the problem:

$$
\newcommand{\p}{\mathop{}\!{\partial}}
\newcommand{\Lagr}{\mathcal{L}}
{\Lagr}(x_1, x_2, \lambda) = x_1 x_2 - \lambda(2x_1 + 2x_2 -p)
$$

Differentiating this to get the first-order optimality conditions

$$
\renewcommand{\p}{\mathop{}\!{\partial}}
\renewcommand{\Lagr}{\mathcal{L}}
\frac{\p\Lagr}{\p x_1} = x_2 - 2 \lambda = 0
\\
\frac{\p\Lagr}{\p x_2} = x_1 - 2 \lambda = 0
\\
\frac{\p\Lagr}{\p \lambda} = - 2 x_1 - 2 x_2 + p = 0
$$

Solving these three equations for the three unknowns ($x_1 , x_2 , \lambda$), we obtain:

$$
x_A =
\begin{bmatrix}
   x_1 \\
   x_2
\end{bmatrix} =
\begin{bmatrix}
   p/4 \\
   p/4
\end{bmatrix},
\lambda_A = \frac{p}{8}
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

2nd order check passes with the Hessian

The units of the lambda is $m^2/m$, which is the change of area (in $m^2$) of the rectangle for a given a change in the perimeter constraint in $m$
