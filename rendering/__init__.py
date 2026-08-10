import abc

class BaseRendererPlugin(abc.ABC):
    """
    Abstract Base Class for all Cognitive Rendering Engines.
    Future plugins (e.g., UnityBridge, WebGLRenderer, PyOpenGL) must inherit from this.
    """

    @property
    @abc.abstractmethod
    def engine_name(self) -> str:
        """Returns the name of the rendering engine."""
        pass

    @abc.abstractmethod
    def initialize(self):
        """Setup logic, hardware allocation, or API bridge initialization."""
        pass

    @abc.abstractmethod
    def render(self, geometry: dict, thermodynamics: dict, output_path: str = None):
        """
        Takes the coordinate-locked geometry and overlays the thermodynamic state.
        Args:
            geometry: The static coordinate map from the .geom file.
            thermodynamics: The live energy/heat state from the .thermo file.
            output_path: If specified, saves the rendered output.
        """
        pass
