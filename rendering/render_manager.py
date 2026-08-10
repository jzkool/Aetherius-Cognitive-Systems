import logging
import os

try:
    from core.config import RENDER_CACHE_DIR
except ImportError:
    from config import RENDER_CACHE_DIR

from rendering.xla_renderer import XLARenderer
from memory.persistence_manager import PersistenceManager

logger = logging.getLogger("Aetherius.RenderManager")

class RenderManager:
    """
    Manages the active rendering engine and bridges the gap between 
    the persistent coordinate-locked memory and visual output.
    """
    
    def __init__(self, default_engine="xla"):
        self.active_engine = None
        self.engines = {
            "xla": XLARenderer()
        }
        self.set_engine(default_engine)

    def set_engine(self, engine_key: str):
        if engine_key in self.engines:
            self.active_engine = self.engines[engine_key]
            self.active_engine.initialize()
            logger.info(f"RenderManager switched to engine: {self.active_engine.engine_name}")
        else:
            logger.error(f"Render engine '{engine_key}' not found. Defaulting to XLA.")
            self.active_engine = self.engines["xla"]
            self.active_engine.initialize()

    def render_concept(self, concept_id: str):
        logger.info(f"Attempting to render concept: {concept_id}")
        
        concept_data = PersistenceManager.load_concept(concept_id)
        if not concept_data:
            logger.warning(f"Concept '{concept_id}' has no locked geometry. Rendering aborted.")
            return None

        output_path = os.path.join(RENDER_CACHE_DIR, f"{concept_id}_render.json")

        result = self.active_engine.render(
            geometry=concept_data["geometry"],
            thermodynamics=concept_data["thermodynamics"],
            output_path=output_path
        )
        
        return result
