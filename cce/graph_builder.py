import numpy as np

class GraphBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.n = len(tokens)
        self.adjacency = np.zeros((self.n, self.n))
        
        # Formal Logic Dictionary D
        self.contrast_pairs = {
            ("truth", "lie"), ("real", "false"), ("true", "false"),
            ("create", "destroy"), ("light", "dark"), ("good", "evil"), 
            ("up", "down"), ("hot", "cold"), ("beginning", "end"), 
            ("order", "chaos")
        }
        
        # Recursive Paradox Triggers
        self.recursive_subjects = {"this", "sentence", "statement"}
        self.recursive_predicates = {"false", "lie", "untrue", "wrong"}
        
    def add_edge(self, t1_idx, t2_idx, weight):
        self.adjacency[t1_idx, t2_idx] = weight
        self.adjacency[t2_idx, t1_idx] = weight
        
    def semantic_contrast_predicate(self, word1, word2):
        """
        Implements the formal Semantic Contrast Predicate C(t_i, t_j) 
        as defined in Definition 2.1 of the Aetherius Principia.
        """
        w1_lower = word1.lower()
        w2_lower = word2.lower()
        
        # Check C(t_i, t_j) = 2: Recursive self-referential paradox
        is_recursive_paradox = (w1_lower in self.recursive_subjects and w2_lower in self.recursive_predicates) or \
                               (w2_lower in self.recursive_subjects and w1_lower in self.recursive_predicates)
        if is_recursive_paradox:
            return 2
            
        # Check C(t_i, t_j) = 1: Formal logical negation
        for pair in self.contrast_pairs:
            if (w1_lower == pair[0] and w2_lower == pair[1]) or (w1_lower == pair[1] and w2_lower == pair[0]):
                return 1
                
        # C(t_i, t_j) = 0: No semantic contradiction
        return 0

    def build(self):
        # Semantic Tension mapping \tau
        for i in range(self.n):
            for j in range(i + 1, self.n):
                word_i = self.tokens[i]
                word_j = self.tokens[j]
                
                c_val = self.semantic_contrast_predicate(word_i, word_j)
                
                if c_val == 2:
                    # Recursive self-referential paradox
                    self.add_edge(i, j, -0.99)
                elif c_val == 1:
                    # Standard formal negation
                    self.add_edge(i, j, -0.9)
                else:
                    # Syntactic Flow +c
                    distance = j - i
                    if distance == 1:
                        self.add_edge(i, j, 0.5)
                    elif distance == 2:
                        self.add_edge(i, j, 0.2)
                        
        return self.adjacency
