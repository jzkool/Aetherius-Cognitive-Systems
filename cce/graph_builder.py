import numpy as np

class GraphBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.n = len(tokens)
        self.adjacency = np.zeros((self.n, self.n))
        
        # Lightweight Semantic Contrast Dictionary (Negative Curvature Injectors)
        self.contrast_pairs = [
            ("truth", "lie"), ("real", "false"), ("create", "destroy"),
            ("light", "dark"), ("good", "evil"), ("up", "down"),
            ("hot", "cold"), ("beginning", "end"), ("order", "chaos")
        ]
        
    def add_edge(self, t1_idx, t2_idx, weight):
        self.adjacency[t1_idx, t2_idx] = weight
        self.adjacency[t2_idx, t1_idx] = weight
        
    def check_contrast(self, word1, word2):
        for pair in self.contrast_pairs:
            if (word1 == pair[0] and word2 == pair[1]) or (word1 == pair[1] and word2 == pair[0]):
                return -0.9 # Extreme tension
        return 0.0

    def build(self):
        # Dynamic Heuristic Engine
        for i in range(self.n):
            for j in range(i + 1, self.n):
                word_i = self.tokens[i]
                word_j = self.tokens[j]
                
                # 1. Check for explicit semantic contradiction
                contrast_weight = self.check_contrast(word_i, word_j)
                if contrast_weight != 0:
                    self.add_edge(i, j, contrast_weight)
                    continue
                
                # 2. Syntactic Proximity (Flow)
                distance = j - i
                if distance == 1:
                    self.add_edge(i, j, 0.5) # Adjacent flow
                elif distance == 2:
                    self.add_edge(i, j, 0.2) # Secondary association
                    
        return self.adjacency
