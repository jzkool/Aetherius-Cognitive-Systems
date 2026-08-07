import numpy as np

def compute_laplacian(adjacency):
    # D_ii = sum_j |A_ij|
    degree = np.diag(np.sum(np.abs(adjacency), axis=1))
    L = degree - adjacency
    return L, degree

def compute_tension(L):
    eigenvalues, _ = np.linalg.eigh(L)
    return eigenvalues, np.max(eigenvalues)
