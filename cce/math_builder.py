import numpy as np

class MathBuilder:
    def __init__(self, equation):
        # Extremely simplified prototype AST tokenizer for algebraic inputs like "x + 2 = 5"
        self.tokens = [t for t in equation.split() if t.strip()]
        self.n = len(self.tokens)
        self.adjacency = np.zeros((self.n, self.n))
        
    def build(self):
        # Math topological weighting rules
        # Equality acts as a strict structural bond (high positive curvature)
        # Operators act as directional edges. Unknown variables inherently lack bounds, causing tension.
        
        for i in range(self.n):
            for j in range(i + 1, self.n):
                t1 = self.tokens[i]
                t2 = self.tokens[j]
                
                # If they are adjacent mathematically
                if j - i == 1:
                    # Binding constants and operators
                    self.adjacency[i, j] = 0.8
                    self.adjacency[j, i] = 0.8
                
                # Absolute bond across the equality sign
                if t1 == "=" or t2 == "=":
                    self.adjacency[i, j] = 1.0
                    self.adjacency[j, i] = 1.0
                    
                # Unknown variables inject negative curvature (tension) to be resolved by the flow
                if t1.isalpha() or t2.isalpha():
                    self.adjacency[i, j] -= 0.5
                    self.adjacency[j, i] -= 0.5
                    
        return self.adjacency
