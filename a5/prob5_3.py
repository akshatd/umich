#!/usr/bin/env python

import numpy as np
from time import time
from truss import tenbartruss


if __name__ == "__main__":
    num_bars = 10
    areas = [
        51e-5,
        51e-4,
    ]
    # grads = ['FD', 'CS']
    # grads = ['FD', 'CS', 'DT']
    grads = ['FD', 'CS', 'DT', 'AJ']
    # grads = ['FD', 'CS', 'DT', 'AJ', 'AD']
    dstress_dAs = {}
    for area in areas:
        print(f"Bar area = {area}")
        for grad in grads:
            cs_area = np.full(num_bars, area)
            # bars = np.array([0.1, 0.01, 0.2, 0.02, 0.3,
            #                 0.03, 0.4, 0.04, 0.5, 0.05,])
            mass, stress, dmass_dA, dstress_dA = tenbartruss(cs_area, grad)
            dstress_dAs[grad] = dstress_dA
            # print(f"{grad} with bars = {area} :\n{dstress_dA}")
        grad_set = set()
        for grad1, dstress in dstress_dAs.items():
            for grad2, dstress2 in dstress_dAs.items():
                if grad1 is not grad2 and grad1+grad2 not in grad_set and grad2+grad1 not in grad_set:
                    grad_set.add(grad1+grad2)
                    print(
                        f"Error between {grad1} and {grad2}\n- Mean: {np.mean(np.abs(dstress - dstress2)/np.abs(dstress2))}\n- Max: {np.max(np.abs(dstress - dstress2)/np.abs(dstress2))}\n")

    # benchmark all the functions
    iters = 100
    for grad in grads:
        cs_area = np.full(num_bars, 51e-5)
        start = time()

        for i in range(iters):
            mass, stress, dmass_dA, dstress_dA = tenbartruss(cs_area, grad)

        end = time()
        print(f"Time per fn call for {grad} = {(end-start)/iters*1000} ms")
