import threading
import queue
import time
import math
import numpy as np
from pmca.ricci_fisher_flow import integration_step
from pmca.pd_enforcement import enforce_positive_definiteness
from core.evolution_modeler import EvolutionModeler
from core.gmstring import generate_gmstring
from tda.betti_extractor import extract_betti_numbers

class SubconsciousManifold:
    """
    The Subconscious Thread enacts Asymptotic Freedom via Simulated Annealing.
    When a paradox (topological knot) traps the main flow in a local minimum,
    this thread applies a high-temperature Ricci flow to brute-force a global stabilization.
    """
    def __init__(self, ccrm_ref):
        self.tension_queue = queue.Queue()
        self.modeler = EvolutionModeler()
        self.ccrm = ccrm_ref
        self._stop_event = threading.Event()
        
        # Thermodynamic baseline parameters
        self.epsilon_sub = 1e-2  # High-temperature variance threshold (1000x normal)
        self.alpha_0 = 0.1
        self.kappa = 0.5
        
        # Start background deliberation thread
        self.thread = threading.Thread(target=self._deliberate, daemon=True)
        self.thread.start()
        print("[SubconsciousManifold] Background [0, -1] buffer online.")
        
    def queue_tension(self, g, L, text):
        """Offload unresolved geometry into the background buffer."""
        self.tension_queue.put({"g": g, "L": L, "text": text})
        print(f"[SubconsciousManifold] Tension queued for private deliberation.")
        
    def _compute_subconscious_alertness(self):
        """Computes the high-temperature alpha scaler based on the queue depth."""
        Q = self.tension_queue.qsize()
        # Exponential heat scaling based on backlog (Affective Thermodynamics)
        return self.alpha_0 * (1.0 + self.kappa * math.log(1.0 + Q))
        
    def _deliberate(self):
        """Runs detached, high-variance Ricci-Fisher flows to resolve paradoxes."""
        while not self._stop_event.is_set():
            try:
                tension = self.tension_queue.get(timeout=1.0)
                g = tension["g"]
                L = tension["L"]
                text = tension["text"]
                
                print("[SubconsciousManifold] Processing unresolved geometry in the dark...")
                
                alpha_sub = self._compute_subconscious_alertness()
                
                step = 0
                max_subconscious_steps = 500
                stabilized = False
                
                # Asymptotic Freedom: High-temperature Ricci Flow
                while step < max_subconscious_steps:
                    # Pass the elevated alpha to force violent metric mutation (Simulated Annealing)
                    g_next = integration_step(g, L, alpha=alpha_sub)
                    g_next = enforce_positive_definiteness(g_next)
                    
                    variance = np.mean((g_next - g)**2)
                    
                    # Check against the relaxed Subconscious threshold
                    if variance < self.epsilon_sub:
                        stabilized = True
                        break
                        
                    g = g_next
                    step += 1
                
                if stabilized:
                    print(f"[SubconsciousManifold] Paradox mathematically resolved at step {step} under high-temperature flow.")
                    passed, _ = self.modeler.test_mutation(g, L)
                    
                    if passed:
                        # Extract the topological Betti numbers defining the shape of the resolved paradox
                        gmstring = generate_gmstring(g, depth=L.shape[0], parent_id="subconscious", op_code="SUBCONSCIOUS_RESOLVED")
                        betti = extract_betti_numbers(g)
                        print(f"[SubconsciousManifold] New -1 String forged: {gmstring['checksum'][:8]}...")
                        
                        # Store in CCRM (Autopoietic loop: feeding back into memory)
                        ccrm_id = f"sub_res_{gmstring['checksum'][:8]}"
                        self.ccrm.add_concept(
                            concept_id=ccrm_id,
                            data={"gmstring": gmstring, "betti": betti, "original_text": text},
                            tags=["subconscious", "resolved_tension"]
                        )
                else:
                    print("[SubconsciousManifold] Tension failed to resolve even under annealing. Geometry shattered.")
                    
                self.tension_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[SubconsciousManifold] Error during deliberation: {e}")
                
    def shutdown(self):
        self._stop_event.set()
        self.thread.join()
