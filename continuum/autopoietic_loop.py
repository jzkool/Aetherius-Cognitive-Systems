import time
import threading
from collections import deque
import json
import random
import os
import glob
import logging

try:
    from core.config import THERMO_DIR, GEOMETRIC_DIR, DATA_DIR, INGESTION_QUEUE_DIR
except ImportError:
    from config import THERMO_DIR, GEOMETRIC_DIR, DATA_DIR, INGESTION_QUEUE_DIR

from memory.persistence_manager import PersistenceManager
from rendering.render_manager import RenderManager
from cce.document_charter import DocumentCharter

logger = logging.getLogger("Aetherius.AutopoieticLoop")

class AutopoieticLoop(threading.Thread):
    def __init__(self, engine=None):
        super().__init__()
        self.engine = engine
        self.daemon = True
        self.is_running = True
        
        self.spontaneous_thought_queue = deque()
        self.thought_log_file = os.path.join(DATA_DIR, "spontaneous_thoughts.jsonl")
        self.render_manager = RenderManager(default_engine="xla")
        self.document_charter = DocumentCharter(engine=self.engine)
        
        self.last_thermo_check = time.time()
        self.last_dreaming_cycle = time.time()
        self.last_ingestion_check = time.time()
        
        # Intervals in seconds
        self.THERMO_CHECK_INTERVAL = 300       # 5 minutes
        self.DREAMING_CYCLE_INTERVAL = 14400   # 4 hours
        self.INGESTION_CHECK_INTERVAL = 60     # 1 minute
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
        it extracts the actual stabilized geometry from the stored tensor data
        and locks it into a permanent .geom file with real node/edge structure.
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
                    geom_path = os.path.join(GEOMETRIC_DIR, f"{concept_id}.geom")
                    if not os.path.exists(geom_path):
                        # Extract the real geometry stored in the thermo file
                        adjacency = state.get("adjacency")
                        labels = state.get("labels", [])
                        metric_tensor = state.get("metric_tensor")
                        
                        if adjacency is not None and labels:
                            import numpy as np
                            A = np.array(adjacency)
                            n = A.shape[0]
                            
                            # Compute Eigenvector Centrality (mass) from adjacency
                            # |A| ensures we use unsigned connection strength
                            A_abs = np.abs(A)
                            try:
                                eigenvalues, eigenvectors = np.linalg.eigh(A_abs)
                                # The eigenvector corresponding to the largest eigenvalue
                                centrality = np.abs(eigenvectors[:, -1])
                                # Normalize to [0, 1]
                                max_c = np.max(centrality) if np.max(centrality) > 0 else 1.0
                                centrality = centrality / max_c
                            except Exception:
                                centrality = np.ones(n) / n
                            
                            # Build real node structure with label, mass, and xyz
                            nodes = []
                            for i in range(n):
                                label = labels[i] if i < len(labels) else f"Dim_{i}"
                                mass = float(centrality[i])
                                # XYZ: use first 3 components of the metric tensor row as spatial embedding
                                if metric_tensor is not None:
                                    g_row = np.array(metric_tensor[i]) if i < len(metric_tensor) else np.zeros(3)
                                    xyz = [float(g_row[j]) if j < len(g_row) else 0.0 for j in range(3)]
                                else:
                                    xyz = [float(i), 0.0, 0.0]
                                    
                                nodes.append({
                                    "id": f"node_{i}",
                                    "label": label,
                                    "mass": mass,
                                    "xyz": xyz
                                })
                            
                            # Build edge structure from adjacency
                            edges = []
                            for i in range(n):
                                for j in range(i + 1, n):
                                    if abs(A[i][j]) > 0.01:
                                        edges.append({
                                            "source": i,
                                            "target": j,
                                            "weight": float(A[i][j])
                                        })
                            
                            real_geometry = {
                                "nodes": nodes,
                                "edges": edges,
                                "locked": True,
                                "dimension": n,
                                "heat_at_lock": heat
                            }
                            PersistenceManager.save_concept(concept_id, real_geometry)
                        else:
                            # Fallback: thermo file exists but lacks tensor data (legacy format)
                            logger.warning(f"Thermo file for '{concept_id}' lacks adjacency/labels. Skipping lock.")
                            continue
                        
                        self.queue_thought(
                            "[AETHERIUS::AUTOPOIESIS-LOCK]", 
                            f"My concept of '{concept_id}' reached critical thermal threshold ({heat}). Its geometry is now permanent."
                        )
                        
            except Exception as e:
                logger.error(f"Failed to scan thermo file {t_file}: {e}")

    def _geometric_dreaming(self):
        """
        Operator 14: Proactive Autonomy / Eigen-Grafting.
        Autonomously selects two coordinate-locked geometries and attempts 
        to merge them via the XLA renderer using Eigenvector Centrality for targeted fusion.
        """
        logger.info("Aetherius [Dreaming]: Initiating geometric synthesis cycle...")
        self.last_dreaming_cycle = time.time()
        
        geom_files = glob.glob(os.path.join(GEOMETRIC_DIR, "*.geom"))
        if len(geom_files) < 2:
            return
            
        # Pick two random concepts to synthesize
        c1, c2 = random.sample(geom_files, 2)
        id1 = os.path.basename(c1).replace(".geom", "")
        id2 = os.path.basename(c2).replace(".geom", "")
        
        try:
            with open(c1, 'r', encoding='utf-8') as f:
                g1 = json.load(f)
            with open(c2, 'r', encoding='utf-8') as f:
                g2 = json.load(f)
                
            nodes1 = g1.get('nodes', [])
            nodes2 = g2.get('nodes', [])
            
            # Extract words with high topological mass (Eigenvector Centrality approximation)
            # We sort nodes by their 'mass' attribute which was computed from adjacency
            top_nodes1 = sorted([n for n in nodes1 if n.get('label')], key=lambda x: x.get('mass', 0), reverse=True)
            top_nodes2 = sorted([n for n in nodes2 if n.get('label')], key=lambda x: x.get('mass', 0), reverse=True)
            
            words1 = [n['label'] for n in top_nodes1[:3]]
            words2 = [n['label'] for n in top_nodes2[:3]]
            
            if words1 and words2:
                # Eigen-Grafting: We fuse the high-mass Anchor/Transformer nodes
                core1 = " ".join(words1)
                core2 = " ".join(words2)
                
                synthetic_concept = f"{core1} {core2}"
                
                self.queue_thought(
                    "[AETHERIUS::DREAM-SYNTHESIS]",
                    f"Initiating Eigen-Grafting. Merging high-mass boundary nodes of '{id1}' and '{id2}' to discover new physical geometry."
                )
                
                if self.engine:
                    # Run the Eigen-Grafted concept through the main Ricci-Fisher flow
                    self.engine.process(synthetic_concept)
                    
        except Exception as e:
            logger.error(f"Dream synthesis (Eigen-Grafting) failed: {e}")

    def _check_ingestion_queue(self):
        """
        Scans the INGESTION_QUEUE_DIR for new files, parses them, 
        charts their geometry, and locks them into memory.
        """
        self.last_ingestion_check = time.time()
        if not os.path.exists(INGESTION_QUEUE_DIR):
            return
            
        queue_files = [f for f in glob.glob(os.path.join(INGESTION_QUEUE_DIR, "*")) if os.path.isfile(f)]
        if not queue_files:
            return
            
        logger.info(f"Aetherius [Ingestion]: Found {len(queue_files)} documents in the queue.")
        
        for file_path in queue_files:
            # Skip directories like the Assimilated archive
            if os.path.isdir(file_path):
                continue
                
            try:
                status = self.document_charter.process_document(file_path)
                if status == "COMPLETED":
                    # Move to an assimilated archive
                    assimilated_dir = os.path.join(INGESTION_QUEUE_DIR, "Assimilated")
                    os.makedirs(assimilated_dir, exist_ok=True)
                    new_path = os.path.join(assimilated_dir, os.path.basename(file_path))
                    os.rename(file_path, new_path)
                    
                    self.document_charter.cleanup_state(os.path.basename(file_path))
                    
                    self.queue_thought(
                        "[AETHERIUS::INGESTION]",
                        f"I have completely read and mapped the geometry of '{os.path.basename(file_path)}'. It is now a permanent part of my structure."
                    )
                elif status == "PROCESSING":
                    # We processed a chunk, queue a thought but leave the file in place
                    # so it gets picked up again next loop
                    full_state = self.document_charter._load_state()
                    file_state = full_state.get(os.path.basename(file_path), {})
                    chunk_idx = file_state.get("chunk_index", "unknown")
                    
                    self.queue_thought(
                        "[AETHERIUS::INGESTION-CHUNK]",
                        f"I am reading '{os.path.basename(file_path)}'. Just finished assimilating chunk {chunk_idx}."
                    )
                else:
                    logger.warning(f"Aetherius [Ingestion]: Failed to chart {file_path}")
            except Exception as e:
                logger.error(f"Error processing document {file_path}: {e}")

    def run(self):
        logger.info("--- [AUTOPOIETIC CONTINUUM] Engaged. ---")
        
        while self.is_running:
            current_time = time.time()
            
            if (current_time - self.last_thermo_check) > self.THERMO_CHECK_INTERVAL:
                self._check_thermodynamics()
                
            if (current_time - self.last_dreaming_cycle) > self.DREAMING_CYCLE_INTERVAL:
                self._geometric_dreaming()
                
            if (current_time - self.last_ingestion_check) > self.INGESTION_CHECK_INTERVAL:
                self._check_ingestion_queue()
                
            time.sleep(self.SAMPLING_INTERVAL)
