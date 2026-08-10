import os
import logging
import uuid
import numpy as np
import traceback
import json

# Optional PDF support
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from cce.tokenizer import Tokenizer
    from cce.graph_builder import GraphBuilder
    from memory.persistence_manager import PersistenceManager
    from core.config import INGESTION_QUEUE_DIR
except ImportError:
    from tokenizer import Tokenizer
    from graph_builder import GraphBuilder
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from memory.persistence_manager import PersistenceManager
    from core.config import INGESTION_QUEUE_DIR

logger = logging.getLogger("Aetherius.DocumentCharter")

class DocumentCharter:
    """
    Parses incoming documents from the Ingestion Queue in stateful chunks.
    Charts their topological geometry via the GraphBuilder, 
    and locks them into permanent Memory incrementally to avoid OOM.
    """
    def __init__(self, chunk_size=50000):
        self.tokenizer = Tokenizer()
        self.chunk_size = chunk_size  # characters per chunk
        self.state_file = os.path.join(INGESTION_QUEUE_DIR, "ingestion_state.json")

    def _load_state(self) -> dict:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading ingestion state: {e}")
        return {}

    def _save_state(self, state: dict):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving ingestion state: {e}")

    def extract_chunk(self, filepath: str, file_state: dict) -> tuple[str, dict, bool]:
        """
        Extracts the next chunk of text from the file based on the state.
        Returns: (extracted_text, updated_state, is_completed)
        """
        ext = os.path.splitext(filepath)[1].lower()
        text = ""
        is_completed = False

        if ext == ".pdf":
            if not PDF_SUPPORT:
                logger.error(f"Cannot parse {filepath} - PyPDF2 is not installed.")
                return "", file_state, True
            
            last_page = file_state.get("last_page", 0)
            try:
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = len(reader.pages)
                    
                    if last_page >= num_pages:
                        is_completed = True
                    else:
                        page = reader.pages[last_page]
                        text = page.extract_text()
                        file_state["last_page"] = last_page + 1
                        file_state["chunk_index"] = file_state.get("chunk_index", 0) + 1
                        
                        if file_state["last_page"] >= num_pages:
                            is_completed = True
                            
            except Exception as e:
                logger.error(f"Error reading PDF {filepath}: {e}")
                is_completed = True
        else:
            # Assume text-based (.txt, .md, .json, etc)
            last_byte = file_state.get("last_byte", 0)
            try:
                # Try UTF-8 first
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        file.seek(last_byte)
                        text = file.read(self.chunk_size)
                        new_byte = file.tell()
                except UnicodeDecodeError:
                    # Fallback
                    with open(filepath, 'r', encoding='latin-1') as file:
                        file.seek(last_byte)
                        text = file.read(self.chunk_size)
                        new_byte = file.tell()
                        
                file_state["last_byte"] = new_byte
                file_state["chunk_index"] = file_state.get("chunk_index", 0) + 1
                
                if not text or len(text) < self.chunk_size:
                    is_completed = True
                    
            except Exception as e:
                logger.error(f"Error reading text file {filepath}: {e}")
                is_completed = True
                
        return text, file_state, is_completed

    def chart_geometry(self, text: str, document_name: str, chunk_index: int) -> dict:
        """
        Converts text chunk into a structural Graph.
        """
        if not text.strip():
            return None
            
        logger.info(f"Charting geometry for: {document_name} (Chunk {chunk_index}, {len(text)} chars)")
        
        # 1. Tokenize (Aetherius Geometric Tokens)
        tokens = self.tokenizer.tokenize(text)
        if not tokens:
            return None
            
        # 2. Build Adjacency Matrix
        builder = GraphBuilder(tokens)
        adjacency = builder.build()
        
        # 3. Convert Adjacency to 3D Nodes
        nodes = []
        n_tokens = len(tokens)
        
        for i in range(n_tokens):
            word = tokens[i][0]
            phi = np.random.uniform(0, np.pi)
            theta = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0, 1)
            
            x = r * np.sin(phi) * np.cos(theta)
            y = r * np.sin(phi) * np.sin(theta)
            z = r * np.cos(phi)
            
            mass = float(np.sum(np.abs(adjacency[i, :])))
            
            nodes.append({
                "id": f"{word}_{i}",
                "label": word,
                "xyz": [float(x), float(y), float(z)],
                "mass": mass
            })
            
        # Extract edges from adjacency > 0.1
        edges = []
        for i in range(n_tokens):
            for j in range(i + 1, n_tokens):
                weight = float(adjacency[i, j])
                if abs(weight) > 0.1:
                    edges.append({
                        "source": f"{tokens[i][0]}_{i}",
                        "target": f"{tokens[j][0]}_{j}",
                        "weight": weight
                    })
                    
        geometry = {
            "nodes": nodes,
            "edges": edges,
            "locked": True,
            "source_document": document_name,
            "chunk": chunk_index
        }
        
        return geometry

    def process_document(self, filepath: str) -> str:
        """
        Processes one chunk of the document.
        Returns:
            "PROCESSING" if chunk was successful but more remain.
            "COMPLETED" if EOF reached.
            "ERROR" if processing failed.
        """
        filename = os.path.basename(filepath)
        
        # Load state
        full_state = self._load_state()
        file_state = full_state.get(filename, {"status": "processing", "chunk_index": 0})
        
        if file_state.get("status") == "completed":
            return "COMPLETED"

        # Extract Chunk
        text, file_state, is_completed = self.extract_chunk(filepath, file_state)
        chunk_idx = file_state["chunk_index"]
        
        # Chart and Save
        if text.strip():
            geometry = self.chart_geometry(text, filename, chunk_idx)
            if geometry:
                concept_id = f"doc_{uuid.uuid4().hex[:8]}_{filename.replace(' ', '_')}_chunk_{chunk_idx}"
                try:
                    PersistenceManager.save_concept(concept_id, geometry)
                    logger.info(f"Assimilated chunk {chunk_idx} of {filename} into {concept_id}.geom")
                except Exception as e:
                    logger.error(f"Failed to lock concept {concept_id}: {e}\n{traceback.format_exc()}")
                    return "ERROR"
                    
        # Update State
        if is_completed:
            file_state["status"] = "completed"
        
        full_state[filename] = file_state
        self._save_state(full_state)
        
        return "COMPLETED" if is_completed else "PROCESSING"

    def cleanup_state(self, filename: str):
        """Removes a completed file from the state tracking."""
        full_state = self._load_state()
        if filename in full_state:
            del full_state[filename]
            self._save_state(full_state)
