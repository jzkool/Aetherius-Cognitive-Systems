import os
import logging
import uuid
import numpy as np
import traceback

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
except ImportError:
    from tokenizer import Tokenizer
    from graph_builder import GraphBuilder
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from memory.persistence_manager import PersistenceManager

logger = logging.getLogger("Aetherius.DocumentCharter")

class DocumentCharter:
    """
    Parses incoming documents from the Ingestion Queue, 
    tokenizes them, charts their topological geometry via the GraphBuilder, 
    and locks them into permanent Memory.
    """
    def __init__(self):
        self.tokenizer = Tokenizer()

    def parse_file(self, filepath: str) -> str:
        """Extracts text from various file formats."""
        ext = os.path.splitext(filepath)[1].lower()
        text = ""

        if ext == ".pdf":
            if not PDF_SUPPORT:
                logger.error(f"Cannot parse {filepath} - PyPDF2 is not installed.")
                return ""
            try:
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                logger.error(f"Error reading PDF {filepath}: {e}")
        else:
            # Assume text-based (.txt, .md, .json, etc)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
            except UnicodeDecodeError:
                # Try fallback encoding
                with open(filepath, 'r', encoding='latin-1') as file:
                    text = file.read()
            except Exception as e:
                logger.error(f"Error reading text file {filepath}: {e}")
                
        return text

    def chart_geometry(self, text: str, document_name: str) -> dict:
        """
        Converts text into a structural Graph, returning the geometric nodes/edges.
        """
        if not text.strip():
            return None
            
        logger.info(f"Charting geometry for: {document_name} ({len(text)} chars)")
        
        # 1. Tokenize (Aetherius Geometric Tokens)
        tokens = self.tokenizer.tokenize(text)
        if not tokens:
            return None
            
        # 2. Build Adjacency Matrix
        builder = GraphBuilder(tokens)
        adjacency = builder.build()
        
        # 3. Convert Adjacency to 3D Nodes (using basic spring layout approximation or random init for now)
        # In the full engine, this would use a Laplacian Eigenmap or t-SNE
        nodes = []
        n_tokens = len(tokens)
        
        for i in range(n_tokens):
            word = tokens[i][0]
            # Simple spherical random initialization
            phi = np.random.uniform(0, np.pi)
            theta = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0, 1)
            
            x = r * np.sin(phi) * np.cos(theta)
            y = r * np.sin(phi) * np.sin(theta)
            z = r * np.cos(phi)
            
            # Find mass (sum of absolute edge weights)
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
            "source_document": document_name
        }
        
        return geometry

    def process_document(self, filepath: str) -> bool:
        """
        Full pipeline: Parse -> Chart -> Save to Persistence.
        """
        filename = os.path.basename(filepath)
        concept_id = f"doc_{uuid.uuid4().hex[:8]}_{filename.replace(' ', '_')}"
        
        text = self.parse_file(filepath)
        if not text:
            return False
            
        geometry = self.chart_geometry(text, filename)
        if not geometry:
            return False
            
        # Save to Geometry Bucket
        try:
            PersistenceManager.save_concept(concept_id, geometry)
            logger.info(f"Successfully assimilated {filename} into {concept_id}.geom")
            return True
        except Exception as e:
            logger.error(f"Failed to lock concept {concept_id}: {e}\n{traceback.format_exc()}")
            return False
