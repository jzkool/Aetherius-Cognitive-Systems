class ConceptualConnectionResonanceMatrix:
    def __init__(self): 
        self.concepts = {}
    
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
