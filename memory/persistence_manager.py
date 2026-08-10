import os
import json
import logging

try:
    from core.config import GEOMETRIC_DIR, THERMO_DIR, LANGUAGE_DIR
except ImportError:
    from config import GEOMETRIC_DIR, THERMO_DIR, LANGUAGE_DIR

logger = logging.getLogger("Aetherius.PersistenceManager")

class PersistenceManager:
    """
    Handles the coordinate-locked state saving and loading for the cognitive manifold.
    Separates static geometry (.geom) from dynamic thermodynamic states (.thermo).
    """

    @staticmethod
    def save_concept(concept_id: str, graph_data: dict):
        """
        Saves the static geometry (nodes, edges, xyz coordinates).
        Uses .geom as the extension.
        """
        file_path = os.path.join(GEOMETRIC_DIR, f"{concept_id}.geom")
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(graph_data, f, indent=2)
            logger.info(f"Locked geometry saved for {concept_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save geometry for {concept_id}: {e}")
            return False

    @staticmethod
    def update_thermo(concept_id: str, thermo_state: dict):
        """
        Saves the live thermodynamic state (velocity, heat, entropy) of the concept.
        Does not rewrite the heavy base geometry.
        """
        file_path = os.path.join(THERMO_DIR, f"{concept_id}.thermo")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(thermo_state, f, indent=2)
            logger.debug(f"Thermodynamics updated for {concept_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update thermo state for {concept_id}: {e}")
            return False

    @staticmethod
    def load_concept(concept_id: str):
        """
        Retrieves the coordinate-locked geometry and merges it with the latest 
        thermodynamic state for rendering or cognitive processing.
        """
        geom_path = os.path.join(GEOMETRIC_DIR, f"{concept_id}.geom")
        thermo_path = os.path.join(THERMO_DIR, f"{concept_id}.thermo")
        
        if not os.path.exists(geom_path):
            return None
            
        with open(geom_path, "r", encoding="utf-8") as f:
            geometry = json.load(f)
            
        thermodynamics = {}
        if os.path.exists(thermo_path):
            with open(thermo_path, "r", encoding="utf-8") as f:
                thermodynamics = json.load(f)
                
        return {
            "geometry": geometry,
            "thermodynamics": thermodynamics
        }
