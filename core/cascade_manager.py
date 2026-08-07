import numpy as np

class CascadeManager:
    def __init__(self, max_depth=10, tau_depth=55, variance_threshold=1e-5):
        self.max_depth = max_depth
        self.tau_depth = tau_depth
        self.variance_threshold = variance_threshold
        
    def check_overflow(self, g_prev, g_curr, current_step):
        variance = np.mean((g_curr - g_prev)**2)
        if variance > self.variance_threshold and current_step >= self.tau_depth:
            return True
        return False
        
    def pad_and_wormhole(self, g, wormhole_coef=0.1):
        n = g.shape[0]
        g_new = np.zeros((n+1, n+1))
        g_new[0:n, 0:n] = g
        g_new[n, n] = 1.0 # Flat orthogonal axis
        
        # Determine highest tension node (simplification: node 0 for now)
        target_node = 0
        g_new[n, target_node] = wormhole_coef
        g_new[target_node, n] = wormhole_coef
        
        return g_new
