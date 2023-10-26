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

There is just one possibility of a valid x, so this is the maximum

The units of the lambda is $m^2/m$, which is the change of area (in $m^2$) of the rectangle for a given a change in the perimeter constraint in $m$

### 4.2

Constants:

$$
\begin{align*}
h = 250mm &= .25m
\\
b = 125mm &= .125m
\\
{\sigma}_{yield} = 200MPa &= 200000000Pa
\\
{\tau}_{yield} = 116MPa &= 116000000Pa
\\
P = 100kN &= 100000N
\\
l &= 1m
\end{align*}
$$

Variables

$$
t_b = x_1
\\
t_w = x_2
$$

Minimize

$$
f(x_1, x_2) = 2bx_1 + hx_2
$$

Given second moment of area

$$
\begin{align*}
I &= \frac{h^3}{12}x_2 + \frac{b}{6}x_1^3 + \frac{h^2b}{2}x_1
\\
\implies I &= \frac{.25^3}{12}x_2 + \frac{.125}{6}x_1^3 + \frac{.25^2.125}{2}x_1
\\
\implies I &= \frac{x_2}{768} + \frac{x_1^3}{48} + \frac{x_1}{256}
\\
\implies I &= \frac{x_2 + 16 x_1^3  + 3 x_1}{768}
\\
\implies \frac{1}{I} &= \frac{768}{x_2 + 16 x_1^3  + 3 x_1}
\end{align*}
$$

Subject to

$$
\begin{align*}
g_1(x_1, x_2) &= \frac{Plh}{2I} - {\sigma}_{yield} \leq 0
\\
g_2(x_2) &= \frac{1.5P}{hx_2} - {\tau}_{yield} \leq 0
\end{align*}
$$

The Lagrangian for this problem is

$$
\begin{align*}
{\L}(x, \sigma, s) &= 2bx_1 + hx_2 + \sigma_1(\frac{Plh}{2I} - {\sigma}_{yield} + s_1^2) + \sigma_2(\frac{1.5P}{hx_2} - {\tau}_{yield} + s_2^2)
\\
\implies
{\L}(x, \sigma, s) &= .25x_1 + .25x_2 + \frac{9600000 \sigma_1}{x_2 + 16 x_1^3  + 3 x_1} - 200000000 \sigma_1 + \sigma_1 s_1^2 + \frac{600000 \sigma_2}{x_2} - 116000000 \sigma_2 + \sigma_2 s_2^2
\end{align*}
$$

Differentiating the Lagrangian with respect to all the variables, we get the
first-order optimality conditions,

$$
\begin{align*}
% https://www.emathhelp.net/en/calculators/calculus-3/partial-derivative-calculator/?f=9600000%2F%28y+%2B+16*x%5E3+%2B+3*x%29&var=x
&\frac{\p \L}{\p x_1} = 0.250 - \sigma_1\frac{460800000 x_1^2 + 28800000}{(16 x_1^3 + 3 x_1 + x_2)^2}
\\
% https://www.emathhelp.net/en/calculators/calculus-3/partial-derivative-calculator/?f=9600000%2F%28y+%2B+16*x%5E3+%2B+3*x%29&var=y
% https://www.emathhelp.net/en/calculators/calculus-3/partial-derivative-calculator/?f=600000%2Fy&var=y
&\frac{\p \L}{\p x_2} = 0.250 - \frac{9600000 \sigma_1}{(16 x_1^3 + 3 x_1 + x_2)^2} - \frac{600000\sigma_2}{x_2^2}
\\
&\frac{\p \L}{\p \sigma_1} = \frac{9600000}{x_2 + 16 x_1^3  + 3 x_1} - 200000000 + s_1^2 = 0
\\
&\frac{\p \L}{\p \sigma_2} = \frac{600000}{x_2} - 116000000 + s_2^2 = 0
\\
&\frac{\p \L}{\p s_1} = 2 \sigma_1 s_1 = 0
\\
&\frac{\p \L}{\p s_2} = 2 \sigma_2 s_2 = 0
\end{align*}
$$

Slackness conditions

$$
\begin{array}{ccccccccc}
\hline
Assumption & Meaning & x_1 & x_2 & \sigma_1 & \sigma_2 & s_1 & s_2 & Point \\ \hline
s_1 = 0      & g_1\text{ is active}   & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
s_2 = 0      & g_2\text{ is active}   & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ \hline
\sigma_1 = 0 & g_1\text{ is inactive} & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
\sigma_2 = 0 & g_2\text{ is inactive} & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ \hline
s_1 = 0      & g_1\text{ is active}   & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
\sigma_2 = 0 & g_2\text{ is inactive} & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ \hline
\sigma_1 = 0 & g_1\text{ is inactive} & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
s_2 = 0      & g_2\text{ is active}   & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ \hline
\end{array}
$$
