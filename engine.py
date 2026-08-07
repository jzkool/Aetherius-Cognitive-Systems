import numpy as np
from cce.tokenizer import Tokenizer
from cce.graph_builder import GraphBuilder
from cce.laplacian import compute_laplacian, compute_tension
from pmca.manifold import initialize_metric
from pmca.ricci_fisher_flow import integration_step
from pmca.pd_enforcement import enforce_positive_definiteness
from core.cascade_manager import CascadeManager
from core.gmstring import generate_gmstring
from tda.betti_extractor import extract_betti_numbers

class AetheriusEngine:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.cascade_mgr = CascadeManager()
        
    def process(self, text, custom_adjacency=None):
        print(f"[Engine] Processing input: '{text}'")
        tokens = self.tokenizer.tokenize(text)
        print(f"[CCE] Tokens mapped: {tokens}")
        
        builder = GraphBuilder(tokens)
        if custom_adjacency is not None:
            builder.adjacency = custom_adjacency
        
        A = builder.build()
        L, _ = compute_laplacian(A)
        _, max_tension = compute_tension(L)
        print(f"[CCE] Laplacian computed. Max Tension: {max_tension:.4f}")
        
        g = initialize_metric(L)
        print(f"[PMCA] Manifold initialized at D={g.shape[0]}")
        
        depth = 0
        step = 0
        g_prev = g.copy()
        
        while True:
            # Ricci-Fisher Flow
            g_next = integration_step(g, L)
            g_next = enforce_positive_definiteness(g_next)
            
            variance = np.mean((g_next - g)**2)
            
            # Check stabilization
            if variance < 1e-5:
                print(f"[PMCA] Manifold stabilized at step {step}")
                op_code = "STABLE"
                break
                
            # Check overflow
            if self.cascade_mgr.check_overflow(g, g_next, step):
                print(f"[CORE] Chaos Overflow detected at step {step}!")
                print(f"[CORE] Triggering Dual-Conal Cascade...")
                g_next = self.cascade_mgr.pad_and_wormhole(g_next)
                
                # Expand L to match new dimension so Fisher anchor doesn't crash
                new_L = np.zeros_like(g_next)
                new_L[0:L.shape[0], 0:L.shape[0]] = L
                L = new_L
                
                depth += 1
                step = 0 # Reset flow for new dimension
                print(f"[PMCA] Restarting flow at D={g_next.shape[0]}")
                if depth >= self.cascade_mgr.max_depth:
                    print(f"[CORE] Max depth reached. Forcing stability.")
                    op_code = "FORCE_STABLE"
                    break
            
            g_prev = g
            g = g_next
            step += 1
            
        gmstring = generate_gmstring(g, depth, "root", op_code)
        print(f"[CORE] GMString generated with checksum: {gmstring['checksum'][:8]}...")
        
        betti = extract_betti_numbers(g)
        print(f"[TDA] Topological Signature Extracted: {betti}")
        
        return gmstring, betti
