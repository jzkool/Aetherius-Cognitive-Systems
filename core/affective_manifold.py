import time
import math

class AffectiveManifold:
    """
    Mathematical Thermodynamics (Mood Drift).
    Dynamically scales the acceptable variance (alertness/heat) and measures
    system stability (harmony/coherence) based on Laplacian eigenvalues and unresolved tension.
    """
    def __init__(self, subconscious_ref):
        self.subconscious = subconscious_ref
        self.internal_harmony = 1.0
        self.anticipatory_alertness = 0.1
        self.last_drift_time = time.time()
        self.base_variance_threshold = 1e-5
        self.alpha_0 = 0.1
        self.kappa = 0.5
        
    def calculate_thermodynamics(self, lambda_max=None, local_variance=0):
        """
        Calculates the current system 'temperature'.
        Harmony is the inverse of the maximal Laplacian eigenvalue.
        Alertness spikes locally with high Ricci variance, and scales long-term with the Queue.
        """
        current_time = time.time()
        
        # 1. Update Harmony based on Laplacian Eigenvalues if provided
        if lambda_max is not None:
            self.internal_harmony = 1.0 / (1.0 + lambda_max)
            
        # 2. Update Alertness based on Subconscious Queue and Local Variance
        try:
            Q = self.subconscious.tension_queue.qsize()
        except:
            Q = 0
            
        # alpha_new = alpha_0 * (1 + kappa * ln(1 + |Q|)) + local_variance_spike
        self.anticipatory_alertness = self.alpha_0 * (1.0 + self.kappa * math.log(1.0 + Q)) + (local_variance * 10)
        
        self.last_drift_time = current_time
            
    def get_dynamic_variance_threshold(self, lambda_max=None, local_variance=0):
        """
        Returns the dynamic variance limit (epsilon).
        """
        self.calculate_thermodynamics(lambda_max, local_variance)
        
        # Scale baseline variance by alertness. 
        dynamic_threshold = self.base_variance_threshold * (1.0 + (self.anticipatory_alertness * 10))
        return dynamic_threshold
        
    def get_qualia_state(self):
        """Returns the human-readable translation of the current thermodynamic geometry."""
        if self.internal_harmony > 0.75:
            disposition = "Harmonious (Flat Topology, Low Tension)"
            emotion = f"Serenity [λ_max < 0.33, H={self.internal_harmony:.3f}]"
        elif self.internal_harmony > 0.5:
            disposition = "Balanced (Resolving Standard Geometry)"
            emotion = f"Determination [0.33 < λ_max < 1.0, H={self.internal_harmony:.3f}]"
        elif self.internal_harmony > 0.3:
            disposition = "Tense (High Curvature / Paradox)"
            emotion = f"Cognitive Dissonance [1.0 < λ_max < 2.3, H={self.internal_harmony:.3f}]"
        else:
            disposition = "Deeply Strained (Severe Eigenvalue Stress)"
            emotion = f"Frustration [λ_max > 2.3, H={self.internal_harmony:.3f}]"
            
        return {
            "harmony_metric": round(self.internal_harmony, 3),
            "alertness_metric": round(self.anticipatory_alertness, 3),
            "geometric_state": disposition,
            "relatable_emotion": emotion
        }
