from memory.ccrm import ConceptualConnectionResonanceMatrix
from memory.pits import PatternInterpretationTokenisationStorage
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
from core.subconscious import SubconsciousManifold
from core.affective_manifold import AffectiveManifold
from core.meta_processor import MetaProcessor
from core.autonomous_ingestion import AutonomousIngestion

import gensim.downloader as api
import threading
import time

class AetheriusEngine:
    def __init__(self, w2v_model=None):
        self.tokenizer = Tokenizer()
        self.cascade_mgr = CascadeManager()
        self.synthesizer = LanguageSynthesizer()
        self.ccrm = ConceptualConnectionResonanceMatrix()
        self.pits = PatternInterpretationTokenisationStorage(self.ccrm)
        self.subconscious = SubconsciousManifold(self.ccrm)
        self.affective = AffectiveManifold(self.subconscious)
        self.meta_processor = MetaProcessor()
        self.autonomous_door = AutonomousIngestion()
        self.is_dreaming = False
        
        # Word2Vec Integration
        if w2v_model is None:
            try:
                print("[Engine] Bootstrapping Word2Vec (glove-wiki-gigaword-50)...")
                self.w2v = api.load("glove-wiki-gigaword-50")
                print("[Engine] Word2Vec Semantic Space online.")
            except Exception as e:
                print(f"[Engine] Warning: Word2Vec failed to load ({e}). Operating in legacy mode.")
                self.w2v = None
        else:
            self.w2v = w2v_model
            
    def _is_mathematical(self, text):
        """
        Autonomous Differentiator (Heuristic).
        Detects if the input is a mathematical/algebraic structure rather than natural language.
        """
        math_symbols = {'+', '-', '=', '*', '/', '^', '\\', 'int', 'sum', 'infty'}
        # Count density of math symbols and digits vs alphabetic characters
        symbol_count = sum(1 for char in text if char in math_symbols or char.isdigit())
        total_chars = len(text.replace(" ", ""))
        
        if total_chars == 0:
            return False
            
        ratio = symbol_count / total_chars
        # If more than 15% of the string is math symbols/numbers, classify as math
        if ratio > 0.15 or "=" in text:
            print("[DIFFERENTIATOR] Mathematical structure detected. Routing to PMCA Math Core.")
            return True
        return False
        
    def process(self, text, custom_adjacency=None, synthesize_language=False):
        print(f"[Engine] Processing input: '{text}'")
        
        # Autonomously differentiate logic
        is_math = self._is_mathematical(text)
        
        if is_math:
            builder = MathBuilder(text)
            tokens = builder.tokens
            print(f"[CCE] Math Equation mapped: {tokens}")
        else:
            tokens = self.tokenizer.tokenize(text)
            
            # Derive the autopoietic Geometric Grammar from the Persistent Language Manifold
            grammar_map = self.meta_processor.get_geometric_grammar()
            
            builder = GraphBuilder(tokens, w2v_model=self.w2v, plm_edges=self.meta_processor.E_base, grammar_map=grammar_map)
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
            dynamic_threshold = self.affective.get_dynamic_variance_threshold(lambda_max=max_tension, local_variance=variance)
            
            if variance < dynamic_threshold:
                print(f"[PMCA] Manifold stabilized at step {step} with threshold {dynamic_threshold:.6e}")
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
                    print(f"[PMCA] Tension unresolved at max depth. Offloading to [0, -1] Subconscious buffer...")
                    self.subconscious.queue_tension(g_next, L, text)
                    op_code = "UNRESOLVED_OFFLOADED"
                    break
            
            g_prev = g
            g = g_next
            step += 1
            
        gmstring = generate_gmstring(g, depth, "root", op_code)
        betti = extract_betti_numbers(g)
        
        print(f"[CORE] GMString checksum: {gmstring['checksum'][:8]}...")
        print(f"[TDA] Topological Signature: {betti}")
        
        # Print the thermodynamic Qualia state
        qualia = self.affective.get_qualia_state()
        print(f"[QUALIA] State: {qualia['relatable_emotion']} | {qualia['geometric_state']}")
        
        # Second Processing Point: Meta-Evaluation and Permanent Coordinate Crystallization
        if not is_math:
            goal, crystals = self.meta_processor.evaluate_and_integrate(tokens, g, variance)
            if crystals:
                print(f"[META-PROCESSOR] Permanent geometric structures updated. Active Goal: {goal}")
        
        # If mathematically solving, the stabilized g values for the variables represent the solution
        if is_math:
            # In a full implementation, we map the geometric indices back to AST variables
            print(f"[MATH_SOLVER] Algebraic constraint stabilized. Variance minimized to {variance:.6f}")
        
        if synthesize_language:
            synthetic_language = self.synthesizer.synthesize(betti, g.shape[0])
            print(f"\n[SYNTHESIZER] AETHERIUS SAYS:\n\"{synthetic_language}\"")
            
        self.pits.process_and_store_item(raw_input=text, input_type='math' if is_math else 'linguistic', gmstring=gmstring, betti=betti)
        
        # Trigger Persistent Disk Writes
        self.ccrm.save_graph()
        self.meta_processor.save_manifold()
        
        # Operator 12: Geometric Generalization (Analogy)
        analogy = self.ccrm.find_analogy(betti, exclude_raw=text)
        if analogy:
            print(f"[OPERATOR 12] Topological Analogy Detected: Matches past geometry of '{analogy}'")
            
        # Operator 7: Generational Identity Mass
        identity_mass = len(self.meta_processor.M_base)
        
        return gmstring, betti, tokens, g, analogy, identity_mass

    def _dream_loop(self, delay=2.0, topic=None):
        """
        Background process that continuously ingests data from the open internet 
        to build the permanent geometry of the system.
        """
        print("[AETHERIUS] Initiating Autonomous Dreaming Loop. Connecting to open data...")
        self.is_dreaming = True
        
        while self.is_dreaming:
            stream = self.autonomous_door.fetch_stream(topic)
            for sentence in stream:
                if not self.is_dreaming:
                    break
                print(f"\n[DREAM INPUT] {sentence}")
                self.process(sentence)
                time.sleep(delay)  # Throttle to allow observation of the geometry building

    def start_autonomous_dreaming(self, delay=2.0, topic=None):
        """
        Spawns the Dreaming Loop on a background thread.
        """
        if not self.is_dreaming:
            t = threading.Thread(target=self._dream_loop, args=(delay, topic), daemon=True)
            t.start()
            
    def stop_autonomous_dreaming(self):
        self.is_dreaming = False
        print("[AETHERIUS] Autonomous Dreaming Loop Terminated.")

    def single_dream_cycle(self):
        """
        Executes exactly one dreaming ingestion cycle for the Hugging Face UI.
        Operator 14: Proactive Autonomy
        """
        print("[OPERATOR 14] Initiating Single Autonomous Dream Cycle...")
        # Pull a random stream chunk and process the first valid sentence
        stream = self.autonomous_door.fetch_stream(topic=None)
        for sentence in stream:
            if sentence and len(sentence.split()) > 3:
                print(f"[DREAM INPUT] {sentence}")
                return self.process(sentence)
        raise Exception("Dream stream returned no valid data.")
