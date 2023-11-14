#!/usr/bin/env python

import numpy as np
from truss import tenbartruss


if __name__ == "__main__":
    num_bars = 10
    areas = [
        # np.full(num_bars, 0.5),
        np.full(num_bars, 1),
        # np.full(num_bars, 1.5),
    ]
    # grads = ['FD', 'CS', 'DT', 'AJ', 'AD']
    grads = ['FD', 'CS']
    dstress_dAs = {}

    for A in areas:
        for grad in grads:
            mass, stress, dmass_dA, dstress_dA = tenbartruss(A, grad)
            dstress_dAs[grad] = dstress_dA
            print(f"{grad} with bars = {A} : {dstress_dA}")

    for grad, dstress in dstress_dAs.items():
        for grad2, dstress2 in dstress_dAs.items():
            if grad is not grad2:
                print(
                    f"Error between {grad} and {grad2} is {dstress - dstress2}")
