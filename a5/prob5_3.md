## 5.3

Using equation 6.42 for Example 6.12

$$
\newcommand{\p}{\mathop{}\!{\partial}}
\begin{aligned}
\frac{df}{dx} &= \frac{\p f}{\p x} - \frac{\p f}{\p u} \frac{\p r}{\p u}^{-1} \frac{\p r}{\p x} \\
\\ where \\
\frac{\p f}{\p x} &= 0 \\
\frac{\p f}{\p u} &= S \\
\frac{\p r}{\p u} &= K \\
\frac{\p r}{\p x} &= using \ FD/CS
\\\\
For \ Direct \ method, \ we \ need \ \phi \ such \ that \\
K \phi &= \frac{\p}{\p x}Ku \\
which \ can \ be \ obtaied \ using \ a \ linear \ solver \\
We \ can \ then \ use \ \phi \ to \ get \\
\frac{df}{dx} &= -S\phi \\
\\\\
For \ Adjoint \ method, \ we \ need \ \psi \ such \ that \\
K\psi = S^T \\
which \ can \ be \ obtaied \ using \ a \ linear \ solver \\
We \ can \ then \ use \ \psi \ to \ get \\
\frac{df}{dx} &= -\psi^T \frac{\p}{\p x}Ku \\
\end{aligned}
$$

Unlike the example 6.12, we actually did not need to go column by column or row by row to compute $\phi$ or $\psi$ since they can be solved in a single call with the numpy linear solver. This is why I skiped the $i$ and $j$ subscripts in the equations.

### Relative errors of derivatives

Columns are the algorithms being compared, rows are the algorithms being compared to

#### Mean Error

Cross section area = 0.00051

|     | FD                     | CS                     | DT                     |
| --- | ---------------------- | ---------------------- | ---------------------- |
| FD  |                        |                        |                        |
| CS  | 1.5693885405866314e-05 |                        |                        |
| DT  | 5.267695884326408e-09  | 1.5694225171944888e-05 |                        |
| AJ  | 5.267695954118095e-09  | 1.56942251720772e-05   | 2.0698942265641576e-15 |

Cross section area = 0.0051

|     | FD                     | CS                     | DT                    |
| --- | ---------------------- | ---------------------- | --------------------- |
| FD  |                        |                        |                       |
| CS  | 1.5740799499070659e-06 |                        |                       |
| DT  | 2.896905846095844e-08  | 1.5765855570527423e-06 |                       |
| AJ  | 2.896905875393636e-08  | 1.5765855567551157e-06 | 1.560493808446306e-15 |

#### Max Error

Cross section area = 0.00051

|     | FD                    | CS                    | DT                     |
| --- | --------------------- | --------------------- | ---------------------- |
| FD  |                       |                       |                        |
| CS  | 1.76301404257226e-05  |                       |                        |
| DT  | 7.345428070377964e-08 | 1.759104891132644e-05 |                        |
| AJ  | 7.345428458456883e-08 | 1.759104891275623e-05 | 3.5909090956818885e-14 |

Cross section area = 0.0051

|     | FD                     | CS                     | DT                     |
| --- | ---------------------- | ---------------------- | ---------------------- |
| FD  |                        |                        |                        |
| CS  | 2.0315278996614934e-06 |                        |                        |
| DT  | 3.354622427716693e-07  | 1.7679381964847262e-06 |                        |
| AJ  | 3.354622481970304e-07  | 1.767938198420282e-06  | 1.9663696351694963e-14 |

#### Discussion

As expected, DT and AJ perform similarly, while FD and CS perform worse than those methods. It is interesting that DJ and AJ are not exactly the same, because mathematically they should be. This could be due to the loss of precision adding up as we multiply different matrices together for DT and AJ. The more mathematical operations we do, the more accuracy we will lose. Also, both of these methods are using a linear solver to solve a different set of equations, where the precision loss might also build up.

Another interesting observation is that according to the theory, the CS method should be very accurate, but it is not as close to the DT and AJ methods as expected.

### Computational cost of derivatives

These tests are averaged over 100 function calls

FD = 4.062857627868652 ms

CS = 4.0137457847595215 ms

DT = 5.500221252441406 ms

AJ = 5.625064373016357 ms

All the algorithms take around the same amount of time, which makes sense given that they are all making 2 calls to the function for the finite difference steps (2x effort per call for complex step for the imaginary part). Ideally the finite difference would not be needed if we could calculate the partial derivatives symbolically and that would save a lot of computation time and make DT and AJ more efficient than the rest. In addition to the function calls, DT and AJ also involve using a linear solver, which adds to their run time, making them slighly slower.
