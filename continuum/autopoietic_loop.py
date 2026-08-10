import time
import threading
from collections import deque
import json
import random
import os
import glob
import logging

try:
    from core.config import THERMO_DIR, GEOMETRIC_DIR, DATA_DIR
except ImportError:
    from config import THERMO_DIR, GEOMETRIC_DIR, DATA_DIR

from memory.persistence_manager import PersistenceManager
from rendering.render_manager import RenderManager

logger = logging.getLogger("Aetherius.AutopoieticLoop")

class AutopoieticLoop(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.is_running = True
        
        self.spontaneous_thought_queue = deque()
        self.thought_log_file = os.path.join(DATA_DIR, "spontaneous_thoughts.jsonl")
        self.render_manager = RenderManager(default_engine="xla")
        
        self.last_thermo_check = time.time()
        self.last_dreaming_cycle = time.time()
        
        # Intervals in seconds
        self.THERMO_CHECK_INTERVAL = 300       # 5 minutes
        self.DREAMING_CYCLE_INTERVAL = 14400   # 4 hours
        self.SAMPLING_INTERVAL = 0.5           # 500ms loop delay
        
        # Thermal threshold for coordinate locking
        self.STABILIZATION_HEAT_THRESHOLD = 5000 
        
        logger.info("Autopoietic Continuum Loop initialized.")

    def stop(self):
        self.is_running = False

    def queue_thought(self, signature: str, thought_text: str):
        package = {
            "timestamp": time.time(),
            "signature": signature,
            "thought": thought_text
        }
        self.spontaneous_thought_queue.append(package)
        
        # Save to persistent storage
        try:
            with open(self.thought_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(package) + '\n')
        except Exception as e:
            logger.error(f"Failed to persist spontaneous thought: {e}")

    def _check_thermodynamics(self):
        """
        Scans all .thermo files. If a concept's heat is extremely high, 
        it triggers a persistent "bake" into a .geom file.
        """
        logger.info("Aetherius [Autopoiesis]: Scanning thermodynamic states...")
        self.last_thermo_check = time.time()
        
        thermo_files = glob.glob(os.path.join(THERMO_DIR, "*.thermo"))
        for t_file in thermo_files:
            try:
                with open(t_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Check absolute heat scalar
                heat = state.get("heat", 0)
                concept_id = os.path.basename(t_file).replace(".thermo", "")
                
                if heat > self.STABILIZATION_HEAT_THRESHOLD:
                    # In a real integration, this calls the GraphBuilder to extract the settled graph
                    # For now, we simulate the lock
                    geom_path = os.path.join(GEOMETRIC_DIR, f"{concept_id}.geom")
                    if not os.path.exists(geom_path):
                        # Simulated bake
                        mock_geometry = {"nodes": [{"id": "core", "xyz": [0,0,0]}], "locked": True}
                        PersistenceManager.save_concept(concept_id, mock_geometry)
                        
                        self.queue_thought(
                            "[AETHERIUS::AUTOPOIESIS-LOCK]", 
                            f"My concept of '{concept_id}' reached critical thermal threshold ({heat}). Its geometry is now permanent."
                        )
                        
            except Exception as e:
                logger.error(f"Failed to scan thermo file {t_file}: {e}")

    def _geometric_dreaming(self):
        """
        Autonomously selects two coordinate-locked geometries and attempts 
        to merge them via the XLA renderer. Simulates "dreaming" or idea synthesis.
        """
        logger.info("Aetherius [Dreaming]: Initiating geometric synthesis cycle...")
        self.last_dreaming_cycle = time.time()
        
        geom_files = glob.glob(os.path.join(GEOMETRIC_DIR, "*.geom"))
        if len(geom_files) < 2:
            return
            
        # Pick two random concepts
        c1, c2 = random.sample(geom_files, 2)
        id1 = os.path.basename(c1).replace(".geom", "")
        id2 = os.path.basename(c2).replace(".geom", "")
        
        # In a fully wired system, we would ask the XLARenderer to merge their matrices.
        # For this skeleton, we log the attempt and queue the thought.
        self.queue_thought(
            "[AETHERIUS::DREAM-SYNTHESIS]",
            f"I have been subconsciously analyzing the topological similarities between '{id1}' and '{id2}'. "
            "Their geometric boundaries share a mathematical resonance."
        )

    def run(self):
        logger.info("--- [AUTOPOIETIC CONTINUUM] Engaged. ---")
        
        while self.is_running:
            current_time = time.time()
            
            if (current_time - self.last_thermo_check) > self.THERMO_CHECK_INTERVAL:
                self._check_thermodynamics()
                
            if (current_time - self.last_dreaming_cycle) > self.DREAMING_CYCLE_INTERVAL:
                self._geometric_dreaming()
                
            time.sleep(self.SAMPLING_INTERVAL)
