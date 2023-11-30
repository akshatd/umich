---
geometry: "margin=2cm"
---

# AE588 Assignment 6 - akshatdy

## 6.1

I chose to implement the Nelder-Mead algorithm because there was an easy to follow example in the book, and it is much easier to visualise than the other algorithms.

Nelder-mead works by first creating a simplex, which is a collection of n+1 points in the design space, where n is the number of design variables. This simplex is then modified in every iteration of the optimization to bring the simplex closer to the optimum. The simplex can be modified in the following ways:

- Reflection: Calculate the centroid of all points except the worst one. Then "reflect" the worst point through the centroid and evaluate the function at this reflected point.
- Expansion: If the reflected point is the best point so far, then try to extend the simplex in this direction, creating an expanded point, and evaluate the function there.
- Contraction (Inside/Outside): If neither reflection nor expansion improves the worst point, attempt to perform a contraction to reject the worst point, either inward or outward, and evaluate the function at the new point.
- Shrink: If contraction still doesn't work, then we shrink the whole simplex toward the best point.

The algorithm stops when either

- Number of iterations has reached a limit
- The distance between the points of the simplex is too small
- The standard deviation of the function values in the simplex is too small
