import json
import os

class ConceptualConnectionResonanceMatrix:
    def __init__(self): 
        self.concepts = {}
        # Try Hugging Face persistent volume first, otherwise local
        self.storage_path = "./data/ccrm_graph.json" if os.path.exists("./data") else "ccrm_graph.json"
        self.load_graph()
        
    def save_graph(self):
        try:
            # Convert sets to lists for JSON serialization
            serializable = {}
            for k, v in self.concepts.items():
                serializable[k] = {"data": v["data"], "tags": list(v["tags"])}
            with open(self.storage_path, "w") as f:
                json.dump(serializable, f)
        except Exception as e:
            print(f"[CCRM] Failed to save graph to {self.storage_path}: {e}")
            
    def load_graph(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    loaded = json.load(f)
                for k, v in loaded.items():
                    self.concepts[k] = {"data": v["data"], "tags": set(v["tags"])}
                print(f"[CCRM] Restored {len(self.concepts)} persistent memories from {self.storage_path}")
            except Exception as e:
                print(f"[CCRM] Failed to load graph from {self.storage_path}: {e}")
    
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
