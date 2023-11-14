## 5.3

Using equation 6.42 for Example 6.12

$$
\newcommand{\p}{\mathop{}\!{\partial}}

\begin{aligned}
\frac{df}{dx} &= \frac{\p f}{\p x} - \frac{\p f}{\p u} \frac{\p r}{\p u}^{-1} \frac{\p r}{\p x}

\\\\
where \ \ \ \
\frac{\p f}{\p x} &= 0 \\
\frac{\p f}{\p u} &= S \\
\frac{\p r}{\p u} &= K \\
\frac{\p r}{\p x} &= using \ FD/CS

\\\\
so \ \ \ \
\frac{df}{dx} &= - SK^{-1}\frac{\p r}{\p x}
\\\\
For \ Direct \ method, \ compute \
K^{-1}\frac{\p r}{\p x} \\
\\\\
For \ Adjoint \ method, \ compute \
K^{-1}S^{T} \\

\end{aligned}
$$

Derivatives computed using:

- Forward finite-difference:
- Complex-step
- Implicit analytic direct method
