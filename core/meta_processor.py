import numpy as np
import json
import os

class MetaProcessor:
    """
    The Second Processing Point (Meta-Observer).
    Evaluates, stabilizes, and permanently stores the outputs of the primary geometric cognition engine.
    """
    def __init__(self):
        # Permanent manifold structure: dictionary mapping linguistic concepts to their geometric mass/density
        self.M_base = {}
        # Persistent Language Manifold: Global edge-weight topology connecting concepts
        self.E_base = {}
        # Threshold for crystallization (when a coordinate becomes a permanent structure)
        self.crystallization_threshold = 5.0
        
        self.bucket_dir = "./data"
        self.storage_path = os.path.join(self.bucket_dir, "meta_manifold.json")
        self.edge_storage_path = os.path.join(self.bucket_dir, "language_manifold.json")
        
        # Ensure the persistent bucket directory exists before trying to write to it
        if not os.path.exists(self.bucket_dir):
            try:
                os.makedirs(self.bucket_dir)
            except Exception as e:
                pass
                
        self.load_manifold()

    def save_manifold(self):
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.M_base, f)
            with open(self.edge_storage_path, "w") as f:
                json.dump(self.E_base, f)
            print(f"[META-PROCESSOR] Successfully saved mass manifold and language topology to persistent bucket.")
        except Exception as e:
            print(f"[META-PROCESSOR] CRITICAL FAILURE: Cannot write to persistent bucket. Error: {e}")
            
    def load_manifold(self):
        loaded = None
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    loaded = json.load(f)
                print(f"[META-PROCESSOR] Successfully loaded persistent manifold from bucket.")
            except Exception as e:
                print(f"[META-PROCESSOR] Failed to load from persistent bucket: {e}")
                
        if loaded:
            self.M_base = loaded
            print(f"[META-PROCESSOR] Restored {len(self.M_base)} crystallized coordinates.")
            
        loaded_edges = None
        if os.path.exists(self.edge_storage_path):
            try:
                with open(self.edge_storage_path, "r") as f:
                    loaded_edges = json.load(f)
                print(f"[META-PROCESSOR] Successfully loaded persistent language topology from bucket.")
            except Exception as e:
                print(f"[META-PROCESSOR] Failed to load language topology from bucket: {e}")
                
        if loaded_edges:
            self.E_base = loaded_edges
            print(f"[META-PROCESSOR] Restored {len(self.E_base)} language topology edges.")

    def evaluate_and_integrate(self, tokens, g_resolved, variance):
        """
        Integrates the newly resolved metric tensor (g_resolved) into the permanent manifold.
        Increases the mass of interacted coordinates over time.
        """
        print("[META-PROCESSOR] Evaluating primary engine output for permanent structural embedding...")
        
        crystallized_events = []
        # tokens is a list of (word, pos_tag)
        for i, (word, pos) in enumerate(tokens):
            if word not in self.M_base:
                self.M_base[word] = {
                    'mass': 1.0, 
                    'pos': pos,
                    'crystallized': False
                }
            else:
                # Hebbian reinforcement: The coordinate becomes a permanent structure over amount of times interacted with
                self.M_base[word]['mass'] += 0.5
                
                # Check for crystallization
                if self.M_base[word]['mass'] >= self.crystallization_threshold and not self.M_base[word]['crystallized']:
                    self.M_base[word]['crystallized'] = True
                    crystallized_events.append(word)
                    print(f"[META-PROCESSOR] *CRYSTALLIZATION EVENT*: Coordinate '{word}' has formed a permanent geometric structure in the manifold.")
        
        # Build the Persistent Language Manifold (PLM)
        # Iterate over the upper triangle of the local metric tensor (g_resolved)
        n = len(tokens)
        if g_resolved is not None and g_resolved.shape == (n, n):
            for i in range(n):
                for j in range(i + 1, n):
                    w1, w2 = tokens[i][0], tokens[j][0]
                    # Ensure alphabetical ordering so undirected edge is unique
                    w_a, w_b = min(w1, w2), max(w1, w2)
                    
                    if w_a not in self.E_base:
                        self.E_base[w_a] = {}
                        
                    # Calculate connection strength inversely proportional to final geometric distance
                    distance = g_resolved[i][j]
                    strength = 1.0 / (1.0 + float(distance))
                    
                    # Accumulate strength
                    if w_b not in self.E_base[w_a]:
                        self.E_base[w_a][w_b] = strength
                    else:
                        self.E_base[w_a][w_b] += strength
                    
        # Meta-Goal formulation based on stability
        goal = "STABLE"
        if variance > 0.1:
            print("[META-PROCESSOR] Warning: High variance detected in local manifold. Formulating Goal: Stabilize global geometry.")
            goal = "GOAL_STABILIZE_MANIFOLD"
            
        return goal, crystallized_events
