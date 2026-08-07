import numpy as np

class GraphBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.n = len(tokens)
        self.adjacency = np.zeros((self.n, self.n))
        
    def add_edge(self, t1_idx, t2_idx, weight):
        self.adjacency[t1_idx, t2_idx] = weight
        self.adjacency[t2_idx, t1_idx] = weight
        
    def build(self):
        # In a full system, this would use a semantic DB to assign weights.
        # For prototype, we expect manual or rule-based injection.
        return self.adjacency
