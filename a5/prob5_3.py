#!/usr/bin/env python

import numpy as np
from truss import tenbartruss


if __name__ == "__main__":
    num_bars = 10
    areas = [
        # 0.5,
        51e-5,
        # 1.5,
    ]
    # grads = ['FD', 'CS']
    grads = ['FD', 'CS', 'DT']
    # grads = ['FD', 'CS', 'DT', 'AJ']
    # grads = ['FD', 'CS', 'DT', 'AJ', 'AD']
    dstress_dAs = {}
    grad_set = set()
    for area in areas:
        for grad in grads:
            mass, stress, dmass_dA, dstress_dA = tenbartruss(
                np.full(num_bars, area), grad)
            dstress_dAs[grad] = dstress_dA
            print(f"{grad} with bars = {area} :\n{dstress_dA}")

    for grad1, dstress in dstress_dAs.items():
        for grad2, dstress2 in dstress_dAs.items():
            if grad1 is not grad2 and grad1+grad2 not in grad_set and grad2+grad1 not in grad_set:
                grad_set.add(grad1+grad2)
                print(
                    f"Mean error between {grad1} and {grad2} is {np.mean(np.abs(dstress - dstress2)/np.abs(dstress2))}")
                print(
                    f"Max error between {grad1} and {grad2} is {np.max(np.abs(dstress - dstress2)/np.abs(dstress2))}")
