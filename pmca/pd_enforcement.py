import jax.numpy as jnp
from jax import jit

@jit
def enforce_positive_definiteness(g, epsilon=1e-4):
    """
    Localized Ricci-DeTurck constraint. 
    Instead of inflating the entire manifold by shifting the spectrum, 
    we clip only the collapsed (negative) dimensions to preserve global topological volume.
    """
    eigenvalues, eigenvectors = jnp.linalg.eigh(g)
    clipped_eigenvalues = jnp.maximum(eigenvalues, epsilon)
    
    # Reconstruct the metric tensor: g = Q * Lambda * Q^T
    g_new = jnp.dot(eigenvectors, jnp.dot(jnp.diag(clipped_eigenvalues), eigenvectors.T))
    
    # Ensure exact symmetry
    g_new = (g_new + g_new.T) / 2.0
    return g_new
