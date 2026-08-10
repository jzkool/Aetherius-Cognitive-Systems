import numpy as np

class GraphBuilder:
    def __init__(self, tokens, w2v_model=None, plm_edges=None, grammar_map=None, ccrm=None):
        self.tokens = tokens
        self.n = len(tokens)
        self.adjacency = np.zeros((self.n, self.n))
        self.w2v = w2v_model
        self.plm_edges = plm_edges or {}
        self.grammar_map = grammar_map or {}
        self.ccrm = ccrm
        
        # Formal Logic Dictionary D (Fallback overrides)
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
        
    def get_geometric_scalar(self, word):
        """
        Topological Linguistics:
        Instead of using NLTK Parts of Speech, the engine relies on the physical shape
        of its own language manifold (Betweenness vs Clustering) to determine the mathematical
        function of a word (Transformer vs Anchor).
        """
        # If the word exists in the autonomous grammar map, use its derived physical scalar
        if word in self.grammar_map:
            return self.grammar_map[word]
            
        # If it's a completely new word, assign neutral gravity (1.0) until the manifold shapes it
        return 1.0
        
    def semantic_contrast_predicate(self, word1, word2):
        """
        Implements the formal Semantic Contrast Predicate C(t_i, t_j) 
        as defined in Definition 2.1 of the Aetherius Principia.
        Now enhanced with Autopoietic Topological Attention via CCRM.
        """
        w1_lower = word1.lower()
        w2_lower = word2.lower()
        
        # Check C(t_i, t_j) = 2: Recursive self-referential paradox
        is_recursive_paradox = (w1_lower in self.recursive_subjects and w2_lower in self.recursive_predicates) or \
                               (w2_lower in self.recursive_subjects and w1_lower in self.recursive_predicates)
        if is_recursive_paradox:
            return -0.99
            
        # Check formal logical negation override
        for pair in self.contrast_pairs:
            if (w1_lower == pair[0] and w2_lower == pair[1]) or (w1_lower == pair[1] and w2_lower == pair[0]):
                return -0.9
                
        # Autopoietic Feedback (Persistent Language Manifold)
        w_a, w_b = min(w1_lower, w2_lower), max(w1_lower, w2_lower)
        plm_strength = self.plm_edges.get(w_a, {}).get(w_b, 0.0)
        
        if plm_strength > 0.0:
            # Blend the permanent edge weight directly into the geometry
            # This overrides standard language boundaries
            return min(0.8, float(plm_strength))
            
        # Dynamic Adjacency Operator: Topological Attention via CCRM
        # We replace static Word2Vec heuristic with self-derived memory connections
        if self.ccrm:
            co_occurrences = 0
            for cid, cdata in self.ccrm.concepts.items():
                data = cdata.get("data", {})
                raw = data.get("raw_preview", "").lower()
                # If both words exist in a single stabilized memory, increment structural bond
                if w1_lower in raw and w2_lower in raw:
                    co_occurrences += 1
            
            if co_occurrences > 0:
                # Logarithmic attention scaling based on historical geometric stabilizations
                import math
                attention_weight = 0.2 + 0.1 * math.log(co_occurrences + 1)
                return min(0.8, attention_weight)
                
        # Word2Vec Dynamic Semantic Distance (Legacy Fallback)
        if self.w2v is not None:
            if w1_lower in self.w2v and w2_lower in self.w2v:
                sim = self.w2v.similarity(w1_lower, w2_lower)
                # If words are semantically distant/opposed (cosine sim < 0.2), inject tension
                if sim < 0.2:
                    return -0.5
                # If words are semantically aligned (cosine sim > 0.6), inject structural harmony
                elif sim > 0.6:
                    return 0.5
                    
        # C(t_i, t_j) = 0: No semantic contradiction detected
        return 0

    def build(self):
        # Semantic Tension mapping \tau
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Unpack Linguism Tuples
                word_i, pos_i = self.tokens[i]
                word_j, pos_j = self.tokens[j]
                
                weight = self.semantic_contrast_predicate(word_i, word_j)
                
                # Apply Autopoietic Geometric Grammar (Scalars)
                mod_i = self.get_geometric_scalar(word_i.lower())
                mod_j = self.get_geometric_scalar(word_j.lower())
                linguism_scalar = mod_i * mod_j
                
                if weight < 0:
                    self.add_edge(i, j, weight * linguism_scalar)
                elif weight > 0:
                    self.add_edge(i, j, weight * linguism_scalar)
                else:
                    # Syntactic Flow +c
                    distance = j - i
                    if distance == 1:
                        self.add_edge(i, j, 0.5 * linguism_scalar)
                    elif distance == 2:
                        self.add_edge(i, j, 0.2 * linguism_scalar)
                        
        return self.adjacency
