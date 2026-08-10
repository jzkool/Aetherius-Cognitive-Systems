import threading
import logging
from typing import List, Dict

try:
    from continuum.autopoietic_loop import AutopoieticLoop
except ImportError:
    # Fallback if imported from outside continuum
    from autopoietic_loop import AutopoieticLoop

# Try to import IPython display for rich notebook output
try:
    from IPython.display import display, HTML
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False

logger = logging.getLogger("Aetherius.TPUNotebookController")

class TPUNotebookController:
    """
    Acts as the bridge between a Jupyter Notebook running on a TPU (e.g., Google Colab)
    and the Autopoietic Continuum Loop running in the background.
    """
    
    _instance = None

    def __init__(self):
        if TPUNotebookController._instance is not None:
            raise Exception("TPUNotebookController is a singleton. Use get_instance().")
            
        self.loop_thread = None
        
        # Check XLA/TPU status immediately
        self._check_tpu_status()
        
        TPUNotebookController._instance = self
        logger.info("TPUNotebookController initialized.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    def _check_tpu_status(self):
        """Verifies if XLA is bound to a TPU backend."""
        try:
            import jax
            backend = jax.default_backend()
            logger.info(f"JAX Default Backend detected: {backend.upper()}")
            if backend != 'tpu':
                logger.warning("TPU not detected by JAX. Render operations will fall back to CPU/GPU.")
        except ImportError:
            logger.warning("JAX not installed. Notebook will run without XLA hardware acceleration.")

    def start_continuum(self):
        """
        Safely spins up the AutopoieticLoop daemon thread.
        This allows the notebook cell to finish execution while the loop runs in the background.
        """
        if self.loop_thread and self.loop_thread.is_alive():
            logger.info("Continuum loop is already running.")
            return

        self.loop_thread = AutopoieticLoop()
        self.loop_thread.start()
        logger.info("Autopoietic Continuum Loop has been started in the background.")

    def stop_continuum(self):
        """Signals the background loop to stop gracefully."""
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.stop()
            self.loop_thread.join(timeout=2.0)
            logger.info("Autopoietic Continuum Loop has been stopped.")
        else:
            logger.info("No active continuum loop to stop.")

    def poll_thoughts(self) -> List[Dict]:
        """
        Pops all accumulated spontaneous thoughts from the queue and returns them.
        If IPython is available, it pretty-prints them in the notebook output cell.
        """
        if not self.loop_thread:
            logger.warning("Continuum loop is not running.")
            return []

        thoughts = []
        queue = self.loop_thread.spontaneous_thought_queue
        
        while queue:
            try:
                thoughts.append(queue.popleft())
            except IndexError:
                break
                
        if not thoughts:
            print("No new spontaneous thoughts at this time.")
            return []

        # Beautiful Output for Notebooks
        if IPYTHON_AVAILABLE:
            html_out = "<div style='font-family: monospace; padding: 10px; background: #1e1e1e; color: #d4d4d4; border-radius: 5px;'>"
            for t in thoughts:
                html_out += f"<p><span style='color: #569cd6;'>{t['signature']}</span>: {t['thought']}</p>"
            html_out += "</div>"
            display(HTML(html_out))
        else:
            # Fallback for standard terminals
            for t in thoughts:
                print(f"{t['signature']}: {t['thought']}")
                
        return thoughts
