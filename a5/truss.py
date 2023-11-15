import numpy as np
from math import sin, cos
# import derivatives as der
import math


def bar(E, A, L, phi):
    """Computes the stiffness and stress matrix for one element

    Parameters
    ----------
    E : float
        modulus of elasticity
    A : float
        cross-sectional area
    L : float
        length of element
    phi : float
        orientation of element

    Outputs
    -------
    K : 4 x 4 ndarray
        stiffness matrix
    S : 1 x 4 ndarray
        stress matrix

    """

    # rename
    c = cos(phi)
    s = sin(phi)

    # stiffness matrix
    k0 = np.array([[c**2, c * s], [c * s, s**2]])
    k1 = np.hstack([k0, -k0])
    K = E * A / L * np.vstack([k1, -k1])

    # stress matrix
    S = E / L * np.array([[-c, -s, c, s]])

    return K, S


def node2idx(node, DOF):
    """Computes the appropriate indices in the global matrix for
    the corresponding node numbers.  You pass in the number of the node
    (either as a scalar or an array of locations), and the degrees of
    freedom per node and it returns the corresponding indices in
    the global matrices

    """

    idx = np.array([], dtype=int)

    for i in range(len(node)):

        n = node[i]
        start = DOF * (n - 1)
        finish = DOF * n

        idx = np.concatenate((idx, np.arange(start, finish, dtype=int)))

    return idx


def truss(nodes1, nodes2, phi, A, L, E, rho, Fx, Fy, rigid):
    """Computes mass and stress for an arbitrary truss structure

    Parameters
    ----------
    nodes1 : ndarray of length nbar
        indices of the first nodes for bars. `nodes1` and `nodes2` can be in any order as long as consistent with phi
    nodes2 : ndarray of length nbar
        indices of the other nodes for bars
    phi : ndarray of length nbar (radians)
        defines orientation or bar
    A : ndarray of length nbar
        cross-sectional areas of each bar
    L : ndarray of length nbar
        length of each bar
    E : ndarray of length nbar
        modulus of elasticity of each bar
    rho : ndarray of length nbar
        material density of each bar
    Fx : ndarray of length nnode
        external force in the x-direction at each node
    Fy : ndarray of length nnode
        external force in the y-direction at each node
    rigid : list(boolean) of length nnode
        True if node_i is rigidly constrained

    Outputs
    -------
    mass : float
        mass of the entire structure
    stress : ndarray of length nbar
        stress of each bar

    """

    n = len(Fx)  # number of nodes
    DOF = 2  # number of degrees of freedom
    nbar = len(A)  # number of bars

    # mass
    mass = np.sum(rho * A * L)

    # stiffness and stress matrices
    K = np.zeros((DOF * n, DOF * n))
    S = np.zeros((nbar, DOF * n))
    if A.dtype == 'complex128':
        K = np.zeros((DOF * n, DOF * n), dtype='complex')
        S = np.zeros((nbar, DOF * n), dtype='complex')

    for i in range(nbar):  # loop through each bar

        # compute submatrix for each element
        Ksub, Ssub = bar(E[i], A[i], L[i], phi[i])

        # insert submatrix into global matrix
        # pass in the starting and ending node number for this element
        idx = node2idx([nodes1[i], nodes2[i]], DOF)
        K[np.ix_(idx, idx)] += Ksub
        S[i, idx] = Ssub

    # applied loads
    F = np.zeros((n * DOF, 1))

    for i in range(n):
        # add 1 b.c. made indexing 1-based for convenience
        idx = node2idx([i + 1], DOF)
        F[idx[0]] = Fx[i]
        F[idx[1]] = Fy[i]

    # boundary condition
    idx = np.squeeze(np.where(rigid))
    # add 1 b.c. made indexing 1-based for convenience
    remove = node2idx(idx + 1, DOF)

    K = np.delete(K, remove, axis=0)
    K = np.delete(K, remove, axis=1)
    F = np.delete(F, remove, axis=0)
    S = np.delete(S, remove, axis=1)

    # solve for deflections
    d = np.linalg.solve(K, F)

    # compute stress
    stress = np.dot(S, d).reshape(nbar)

    return mass, stress, K, np.squeeze(d), S


def tenbartruss(A, grad_method='FD', aggregate=False):
    """This is the subroutine for the 10-bar truss.
    TODO: You will need to complete it.

    Parameters
    ----------
    A : ndarray of length 10
        cross-sectional areas of all the bars
    grad_method : string (optional)
        gradient type.
        'FD' for finite difference,
        'CS' for complex step,
        'DT' for direct method,
        'AJ' for adjoint method,
        'AD' for automatic differentiation (extra credit).
    aggregate : bool (optional)
        If True, return the KS-aggregated stress constraint. If False, do not aggregate and return all stresses.
        The derivatives implementation for `aggreagate`=True is optional (extra credit).

    Outputs
    -------
    mass : float
        mass of the entire structure
    stress : ndarray of length 10 (if `aggregate`=False); float (if `aggregate`=True)
        stress of each bar or KS-aggregated stress value
    dmass_dA : ndarray of length 10
        derivative of mass w.r.t. each A
    dstress_dA : 10 x 10 ndarray (if `aggregate`=False); ndarray of length 10 if `aggregate`=True
        If `aggregated`=False, dstress_dA[i, j] is derivative of stress[i] w.r.t. A[j]
        If `aggregated`=True,  dstress_dA[j] is derivative of the KS-aggregated stress w.r.t. A[j]
    """

    # --- setup 10 bar truss ----
    # Truss node indexing:
    # wall > 1 ---------- 2 ---------- 3
    #          ++      ++ | ++      ++ |
    #            ++  ++   |   ++  ++   |
    #              ++     |     ++     |
    #            ++  ++   |   ++  ++   |
    #          ++      ++ | ++      ++ |
    # wall > 4 ---------- 5 ---------- 6

    # define bars by [node1, node2]
    bars_node = [
        [1, 2],   # bar 1
        [2, 3],   # bar 2 ...
        [4, 5],
        [5, 6],
        [2, 5],
        [3, 6],
        [1, 5],
        [2, 4],
        [2, 6],
        [3, 5]
    ]

    # arrays of the 1st and 2nd nodes
    nodes1 = []
    nodes2 = []
    for bar in bars_node:
        nodes1.append(bar[0])
        nodes2.append(bar[1])

    # bar orientations
    phi = np.deg2rad(np.array([0, 0, 0, 0, -90, -90, -45, -135, -45, -135]))

    # bar lengths
    bar_l = 10  # m
    ld = bar_l * np.sqrt(2)    # length of diagonal bars
    L = np.array([bar_l, bar_l, bar_l, bar_l, bar_l, bar_l, ld, ld, ld, ld])

    # Young Modulus of each bar
    E = np.ones(10) * 70 * 10**9  # Pa

    # density of each bar
    rho = np.ones(10) * 2720  # kg/m^3

    # external loads
    P = 5 * 10**5     # N
    Fx = np.zeros(6)
    Fy = np.array([0, 0, 0, 0, -P, -P])

    # boundary condition (set True for clamped nodes)
    rigid = [True, False, False, True, False, False]

    # --- call truss function ----
    # This will compute the mass and stress of your truss structure
    mass, stress, K, d, S = truss(
        nodes1, nodes2, phi, A, L, E, rho, Fx, Fy, rigid)

    # --- compute derivatives for provided grad_type ----
    num_bars = len(bars_node)
    # df/dx total 10x10
    dmass_dA = np.zeros(num_bars)
    # df/dx total 10x10
    dstress_dA = np.zeros((num_bars, num_bars))
    # dr/dx partial 8x10
    # starting as the transposed dims(10x8) for ease of programming, will transpose later
    # dK_dA = np.zeros((num_bars, np.shape(K)[0]))
    # phi for direct, 8x10
    phi_dir = np.zeros((num_bars, np.shape(K)[0]))
    # psi for adjoint, 10x8, dont need to be transposed cos we solve row by row
    psi_adj = np.zeros((num_bars, np.shape(K)[0]))
    if grad_method == 'FD':
        # h_fd = np.max([math.ulp(s)**(1/2) for s in stress])
        h_fd = 1e-8
        for bar in range(num_bars):
            h_bar = h_fd * (1 + np.abs(A[bar]))
            A_high = A.copy()
            A_high[bar] += h_bar
            mass_high, stress_high, _, _, _ = truss(
                nodes1, nodes2, phi, A_high, L, E, rho, Fx, Fy, rigid)
            dmass_dA[bar] = (mass_high - mass)/h_bar
            dstress_dA[bar] = (stress_high - stress)/h_bar
        dmass_dA = dmass_dA.T
        dstress_dA = dstress_dA.T

    elif grad_method == 'CS':
        h_cplx = 1e-200
        for bar in range(num_bars):
            h = np.zeros(num_bars, dtype="complex")
            h[bar] = complex(0, h_cplx)
            A_high = A.copy()
            A_high = A_high + h
            mass_cplx, stress_cplx, _, _, _ = truss(
                nodes1, nodes2, phi, A_high, L, E, rho, Fx, Fy, rigid)
            dmass_dA[bar] = np.imag(mass_cplx)/h_cplx
            dstress_dA[bar] = np.imag(stress_cplx)/h_cplx
        dmass_dA = dmass_dA.T
        dstress_dA = dstress_dA.T

    elif grad_method == 'DT':
        # h_fd = np.max([math.ulp(k.real)**(1/2) for k in K.flatten()])
        h_fd = 1e-8
        for bar in range(num_bars):
            h_bar = h_fd * (1 + np.abs(A[bar]))
            A_high = A.copy()
            A_high[bar] += h_bar
            _, _, K_high, d_high, _ = truss(
                nodes1, nodes2, phi, A_high, L, E, rho, Fx, Fy, rigid)
            dK_dA_i = (K_high@d_high - K@d_high)/h_bar
            phi_dir[bar] = np.linalg.solve(K, dK_dA_i)

        dstress_dA = np.dot(-S, phi_dir.T)

    elif grad_method == 'AJ':
        # h_fd = np.max([math.ulp(k.real)**(1/2) for k in K.flatten()])
        h_fd = 1e-8
        dK_dA = np.zeros((num_bars, np.shape(K)[0]))
        for bar in range(num_bars):
            h_bar = h_fd * (1 + np.abs(A[bar]))
            A_high = A.copy()
            A_high[bar] += h_bar
            _, _, K_high, d_high, S = truss(
                nodes1, nodes2, phi, A_high, L, E, rho, Fx, Fy, rigid)
            dK_dA[bar] = (K_high@d_high - K@d_high)/h_bar
            psi_adj[bar] = np.linalg.solve(K, S[bar])

        dstress_dA = np.dot(-psi_adj, dK_dA.T)

    return mass, stress, dmass_dA, dstress_dA
