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
    def __init__(self, chunk_size=5000, lines_chunk=50, engine=None):
        self.engine = engine
        self.tokenizer = Tokenizer()
        self.chunk_size = chunk_size  # characters per chunk for text
        self.lines_chunk = lines_chunk # lines per chunk for jsonl
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
                        extracted = page.extract_text()
                        if extracted:
                            text = extracted
                        else:
                            text = ""
                            logger.warning(f"PDF page {last_page} in {filepath} yielded no text (possible image scan).")
                            
                        file_state["last_page"] = last_page + 1
                        file_state["chunk_index"] = file_state.get("chunk_index", 0) + 1
                        
                        if file_state["last_page"] >= num_pages:
                            is_completed = True
                            
            except Exception as e:
                logger.error(f"Error reading PDF {filepath}: {e}")
                is_completed = True
        elif ext == ".jsonl":
            # JSONL: read by precise lines to avoid fracturing objects
            last_line = file_state.get("last_line", 0)
            lines_read = 0
            text_lines = []
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    # Skip to the last read line
                    for _ in range(last_line):
                        next(file, None)
                    
                    # Read the next chunk of lines
                    for _ in range(self.lines_chunk):
                        line = next(file, None)
                        if line is None:
                            is_completed = True
                            break
                        if line.strip():
                            text_lines.append(line.strip())
                            lines_read += 1
                            
                text = " ".join(text_lines)
                file_state["last_line"] = last_line + lines_read
                file_state["chunk_index"] = file_state.get("chunk_index", 0) + 1
                
                if not text:
                    is_completed = True
            except Exception as e:
                logger.error(f"Error reading JSONL file {filepath}: {e}")
                is_completed = True
        else:
            # Assume text-based (.txt, .md, etc) - read by exact byte offset
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

    def chart_geometry(self, text: str, document_name: str, chunk_index: int) -> bool:
        """
        Routes the text into the primary AetheriusEngine for true geometric rendering.
        This forces the system to actually learn from the document and update its topological grammar.
        """
        if not text.strip() or self.engine is None:
            return False
            
        import re
        logger.info(f"Charting geometry for: {document_name} (Chunk {chunk_index}, {len(text)} chars)")
        
        # Split chunk into sentences to avoid OOM on O(N^3) Ricci-Flow
        # JSONL parsing may have preserved json formatting, so we strip out common symbols during the parse
        sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
        
        for sentence in sentences:
            s = sentence.strip()
            # Skip noise (brackets from json, super short stubs)
            if len(s) > 10 and '{' not in s and '}' not in s:
                try:
                    # Physically integrate the sentence into the PMCA engine!
                    self.engine.process(s)
                except Exception as e:
                    logger.error(f"Engine failed to resolve sentence '{s[:30]}...': {e}")
                    
        return True

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
        
        # Chart and Save through Engine
        if text.strip():
            success = self.chart_geometry(text, filename, chunk_idx)
            if success:
                logger.info(f"Assimilated chunk {chunk_idx} of {filename} through Aetherius Engine.")
            else:
                logger.warning(f"Engine was not available or text was blank for chunk {chunk_idx}.")
                    
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
