import uuid
import datetime
from memory.ccrm import ConceptualConnectionResonanceMatrix

class PatternInterpretationTokenisationStorage:
    def __init__(self, ccrm_instance: ConceptualConnectionResonanceMatrix): 
        self.ccrm = ccrm_instance
        
    def process_and_store_item(self, raw_input: any, input_type: str, tags: list = [], gmstring=None, betti=None):
        ccrm_id = f"item_{uuid.uuid4().hex}"
        
        # Dual-Language Representation: Human semantic text + System geometric state
        data_to_store = {
            "raw_preview": str(raw_input)[:150], 
            "timestamp": datetime.datetime.now().isoformat(),
            "gmstring": gmstring,
            "topological_signature": betti
        }
        
        all_tags = [tag.lower() for tag in ([input_type] + tags)]
        self.ccrm.add_concept(concept_id=ccrm_id, data=data_to_store, tags=all_tags)
        
        print(f"[PiTS] Logged memory to CCRM Identity Vector | ID: {ccrm_id[:13]}...", flush=True)
        return ccrm_id
