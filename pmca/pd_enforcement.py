import numpy as np

def enforce_positive_definiteness(g, epsilon=1e-4):
    eigenvalues, eigenvectors = np.linalg.eigh(g)
    min_eig = np.min(eigenvalues)
    
    if min_eig < epsilon:
        shift = abs(min_eig) + epsilon
        g = g + shift * np.eye(g.shape[0])
        
    return g
