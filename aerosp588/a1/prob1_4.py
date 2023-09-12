#!/usr/bin/env python
# coding: utf-8

# ### 1.4

# ### Journal Article: Aerodynamic Optimization Design of Supersonic Wing Based on Discrete Adjoint
# [Link to paper](https://www.mdpi.com/2226-4310/10/5/420)
#
# ##### Problem formulation (Is it well posed? Classify the problem(s) according to Chapter 1 of the textbook)
# - The problem is well formulated, it is specifically about minimizing the fuel consumption in supersonic aircrafts by optimizing the aerodynamic shape to reduce drag.
# - Design Variables
# 	- The paper focuses on both subsonic and supersonic configurations, and the constriants are different for each
# 	- Subsonic
# 		- There are >200 design variables, that include:
# 			- Shape: the displacement of Free Form Deform (FFD) control points (240 in total) on the wing
# 			- Twist: 5 deflection angles of FFD control profile
# 			- Angle of attack
# 	- Supersonic
# 		- There are >100 design variables, that include:
# 			- Shape: the displacement of Free Form Deform (FFD) control points (120 in total) on the wing
# 			- Twist: 3 deflection angles of FFD control profile
# 			- Angle of attack
# 	- Classification: Continous
# - Objective Function
# 	- The initial design is a Lockheed Martin (LM) 1021 developed by NASA N + 2 supersonic verification program
# 	- The objective is to minimize the total drag coefficient
# 	- Classification: Single
# - Constriants
# 	- The paper focuses on both subsonic and supersonic configurations, and the constriants are different for each
# 	- Subsonic
# 		- Thickness of wing (distributed over 7 spanwise sections): >= 97% of the original thickness
# 		- Volume of wing(defined between 50 cross-sections, 25 parts in each cross-section): >= initial volume
# 		- Pitching moment coefficient: >= 0
# 		- Lift coefficient: = 0.142
# 	- Supersonic
# 		- Thickness of wing (distributed over 4 spanwise sections): 2 separate (>=70% and >=90%) of the original thickness
# 		- Volume of wing(defined between 50 cross-sections, 25 parts in each cross-section): 20–70% of the chord length and >= initial volume
# 		- Pitching moment coefficient: >= 0
# 		- Lift coefficient: = 0.195
# 	- Classification: Constrained
#
# ##### Optimization method used (classify the method(s) according to Chapter 1 of the textbook)
# - Optimization method is the SNOPT with the Sequential Quadratic Programming (SQP) algorithm
# - Gradient based
# - Classification
# 	- Smoothness: Continuous
# 	- Linearity: Nonlinear
# 	- Modality: Multimodal
# 	- Convexity: Nonconvex
# 	- Stochasticity: Deterministic
#
# ##### Models, and solvers (see overview of solvers in Chapter 3)
# - uses RANS solver ADflow for structured mesh and overset mesh
# - uses a numerical simulation for aerodynamic optimization
# - uses the three-dimensional compressible RANS equation as the governing equation of the flow field
# - uses the discrete adjoint method to calculate the gradient for minimization
#
# ##### Suitability of methods to solve the problem
# - The methods are suitable because they are able to achieve the results within the scope of the study
# - Even though the problem is well formulated, the issue in this study is mainly that they assumed that there would be a direct correlation between induced drag and fuel consumption, which turns out to be not true because there are other factors that affect it.
#
# ##### Practicality of the results
# - The results are not very practical because this is only optimized for a single metric, which is the drag coeffient
# - There should be other objectives like weight reduction, which can significantly affect the fuel consumption of the flight, especially when fuel consumption was the primary objective of this study
#
# ##### Conclusions (hint: draw your own conclusions before reading the conclusions in the paper and then compare)
# - The paper achieves an improvement of ~4.5% over the origial design, which would be significant fuel savings for long haul flights if multiplied for an entire fleet of aircraft
# - However, the additional shockwave drag makes this design not very optimal because that was never considered during the optimization
# - This seems like a great problem for a multidisciplinary design optimisation with multple objectives
