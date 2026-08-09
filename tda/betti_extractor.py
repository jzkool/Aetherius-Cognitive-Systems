import numpy as np
from ripser import ripser

def extract_betti_numbers(g, noise_threshold=0.1):
    """
    Computes exact Vietoris-Rips persistent homology of the metric tensor.
    Returns the Betti numbers (beta_0, beta_1, beta_2).
    """
    n = g.shape[0]
    
    # The metric tensor g represents connection weights/distances.
    # To compute topology, we convert it into a strict distance matrix D.
    # We take the absolute variation and ensure the diagonal (self-distance) is 0.
    D = np.abs(g)
    np.fill_diagonal(D, 0)
    
    # Symmetrize the distance matrix to ensure Ripser compatibility
    D = (D + D.T) / 2
    
    try:
        # Compute persistent homology up to dimension 2
        result = ripser(D, distance_matrix=True, maxdim=2)
        diagrams = result['dgms']
        
        betti = {"beta_0": 0, "beta_1": 0, "beta_2": 0}
        
        # Extract features that survive beyond the noise threshold
        # H0 (Connected Components)
        if len(diagrams) > 0:
            for p in diagrams[0]:
                # Infinite persistence (p[1] == inf) or persistence > threshold
                if p[1] == np.inf or (p[1] - p[0]) > noise_threshold:
                    betti["beta_0"] += 1
                    
        # H1 (Topological Loops / Paradoxes)
        if len(diagrams) > 1:
            for p in diagrams[1]:
                if p[1] == np.inf or (p[1] - p[0]) > noise_threshold:
                    betti["beta_1"] += 1
                    
        # H2 (Dimensional Voids)
        if len(diagrams) > 2:
            for p in diagrams[2]:
                if p[1] == np.inf or (p[1] - p[0]) > noise_threshold:
                    betti["beta_2"] += 1
                    
        return betti
        
    except Exception as e:
        print(f"[TDA Error] Ripser failed to compute homology: {e}. Falling back to zero-state.")
        return {"beta_0": 1, "beta_1": 0, "beta_2": 0}
