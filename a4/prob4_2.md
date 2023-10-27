$$
\newcommand{\d}{\mathop{}\!{d}}
\newcommand{\p}{\mathop{}\!{\partial}}
\newcommand{\L}{\mathcal{L}}
$$

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
\implies \frac{1}{I} &= \frac{768}{3 x_1 + 16 x_1^3 + x_2}
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
{\L}(x, \sigma, s) = 2bx_1 + hx_2 + \sigma_1(\frac{Plh}{2I} - {\sigma}_{yield} + s_1^2) + \sigma_2(\frac{1.5P}{hx_2} - {\tau}_{yield} + s_2^2)
$$

Differentiating the Lagrangian with respect to all the variables, we get the
first-order optimality conditions,

$$
\begin{align*}
% https://www.wolframalpha.com/input?i=d%2Fdx+2*b*x+%2B+h*y+%2B+g*%28P*l*h*768%2F%282*%28y%2B16*x%5E3%2B3*x%29%29+-+200000000+%2B+s%5E2%29+%2B+p*%281.5*P%2F%28h*y%29+-+116000000+%2B+t%5E2%29
% x=x1, y=x2, g=sigma1, p=sigma2, s=s1, t=s2
% just change the dx to dy etc to get the rest
&\frac{\p \L}{\p x_1} = 2b - \frac{384 \sigma_1 P l h (3 + 48 x_1^2)}{(3 x_1 + 16 x_1^3 + x_2)^2} &= 0
\\
&\frac{\p \L}{\p x_2} = h - \frac{384 \sigma_1 P l h}{(3 x_1 + 16 x_1^3 + x_2)^2} - \frac{1.5 \sigma_2 P}{h x_2^2} &= 0
\\
&\frac{\p \L}{\p \sigma_1} = \frac{384 P l h}{3 x_1 + 16 x_1^3 + x_2} - {\sigma}_{yield} + s_1^2 &= 0
\\
&\frac{\p \L}{\p \sigma_2} = \frac{1.5 P}{h x_2} - {\tau}_{yield} + s_2^2 &= 0
\\
&\frac{\p \L}{\p s_1} = 2 \sigma_1 s_1 &= 0
\\
&\frac{\p \L}{\p s_2} = 2 \sigma_2 s_2 &= 0
\end{align*}
$$

Roots of the equation found with scipy.optimize.fsolve, with initial guesses of $t_b(x_1), t_w(x_2)$ as $10cm(0.01m)$ by eyeballing the diagram, and letting $\sigma_1=\sigma_2=s_1=s_2=0$

$$
\begin{align*}
&t_b = 1.42603955e-02& \approx 14cm   \\
&t_w = 5.17241379e-03& \approx 5cm    \\
&\sigma_1 = 1.99351362e-11& \approx 0 \\
&\sigma_2 = 7.44367855e-12& \approx 0 \\
&s1 &= 0                              \\
&s2 &= 0
\end{align*}
$$
