import json
import os
from core.config import DATA_DIR
from core.json_encoder import safe_json_dump

class ConceptualConnectionResonanceMatrix:
    def __init__(self): 
        self.concepts = {}
        self.storage_path = os.path.join(DATA_DIR, "ccrm_graph.json")
        self.load_graph()
        
    def save_graph(self):
        # Convert sets to lists for JSON serialization
        serializable = {}
        for k, v in self.concepts.items():
            serializable[k] = {"data": v["data"], "tags": list(v["tags"])}
            
        try:
            with open(self.storage_path, "w") as f:
                safe_json_dump(serializable, f)
            print(f"[CCRM] Successfully saved memory to persistent bucket: {self.storage_path}")
        except Exception as e:
            print(f"[CCRM] CRITICAL FAILURE: Cannot write to persistent bucket. Error: {e}")

    def load_graph(self):
        loaded = None
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    loaded = json.load(f)
                print(f"[CCRM] Successfully loaded persistent memory from bucket.")
            except Exception as e:
                print(f"[CCRM] Failed to load from persistent bucket: {e}")
                
        if loaded:
            for k, v in loaded.items():
                self.concepts[k] = {"data": v["data"], "tags": set(v["tags"])}
            print(f"[CCRM] Restored {len(self.concepts)} persistent concepts.")
    
    def add_concept(self, concept_id: str, data: dict, tags: list = None):
        if concept_id not in self.concepts: 
            self.concepts[concept_id] = {"data": data, "tags": set(tags or [])}
            return self.concepts[concept_id]
        return None
        
    def get_concept(self, concept_id: str): 
        return self.concepts.get(concept_id)
        
    def search_by_tags(self, query_keywords: list, specific_tag: str = None) -> list:
        found = []
        for i, d in self.concepts.items():
            if specific_tag and specific_tag.lower() not in d.get("tags", set()): 
                continue
            if query_keywords and not any(k.lower() in d.get("tags", set()) for k in query_keywords): 
                continue
            found.append(d)
        return found
        
    def find_analogy(self, current_betti: dict, exclude_raw: str = None) -> str:
        """
        Operator 12: Geometric Generalization
        Searches the persistent manifold for a past memory with the exact same topological signature.
        """
        if not current_betti:
            return None
            
        for concept_id, concept_data in self.concepts.items():
            data = concept_data.get("data", {})
            stored_betti = data.get("topological_signature")
            
            # Prevent self-matching
            if exclude_raw and data.get("raw_preview") == str(exclude_raw)[:150]:
                continue
                
            if stored_betti and stored_betti == current_betti:
                return data.get("raw_preview")
                
        return None
