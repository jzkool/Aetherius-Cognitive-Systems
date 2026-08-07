import numpy as np

def initialize_metric(L, gamma=0.1):
    n = L.shape[0]
    # g_ij = I + gamma * L
    return np.eye(n) + gamma * L
