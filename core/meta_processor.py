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
        # Threshold for crystallization (when a coordinate becomes a permanent structure)
        self.crystallization_threshold = 5.0
        
        self.storage_path = "./data/meta_manifold.json" if os.path.exists("./data") else "meta_manifold.json"
        self.load_manifold()

    def save_manifold(self):
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.M_base, f)
        except Exception as e:
            print(f"[META-PROCESSOR] Failed to save manifold to {self.storage_path}: {e}")
            
    def load_manifold(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    self.M_base = json.load(f)
                print(f"[META-PROCESSOR] Restored {len(self.M_base)} crystallized coordinates from {self.storage_path}")
            except Exception as e:
                print(f"[META-PROCESSOR] Failed to load manifold from {self.storage_path}: {e}")

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
                    
        # Meta-Goal formulation based on stability
        goal = "STABLE"
        if variance > 0.1:
            print("[META-PROCESSOR] Warning: High variance detected in local manifold. Formulating Goal: Stabilize global geometry.")
            goal = "GOAL_STABILIZE_MANIFOLD"
            
        return goal, crystallized_events
