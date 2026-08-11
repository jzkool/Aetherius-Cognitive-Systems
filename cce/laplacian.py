import numpy as np

def compute_laplacian(adjacency):
    degree_vec = np.sum(np.abs(adjacency), axis=1)
    degree = np.diag(degree_vec)
    L = degree - adjacency
    
    # Compute Symmetric Normalized Laplacian: D^{-1/2} L D^{-1/2}
    with np.errstate(divide='ignore'):
        d_inv_sqrt = np.power(degree_vec, -0.5)
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
    D_inv_sqrt = np.diag(d_inv_sqrt)
    
    L_sym = D_inv_sqrt @ L @ D_inv_sqrt
    return L_sym, degree

def compute_tension(L):
    eigenvalues, _ = np.linalg.eigh(L)
    return eigenvalues, np.max(eigenvalues)
