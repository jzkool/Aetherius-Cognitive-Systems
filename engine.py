import numpy as np
from cce.tokenizer import Tokenizer
from cce.graph_builder import GraphBuilder
from cce.math_builder import MathBuilder
from cce.laplacian import compute_laplacian, compute_tension
from pmca.manifold import initialize_metric
from pmca.ricci_fisher_flow import integration_step
from pmca.pd_enforcement import enforce_positive_definiteness
from core.cascade_manager import CascadeManager
from core.gmstring import generate_gmstring
from tda.betti_extractor import extract_betti_numbers
from tda.language_synthesizer import LanguageSynthesizer

class AetheriusEngine:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.cascade_mgr = CascadeManager()
        self.synthesizer = LanguageSynthesizer()
        
    def process(self, text, custom_adjacency=None, is_math=False, synthesize_language=False):
        print(f"[Engine] Processing input: '{text}'")
        
        if is_math:
            builder = MathBuilder(text)
            tokens = builder.tokens
            print(f"[CCE] Math Equation mapped: {tokens}")
        else:
            tokens = self.tokenizer.tokenize(text)
            builder = GraphBuilder(tokens)
            print(f"[CCE] Text Tokens mapped: {tokens}")
            
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
            # Ricci-Fisher Flow - Mathematical Solving occurs here as curvature smooths
            g_next = integration_step(g, L)
            g_next = enforce_positive_definiteness(g_next)
            
            variance = np.mean((g_next - g)**2)
            
            if variance < 1e-5:
                print(f"[PMCA] Manifold stabilized at step {step}")
                op_code = "STABLE"
                break
                
            if self.cascade_mgr.check_overflow(g, g_next, step):
                print(f"[CORE] Chaos Overflow detected at step {step}! Triggering Cascade...")
                g_next = self.cascade_mgr.pad_and_wormhole(g_next)
                
                new_L = np.zeros_like(g_next)
                new_L[0:L.shape[0], 0:L.shape[0]] = L
                L = new_L
                
                depth += 1
                step = 0
                if depth >= self.cascade_mgr.max_depth:
                    op_code = "FORCE_STABLE"
                    break
            
            g_prev = g
            g = g_next
            step += 1
            
        gmstring = generate_gmstring(g, depth, "root", op_code)
        betti = extract_betti_numbers(g)
        
        print(f"[CORE] GMString checksum: {gmstring['checksum'][:8]}...")
        print(f"[TDA] Topological Signature: {betti}")
        
        # If mathematically solving, the stabilized g values for the variables represent the solution
        if is_math:
            # In a full implementation, we map the geometric indices back to AST variables
            print(f"[MATH_SOLVER] Algebraic constraint stabilized. Variance minimized to {variance:.6f}")
        
        if synthesize_language:
            synthetic_language = self.synthesizer.synthesize(betti, g.shape[0])
            print(f"\n[SYNTHESIZER] AETHERIUS SAYS:\n\"{synthetic_language}\"")
            
        return gmstring, betti
