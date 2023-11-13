## 5.2

$$
\begin{aligned}
x_1 &= M \\
u_1 &= E \\
r_1(x_1) &= M \\
r_2(u_1) &= E - e sin(E) - M = 0 \\
r_3(x_1, u_1) &= f - E + M \\
\end{aligned}
$$

The forward system of the UDE is:

$$
\begin{bmatrix}
   1 & 0 & 0 \\
   -1 & 1-ecos(E) & 0 \\
	 1 & -1 & 1
\end{bmatrix}
\begin{bmatrix}
   1 & 0 & 0 \\
   \frac{d u_1}{d x_1} & \frac{d u_1}{d r_2} & 0 \\
   \frac{d f}{d x_1} & \frac{d f}{d r_2} & 0
\end{bmatrix}
=
\begin{bmatrix}
   1 & 0 & 0 \\
   0 & 1 & 0 \\
   0 & 0 & 1
\end{bmatrix}
$$

Solving the first column to get $\frac{d f}{d x_1}$

$$
\begin{bmatrix}
   1 & 0 & 0 \\
   -1 & 1-ecos(E) & 0 \\
	 1 & -1 & 1
\end{bmatrix}
\begin{bmatrix}
   1 \\
   \frac{d u_1}{d x_1} \\
   \frac{d f}{d x_1}
\end{bmatrix}
=
\begin{bmatrix}
   1 \\
   0 \\
   0
\end{bmatrix}
$$

We have

$$
\begin{aligned}
1 &= 1 \\
-1 + \frac{d u_1}{d x_1}(1-ecos(E)) &= 0 \\
1 - \frac{d u_1}{d x_1} + \frac{d f}{d x_1} &= 0
\end{aligned}
$$

Solving for $\frac{d f}{d x_1}$, we get

$$
\frac{d f}{d x_1} = \frac{1}{1 - ecos(E)} - 1 \\
$$

so

$$
\frac{d f}{d M} = \frac{1}{1 - ecos(E)} - 1
$$

Verification with finite differences match the analytical results

- at M=0.5, df/dM is:
  - UDE: 0.4202054768667982
  - FD: 0.4202054315616266
- at M=1, df/dM is:
  - UDE: -0.07958665799511588
  - FD: -0.07958664394180914
- at M=1.5, df/dM is:
  - UDE: -0.26214792220067595
  - FD: -0.2621479411324401
- at M=2, df/dM is:
  - UDE: -0.349858262004625
  - FD: -0.3498582623606694
- at M=3, df/dM is:
  - UDE: -0.41092304468673113
  - FD: -0.4109230378190887
