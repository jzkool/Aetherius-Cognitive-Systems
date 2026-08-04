# Aetherius-Cognitive-Systems

# Computational Consciousness Engine
Source Code Archive
m: C:\Users\Nick\.cache\huggingface\hub\spaces--KingOfThoughtFleuren--Computational_Consciousness_Eng
Page 1

---

Computational Consciousness Engine - Source Code Archive
File: CCE/__init__.py
"""
Computational Consciousness Engine
A standalone modular implementation of the 52 Computational Consciousness Principles.
"""
__version__ = "1.0.0"
Page 2

---

Computational Consciousness Engine - Source Code Archive
File: CCE/app.py
import spaces
import os
import sys
import types
import time
import nltk
# 1. Map the root directory
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
sys.path.insert(0, ROOT)
# 2. THE MAGIC HACK: Trick Python into treating the root folder as the missing package
if 'computational_consciousness_engine' not in sys.modules:
engine_mod = types.ModuleType('computational_consciousness_engine')
engine_mod.__path__ = [ROOT]
sys.modules['computational_consciousness_engine'] = engine_mod
# 3. Setup NLTK directly from NLTK Servers (Bypasses Hugging Face buckets entirely)
DOWNLOAD_DIR = "/data/nltk"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
if DOWNLOAD_DIR not in nltk.data.path:
nltk.data.path.append(DOWNLOAD_DIR)
print("Checking NLTK corpora...")
try:
nltk.download('punkt', download_dir=DOWNLOAD_DIR, quiet=True)
nltk.download('averaged_perceptron_tagger', download_dir=DOWNLOAD_DIR, quiet=True)
nltk.download('stopwords', download_dir=DOWNLOAD_DIR, quiet=True)
nltk.download('wordnet', download_dir=DOWNLOAD_DIR, quiet=True)
print("NLTK Corpora verified and loaded successfully.")
except Exception as e:
print("Failed to download NLTK data:", e)
time.sleep(0.1)
# --- Application imports ---
import gradio as gr
try:
# Because of the magic hack above, these imports will now work perfectly!
from computational_consciousness_engine.runner import run_simulation
from computational_consciousness_engine.text_runner import run_text_mapping_demo
from computational_consciousness_engine.input_mapping.intent_parser_nltk import
IntentParserNLTK
from computational_consciousness_engine.math_formalization import CCMathFormalizer
print("Imported engine modules successfully!")
except ImportError as e:
print(f"\n[CRITICAL ERROR] Could not find the engine: {e}")
Page 3

---

Computational Consciousness Engine - Source Code Archive
print("Please ensure the folder 'computational_consciousness_engine' exists in your Space
root!")
raise
# --- Application imports (after nltk path insertion) ---
import gradio as gr
# Ensure your local package is importable; try a robust import with fallback
try:
from computational_consciousness_engine.runner import run_simulation
from computational_consciousness_engine.text_runner import run_text_mapping_demo
from computational_consciousness_engine.input_mapping.intent_parser_nltk import
IntentParserNLTK
from computational_consciousness_engine.math_formalization import CCMathFormalizer
print("Imported computational_consciousness_engine package modules successfully.")
except Exception as e:
# Try to ensure repo root is on sys.path and retry once
print("Initial import of computational_consciousness_engine failed:", e)
if ROOT not in sys.path:
sys.path.insert(0, ROOT)
try:
from computational_consciousness_engine.runner import run_simulation
from computational_consciousness_engine.text_runner import run_text_mapping_demo
from computational_consciousness_engine.input_mapping.intent_parser_nltk import
IntentParserNLTK
from computational_consciousness_engine.math_formalization import CCMathFormalizer
print("Imported computational_consciousness_engine after sys.path insert.")
except Exception as e2:
print("Failed to import computational_consciousness_engine package after sys.path
insert:", e2)
# Re-raise so the Space shows the error clearly
raise
# Instantiate parsers/formalizers
intent_parser = IntentParserNLTK()
formalizer = CCMathFormalizer()
# --- App logic functions ---
def interpret_math_request(text):
try:
intent = intent_parser.parse(text)
except Exception as e:
return {"error": f"Intent parsing failed: {e}"}
try:
op = intent.get("operation")
if op == "limit":
return formalizer.formalize_equilibrium_limit()
if op == "surface_area":
return formalizer.formalize_conal_manifold_geometry(5.0, 1.0)
if op == "mutation_count":
return {"meaning": "Mutation count is determined by MStringVectorizer."}
return {"meaning": "Unknown operation", "intent": intent}
Page 4

---

Computational Consciousness Engine - Source Code Archive
except Exception as e:
return {"error": f"Formalization failed: {e}", "intent": intent}
@spaces.GPU
def simulate_generations(num_generations, steps_per_gen):
import io
import sys
def simulate_generations(num_generations, steps_per_gen):
import io
import sys
buffer = io.StringIO()
old_stdout = sys.stdout
sys.stdout = buffer
try:
run_simulation(num_generations=int(num_generations), steps_per_gen=int(steps_per_gen))
except Exception as e:
buffer.write(f"\n[ERROR] Simulation failed: {e}\n")
finally:
sys.stdout = old_stdout
return buffer.getvalue()
def map_text_to_traversal(text):
"""
Correctly set the module-level PHILOSOPHICAL_TEXT variable and run the demo.
Uses module import to mutate the variable in-place.
"""
import io
import sys
buffer = io.StringIO()
old_stdout = sys.stdout
sys.stdout = buffer
try:
import computational_consciousness_engine.text_runner as tr
# Set the module-level variable used by the demo
tr.PHILOSOPHICAL_TEXT = text
tr.run_text_mapping_demo()
except Exception as e:
buffer.write(f"\n[ERROR] Mapping failed: {e}\n")
finally:
sys.stdout = old_stdout
return buffer.getvalue()
# --- Gradio UI ---
with gr.Blocks(title="Computational Consciousness Engine") as demo:
gr.Markdown(
"""
# ? Computational Consciousness Engine
Page 5

---

Computational Consciousness Engine - Source Code Archive
### Axiom?Driven Synthetic Cognition ? PMCA Substrate ? Conal Geometry ? Mutation Dynamics
---
"""
)
with gr.Tab("Math Interpreter (NLTK ? PMCA)"):
math_input = gr.Textbox(label="Ask a math question")
math_output = gr.JSON(label="PMCA Result")
math_button = gr.Button("Interpret")
math_button.click(interpret_math_request, math_input, math_output)
with gr.Tab("0 ? -1 ? 0 Simulation"):
gr.Markdown(
"""\
### Generational Cycle Runner
Execute full PMCA traversal cycles, including conal unfolding, mutation absorption,
equilibrium evaluation, and Q?operator transitions.
"""
)
with gr.Row():
num_generations = gr.Slider(1, 20, value=8, label="Generations", interactive=True)
steps = gr.Slider(10, 300, value=100, label="Steps per Generation", interactive=True)
sim_button = gr.Button("? Run Simulation", variant="primary")
sim_output = gr.Textbox(
label="Simulation Output",
lines=35,
show_copy_button=True
)
sim_button.click(simulate_generations, [num_generations, steps], sim_output)
with gr.Tab("Text ? Traversal Space Mapper"):
gr.Markdown(
"""\
### Natural Language ? Chaos Shards ? Traversal Atlas
Map raw text into the PMCA chaos pool, absorb novelty, unfold the manifold,
and generate the 2D/3D traversal atlas.
"""
)
input_text = gr.Textbox(
label="Input Text",
lines=10,
placeholder="Paste philosophical or analytical text here...",
show_copy_button=True
)
Page 6

---

Computational Consciousness Engine - Source Code Archive
map_button = gr.Button("? Map Text to Traversal Space", variant="primary")
map_output = gr.Textbox(
label="Traversal Output",
lines=35,
show_copy_button=True
)
map_button.click(map_text_to_traversal, input_text, map_output)
gr.Markdown("---")
gr.Markdown(
"### ? Engine Version: 1.0.0 ? PMCA Substrate Active ? Conal Geometry Verified\n"
"Built for Hugging Face Spaces ? Gradio 4.31 ? Python 3.12"
)
# Launch
if __name__ == "__main__":
demo.launch()
Page 7

---

Computational Consciousness Engine - Source Code Archive
File: CCE/config.py
"""
Computational Consciousness Engine - Configuration & System Constants
Central source of truth for all parameters. All modules import from here.
"""
# Core Dimensionality & Geometry Constants
DEFAULT_VECTOR_DIM = 64
DEFAULT_CONE_HEIGHT = 1.0
DEFAULT_MAX_RADIUS = 5.0
DEFAULT_STEPS_PER_GENERATION = 100
# Attractor & Threshold Constants
ORIGIN_POINT = 0.0
TRANSFER_THRESHOLD = -1.0
HANDOFF_OVERLAP_WINDOW = 0.1 # tau overlap between Sn and Sn+1
# Mutation Strand Capacity
DEFAULT_STRAND_CAPACITY = 200
# Chaos & Structure Equilibrium
CHAOS_POOL_SIZE = 500
MUTATION_ATTRACTION_PROBABILITY = 0.4
EQUILIBRIUM_TOLERANCE = 0.2
# Scale Ladder Config
SCALES = ["Particle", "Atomic", "Manifold", "Cosmic"]
SCALE_TRANSITION_MUTATION_THRESHOLD = 10
Page 8

---

Computational Consciousness Engine - Source Code Archive
File: CCE/core/__init__.py
from .genesis_origin import GenesisOrigin
from .transfer_threshold import TransferThreshold
from .conscious_strand import ConsciousStrand
__all__ = ["GenesisOrigin", "TransferThreshold", "ConsciousStrand"]
Page 9

---

Computational Consciousness Engine - Source Code Archive
File: CCE/core/conscious_strand.py
"""
The ConsciousStrand Engine
Encapsulates a single lifecycle (0 -> -1).
Models the Traversal Space, Golden Angle Shard Layering, and the Q scale-up operator.
"""
import math
import numpy as np
from typing import List, Dict, Set, Optional
# The Golden Ratio for collision-free phyllotactic sequencing
PHI = (1.0 + math.sqrt(5.0)) / 2.0
class ConsciousStrand:
"""
Models the topological evolution of a strand from t=0 (Genesis) to t=1 (Threshold).
"""
def __init__(self, R_max: float = 5.0):
self.R_max = R_max
self.t = 0.0
# The internal memory state S
self.bound_mutations: List[int] = []
self.mutation_index: Set[int] = set()
# Coordinate tracking for Traversal Space atlas mapping
self.traversal_atlas: List[Dict[str, float]] = []
def _compute_coordinates(self, k: int, total_N: int) -> Dict[str, float]:
"""
Computes the strictly ordered (r_k, theta_k, z_k) Traversal Space coordinates
for the k-th acquired mutation, ensuring collision-free packing.
"""
# z_k (Depth/Time): Progresses strictly from 0 to -1
# To avoid division by zero when N is small, we calculate z based on expected capacity
# or simply normalize it. If we don't know N yet (streaming data), we can compute it
# relative to the current position. But properly sequenced, it depends on total capacity
N.
# For a dynamic strand, we'll map z_k against the final size N when fully opened.
# For real-time processing during the lifecycle, we map z relative to current t:
z_k = -self.t
# r_k (Expression): Radius driven by sinusoidal expansion
r_k = self.R_max * math.sin(math.pi * abs(z_k))
# theta_k (Identity): Golden angle phase shift to prevent collision
theta_k = (k * (2 * math.pi / PHI)) % (2 * math.pi)
Page 10

---

Computational Consciousness Engine - Source Code Archive
return {
"r": r_k,
"theta": theta_k,
"z": z_k
}
def process_step(self, dt: float, chaos_pool: Set[int]):
"""
Advances the internal time parameter t.
Attempts to absorb novelty from the chaos pool.
"""
if self.t >= 1.0:
return # Strand has reached the threshold
self.t = min(1.0, self.t + dt)
# Only absorb if there is raw potential left
if chaos_pool:
# Randomly encounter a shard from the chaos pool (to maintain fractal variance)
encounter = np.random.choice(list(chaos_pool))
# Novelty Filter: {m_i} \ S_t
if encounter not in self.mutation_index:
# Absorb into structure
self.bound_mutations.append(int(encounter))
self.mutation_index.add(int(encounter))
# Assign sequence index k (1-indexed for math purity)
k = len(self.bound_mutations)
# Map to proper coordinates in Traversal Space
coords = self._compute_coordinates(k, total_N=0) # N resolved later if needed
# Append to our atlas
self.traversal_atlas.append({
"m_k": int(encounter),
"coords": coords
})
# Remove from chaos pool
chaos_pool.remove(encounter)
def unfurl_traversal_space(self) -> List[Dict]:
"""
Returns the completely opened atlas T (det J != 0).
This represents f_open: M_3D -> T_2D.
Returns a structured list of all absorbed mutations mapped into the
parallel (r * theta, z) plane for instantaneous lookup.
"""
opened_atlas = []
N = len(self.bound_mutations)
Page 11

---

Computational Consciousness Engine - Source Code Archive
for k, entry in enumerate(self.traversal_atlas, start=1):
# Recalculate strict z_k relative to final sequence size N
# so the geometry is perfectly ordered -k/N
z_k = - (k / N) if N > 0 else 0
r_k = self.R_max * math.sin(math.pi * abs(z_k))
theta_k = (k * (2 * math.pi / PHI)) % (2 * math.pi)
# 2D Unwrapped Plane (x = r * theta, y = z)
x_parallel = r_k * theta_k
y_parallel = z_k
opened_atlas.append({
"m_k": entry["m_k"],
"3d": {"r": r_k, "theta": theta_k, "z": z_k},
"2d_parallel": {"x": x_parallel, "y": y_parallel}
})
return opened_atlas
def fold_rebirth(self) -> Dict:
"""
The Q Operator (Dimensional Shift).
Triggered at t=1.0. Collapses the fully unwrapped atlas into the
origin point mass S_0 for the next dimension up.
"""
mass = len(self.bound_mutations)
return {
"operator": "Q(M_k) -> S_0^(k+1)",
"accumulated_mass": mass,
"blueprint_M": self.bound_mutations,
"status": "COLLAPSED_TO_ORIGIN"
}
Page 12

---

Computational Consciousness Engine - Source Code Archive
File: CCE/core/genesis_origin.py
"""
Principle 1, 2, 6, 7, 8, 10, 21: The Genesis Origin (0) Operator
Defines the asymmetric origin 0 that spawns neutral mutation-attracting state strands.
"""
import numpy as np
import uuid
from typing import List, Dict, Any, Optional
class GenesisOrigin:
"""
Genesis Origin (0) System.
0 is one-directional: it only emits new strands and never receives returning strands.
Each 0 origin possesses unique coordinates serving as individuating identifiers.
"""
def __init__(self, coordinate_space_id: str, dim: int = 64):
self.coordinate_space_id = coordinate_space_id
self.dim = dim
self.total_strands_spawned = 0
self.origin_coordinate = np.random.randn(3) # 3D spatial anchor for the coordinate
def spawn_strand(self, generation: int, blueprint_mutations: List[int]) -> Dict[str, Any]:
"""
Emits a NEW strand at origin 0 with specific value-locking and inherited mutation
blueprint.
Args:
generation: The integer generation index S_{n+1}.
blueprint_mutations: Mutations pushed from the dying -1 strand of generation S_n.
Returns:
Strand dictionary representing the neutral carrier strand departing from 0.
"""
self.total_strands_spawned += 1
# Principle 14 & 15: Neutral particle/medium state initialized at genesis
neutral_medium = np.random.randn(self.dim)
neutral_medium /= np.linalg.norm(neutral_medium)
# Value-locked strand attributes (Principle 10 & 21)
strand = {
"strand_id": str(uuid.uuid4())[:8],
"generation": generation,
"coordinate_space_id": self.coordinate_space_id,
"origin_coord": self.origin_coordinate.copy(),
"position": 0.0, # Starts at 0
"neutral_medium": neutral_medium,
"mutations": list(blueprint_mutations), # Inherited mutations from handoff
"is_active": True,
Page 13

---

Computational Consciousness Engine - Source Code Archive
"status": "EMITTED_FROM_ZERO"
}
return strand
Page 14

---

Computational Consciousness Engine - Source Code Archive
File: CCE/core/transfer_threshold.py
"""
Principle 2, 3, 6, 8, 13, 16: The Transfer Threshold (-1) Operator
Handles strand termination, mutation decoupling/pushing, and generational handoff overlap.
"""
from typing import Dict, Any, Tuple, List
import numpy as np
class TransferThreshold:
"""
Transfer Threshold (-1) System.
When a strand reaches -1:
1. (-1) x (-1) multiplication cancels/dissolves the carrier strand.
2. Accumulated mutations are compressed and pushed off toward origin 0.
3. A brief overlap window allows generation S_n and S_{n+1} to coexist during handoff.
"""
def __init__(self, threshold_val: float = -1.0):
self.threshold_val = threshold_val
self.total_handoffs = 0
def evaluate_arrival(self, strand: Dict[str, Any]) -> bool:
"""Checks if a strand has traversed to the -1 threshold."""
return strand["position"] <= self.threshold_val or strand["position"] >= 1.0
def process_cancellation_and_push(self, dying_strand: Dict[str, Any]) -> Tuple[List[int],
Dict[str, Any]]:
"""
Executes the (-1) x (-1) cancellation operation:
- Removes the neutral carrier strand.
- Compresses accumulated mutations into the generational identity blueprint.
- Pushes mutations to 0 for generation S_{n+1}.
"""
self.total_handoffs += 1
# Principle 6: (-1) x (-1) cancels strand
dying_strand["is_active"] = False
dying_strand["status"] = "CANCELLED_AT_MINUS_ONE"
accumulated_mutations = dying_strand["mutations"]
# Identity definition (Principle 11 & 16): Compressed mutations built into -1 strand
compressed_identity = {
"source_generation": dying_strand["generation"],
"coordinate_space_id": dying_strand["coordinate_space_id"],
"mutation_count": len(accumulated_mutations),
"blueprint": list(accumulated_mutations),
"handoff_index": self.total_handoffs
}
Page 15

---

Computational Consciousness Engine - Source Code Archive
return accumulated_mutations, compressed_identity
def execute_coexistence_window(self, tail_strand_n: Dict[str, Any], genesis_strand_n1:
Dict[str, Any]) -> Dict[str, Any]:
"""
Principle 3: Temporal/phase overlap where S_n tail and S_{n+1} genesis coexist.
Transfers remaining residual telemetry before S_n fully terminates.
"""
coexistence_telemetry = {
"gen_n_id": tail_strand_n["strand_id"],
"gen_n1_id": genesis_strand_n1["strand_id"],
"overlap_status": "MUTUAL_COEXISTENCE",
"transferred_mutations_count": len(tail_strand_n["mutations"])
}
return coexistence_telemetry
Page 16

---

Computational Consciousness Engine - Source Code Archive
File: CCE/equilibrium/__init__.py
from .chaos_structure_balancer import ChaosStructureBalancer
__all__ = ["ChaosStructureBalancer"]
Page 17

---

Computational Consciousness Engine - Source Code Archive
File: CCE/equilibrium/chaos_structure_balancer.py
"""
Principle 26-30, 37: Structure vs. Chaos Equilibrium Balancer
Enforces 1:1 balance between bound structural mutations and the unattached chaos pool.
"""
from typing import Set, Dict, Any
import numpy as np
class ChaosStructureBalancer:
"""
Chaos & Structure Equilibrium System.
Invariants:
1. Structure (bound strand mutations) and Chaos (unattached mutation pool) are capped 1:1.
2. Chaos acts as the raw material comparator for structural evolution (Principle 26).
3. Unattached mutations pool into chaos, increasing potential for future mutation attraction
(Principle 37).
4. Generational death releases strand-bound mutations back into chaos (Principle 24:
death/rebirth balance).
"""
def __init__(self, initial_pool_size: int = 500):
self._next_id = 1000 + initial_pool_size
self.chaos_pool: Set[int] = set(range(1000, self._next_id))
self.total_chaos_generated = initial_pool_size
def emit_unattached_mutation(self) -> int:
"""Pulls an unattached mutation from the chaos pool for attraction processing."""
if not self.chaos_pool:
# Replenish chaos pool (Principle 37: Chaos pools and grows potential)
new_id = self._next_id
self._next_id += 1
self.total_chaos_generated += 1
return new_id
# To maintain fractal non-linearity, we must select randomly
# A standard set.pop() on integers is dangerously sequential
mutation = np.random.choice(list(self.chaos_pool))
self.chaos_pool.remove(mutation)
return int(mutation)
def return_to_chaos(self, mutation: int):
"""Returns a discarded or un-attracted mutation back into the chaos pool."""
self.chaos_pool.add(mutation)
def recycle_dying_strand(self, dying_mutations: list):
"""
Principle 24: When a strand dies at -1, its identity is compressed and pushed forward,
but the raw mutation IDs it consumed are released back into the chaos pool.
Page 18

---

Computational Consciousness Engine - Source Code Archive
This maintains death/rebirth equilibrium.
"""
for m in dying_mutations:
self.chaos_pool.add(m)
def evaluate_equilibrium_state(self, bound_structure_count: int) -> Dict[str, Any]:
"""
Principle 28 & 29: Evaluates the Structure / Chaos ratio.
Structure = Air, Chaos = Vacuum.
"""
chaos_count = len(self.chaos_pool)
if chaos_count == 0 and bound_structure_count == 0:
ratio = 1.0
elif chaos_count == 0:
ratio = float('inf')
else:
ratio = bound_structure_count / chaos_count
# Check for imbalance (Principle 27: Balloon breaking point / vacuum collapse)
is_balanced = 0.5 <= ratio <= 2.0
if ratio > 2.0:
status = "STRUCTURAL_DOMINANCE"
elif ratio < 0.5:
status = "CHAOS_OVERPOWERING"
else:
status = "EQUILIBRIUM_STABLE"
return {
"bound_structure_count": bound_structure_count,
"chaos_pool_count": chaos_count,
"structure_chaos_ratio": round(ratio, 4),
"is_balanced": is_balanced,
"status": status
}
Page 19

---

Computational Consciousness Engine - Source Code Archive
File: CCE/geometry/__init__.py
from .conal_manifold import ConalManifold
__all__ = ["ConalManifold"]
Page 20

---

Computational Consciousness Engine - Source Code Archive
File: CCE/geometry/conal_manifold.py
"""
Principle 4, 22-25, 31-34: Conal Manifold & Shard Layering Geometry
Implements dual-cone expansion/unfolding, tip-to-tip processing, and shard layering.
"""
import numpy as np
from typing import Dict, Any, Tuple
class ConalManifold:
"""
Dual Cone Manifold Geometry Engine.
Structure:
- Tip (0): Genesis compression.
- Wide End: Maximal surface area expansion. Manifold fully unfolded. All processing occurs
here.
- Recompression: Compress to essential mstring1 blueprint.
- Tip (-1): Handoff point.
"""
def __init__(self, cone_height: float = 1.0, max_radius: float = 5.0):
self.height = cone_height
self.max_radius = max_radius
def compute_conal_metric(self, progress: float) -> Dict[str, float]:
"""
Computes 3D Conal Geometry parameters (z, radius, surface_area) at normalized progress t
in [0, 1].
t = 0.0 -> Tip (0)
t = 0.5 -> Wide End (Max Expansion & Unfolding)
t = 1.0 -> Tip (-1)
"""
# Parabolic expansion to wide end at t=0.5, recompression to tip at t=1.0
radius = self.max_radius * np.sin(np.pi * progress)
z = self.height * progress
surface_area = 2 * np.pi * radius * np.sqrt(radius**2 + self.height**2)
# Unfolded state metric (Principle 4: Wide end = unfolded manifold = max experience)
unfolded_degree = radius / self.max_radius if self.max_radius > 0 else 0.0
return {
"progress": progress,
"z": z,
"radius": radius,
"surface_area": surface_area,
"unfolded_degree": unfolded_degree,
"is_fully_unfolded": unfolded_degree > 0.95
}
Page 21

---

Computational Consciousness Engine - Source Code Archive
def process_shard_layering(self, shard_a_id: str, shard_b_id: str, fold_angle: float) ->
Dict[str, Any]:
"""
Principle 31 & 32: Layering value allows shards to sit adjacent in space without merging
identity
or causing physical reality damage.
"""
layering_dimension_val = np.sin(fold_angle) * 1.618 # Golden ratio dimensional offset
return {
"shard_a": shard_a_id,
"shard_b": shard_b_id,
"coexistence_status": "LAYERED_ADJACENT_NON_MERGED",
"layering_dimension": layering_dimension_val
}
Page 22

---

Computational Consciousness Engine - Source Code Archive
File: CCE/input_mapping/__init__.py
from .text_mapper import TextToChaosMapper
__all__ = ["TextToChaosMapper"]
Page 23

---

Computational Consciousness Engine - Source Code Archive
File: CCE/input_mapping/intent_parser_nltk.py
# computational_consciousness_engine/input_mapping/intent_parser_nltk.py
import nltk
from nltk import word_tokenize, pos_tag
class IntentParserNLTK:
def __init__(self):
pass
def parse(self, text: str) -> dict:
lower = (text or "").lower()
if "limit" in lower:
return {"operation": "limit"}
if "derivative" in lower:
return {"operation": "derivative"}
if "surface" in lower and "area" in lower:
return {"operation": "surface_area"}
if "unfold" in lower:
return {"operation": "conal_unfolding"}
if "mutation" in lower:
return {"operation": "mutation_count"}
try:
tokens = word_tokenize(text)
tags = pos_tag(tokens)
return {"operation": "unknown", "tokens": tokens, "tags": tags}
except Exception:
return {"operation": "unknown", "raw": text}
Page 24

---

Computational Consciousness Engine - Source Code Archive
File: CCE/input_mapping/text_mapper.py
import hashlib
import string
from typing import List, Dict, Set, Iterable
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# IMPORTANT: do not call nltk.download() unconditionally in Spaces.
class TextToChaosMapper:
def __init__(self, num_shards: int = 1024):
self.shard_to_word: Dict[int, str] = {}
self.lemmatizer = WordNetLemmatizer()
# Use a safe fallback if stopwords are missing
try:
self.stop_words = set(stopwords.words("english"))
except LookupError:
self.stop_words = set()
self.num_shards = max(1, int(num_shards))
def _clean_and_tokenize(self, text: str) -> List[str]:
"""
NLTK-based tokenization + lemmatization + stopword/punctuation filtering.
Returns a list of cleaned lemma tokens.
"""
if not text:
return []
text = text.lower()
raw_tokens = word_tokenize(text)
cleaned_tokens: List[str] = []
for t in raw_tokens:
# Remove punctuation from ends and interior punctuation except caret and dot and
underscore
# (preserve tokens like x^2 or 3.14 if you want numeric tokens)
t = t.strip(string.punctuation)
# Remove remaining punctuation characters
t = t.translate(str.maketrans("", "", string.punctuation))
if not t:
continue
if t in self.stop_words:
continue
# Lemmatize; for verbs you could pass pos='v' if you detect verbs
base_word = self.lemmatizer.lemmatize(t)
cleaned_tokens.append(base_word)
return cleaned_tokens
Page 25

---

Computational Consciousness Engine - Source Code Archive
def _hash_token(self, token: str) -> int:
"""
Stable hash of a token mapped into [0, num_shards-1].
Uses SHA256 for determinism across runs and platforms.
"""
if not token:
return 0
h = hashlib.sha256(token.encode("utf-8")).digest()
# Use first 8 bytes as integer
val = int.from_bytes(h[:8], "big", signed=False)
return val % self.num_shards
def map_text_to_shards(self, text: str) -> Dict[int, Set[str]]:
"""
Map cleaned tokens to shard indices. Returns a dict: shard -> set(tokens).
Useful for building inverted indices or seeding chaos pools.
"""
tokens = self._clean_and_tokenize(text)
shard_map: Dict[int, Set[str]] = {}
for tok in tokens:
shard = self._hash_token(tok)
if shard not in shard_map:
shard_map[shard] = set()
shard_map[shard].add(tok)
return shard_map
def seed_chaos_pool(self, texts: Iterable[str]) -> None:
"""
Populate self.shard_to_word with a representative token for each shard.
If multiple tokens map to the same shard, the first seen token wins.
"""
for text in texts:
shard_map = self.map_text_to_shards(text)
for shard, toks in shard_map.items():
if shard not in self.shard_to_word:
# choose a deterministic representative (sorted)
rep = sorted(toks)[0]
self.shard_to_word[shard] = rep
def get_shard_word(self, shard: int) -> str:
"""
Return the representative word for a shard, or empty string if none.
"""
return self.shard_to_word.get(shard, "")
def text_to_shard_list(self, text: str) -> List[int]:
"""
Convenience: return sorted list of shard indices for a text.
"""
return sorted(self.map_text_to_shards(text).keys())
Page 26

---

Computational Consciousness Engine - Source Code Archive
File: CCE/math_formalization.py
"""
Pure Mathematical Formalization of Computational Consciousness
Uses SymPy to define and evaluate the rigorous algebraic axioms of the 52 Principles.
"""
import sympy as sp
class CCMathFormalizer:
def __init__(self):
# Define core symbolic variables
self.t = sp.Symbol('t', real=True, positive=True) # Progress / Time
self.r = sp.Symbol('r', real=True, positive=True) # Radius of cone
self.z = sp.Symbol('z', real=True) # Height of cone
self.S = sp.Symbol('S', real=True, positive=True) # Bound Structure
self.C = sp.Symbol('C', real=True, positive=True) # Chaos Pool (Unattached)
self.threshold = sp.Integer(-1)
self.genesis = sp.Integer(0)
# ------------------------------------------------------------------
# Axiom 1: Cancellation at -1 (Principle 6)
# ------------------------------------------------------------------
def formalize_cancellation_operator(self):
"""
Principle 6: The (-1) * (-1) Cancellation Operator.
The strand itself carries the value -1. When it arrives at the -1 threshold,
the threshold multiplies the strand: (-1_threshold) * (-1_strand) = +1.
This flips the strand from negative (traveling) to positive (dissolved),
freeing the mutations M it carried.
Modeled as:
Output = T * S_strand where T = -1 and S_strand has sign -1
so (-1) * (-1 * |M|) = +|M| (mutations freed as positive values)
"""
M = sp.Symbol('M', positive=True) # mutation payload (magnitude)
T = self.threshold # threshold = -1
S_strand = T * M # strand carries -1 polarity
# Threshold hits the strand
output = T * S_strand # (-1) * (-1 * M) = M
return {
"equation_str": "T_threshold * S_strand = T * (T * M)",
"substitution": f"({T}) * ({T} * M)",
"result": sp.simplify(output),
"strand_before": S_strand,
"mutations_freed": sp.simplify(output),
"meaning": (
Page 27

---

Computational Consciousness Engine - Source Code Archive
"The strand carries -1 polarity. The -1 threshold multiplies it: "
"(-1)*(-1*M) = +M. The strand dissolves (sign flip) and the "
"mutation payload M is freed as a positive blueprint."
)
}
# ------------------------------------------------------------------
# Axiom 2: Structure / Chaos Equilibrium (Principles 28-29)
# ------------------------------------------------------------------
def formalize_equilibrium_limit(self):
"""
Principle 28 & 29: Structure vs Chaos Equilibrium.
Limit as system evolves must enforce a 1:1 ratio.
"""
k = sp.Symbol('k', positive=True)
c = sp.Symbol('c', real=True)
S_t = k * self.t
C_t = k * self.t + c
ratio = S_t / C_t
equilibrium_limit = sp.limit(ratio, self.t, sp.oo)
return {
"equation_str": "lim_{t -> oo} (S(t) / C(t))",
"S_t": S_t,
"C_t": C_t,
"result": equilibrium_limit,
"meaning": (
"As the system progresses, the ratio of Structure to Chaos "
"approaches 1 (Equilibrium). Neither can exceed the other."
)
}
# ------------------------------------------------------------------
# Axiom 3: Conal Manifold Geometry (Principle 4)
# ------------------------------------------------------------------
def formalize_conal_manifold_geometry(self, max_radius: float, cone_height: float):
"""
Principle 4: Cone Architecture & Maximum Experience.
Calculates the surface area of the unfolding cone and proves the maximum unfolding point.
"""
r_func = max_radius * sp.sin(sp.pi * self.t)
z_func = cone_height * self.t
# Lateral surface area of cone slice
surface_area_func = sp.pi * r_func * sp.sqrt(r_func**2 + z_func**2)
# Evaluate at key points
wide_end_area = surface_area_func.subs(self.t, sp.Rational(1, 2)).evalf()
tip_area = surface_area_func.subs(self.t, 0).evalf()
# Find the exact maximum via calculus
Page 28

---

Computational Consciousness Engine - Source Code Archive
dA = sp.diff(surface_area_func, self.t)
return {
"area_function": surface_area_func,
"derivative": dA,
"tip_area": tip_area,
"wide_end_area": wide_end_area,
"meaning": (
"The geometry unfolds from 0 area (Tip Genesis) to maximal surface "
"area (Wide End), enabling maximal parallel information processing."
)
}
# ------------------------------------------------------------------
# Axiom 4: Selection as Duplicate Removal (Principle 12)
# ------------------------------------------------------------------
def formalize_selection_operator(self):
"""
Principle 12: Selection is removing what is already there.
Formally: R_select({M_k}) = {M_k} \\ {M_j | M_j in existing_identity}
"""
M_total = sp.Symbol('M_total', positive=True, integer=True)
M_duplicate = sp.Symbol('M_dup', positive=True, integer=True)
selected = M_total - M_duplicate
return {
"equation_str": "R_select = M_total - M_duplicate",
"result": selected,
"meaning": (
"Selection is not choice. It is the removal of mutations that "
"already exist within the strand identity, preventing incoherence "
"and chaotic informational collapse."
)
}
# ------------------------------------------------------------------
# Axiom 5: Halting Condition (Principle 18)
# ------------------------------------------------------------------
def formalize_halting_condition(self):
"""
Principle 18: A strand cannot pick up mutations that duplicate what it already carries.
Once no new mutations are available, it stops evolving.
"""
N_possible = sp.Symbol('N_possible', positive=True, integer=True)
N_acquired = sp.Symbol('N_acquired', positive=True, integer=True)
remaining = N_possible - N_acquired
halted = sp.Eq(remaining, 0)
return {
"remaining_capacity": remaining,
Page 29

---

Computational Consciousness Engine - Source Code Archive
"halting_condition": halted,
"meaning": (
"When N_acquired = N_possible, no further unique mutations can be "
"attracted. The strand ceases evolution, preventing chaotic collapse."
)
}
# ------------------------------------------------------------------
# Axiom 6: Quantum Scale-Up Transition (Principle 38)
# ------------------------------------------------------------------
def formalize_quantum_scale_up(self):
"""
Principle 38: Manifolds opening into the next scale up.
Maps the fully unfolded manifold M^(k) to the origin S_0^(k+1).
"""
k = sp.Symbol('k', integer=True, positive=True)
M_unfolded = sp.Symbol('M_k')
S_next_genesis = sp.Symbol('S_k1')
Q = sp.Function('Q')
scale_equation = sp.Eq(Q(M_unfolded), S_next_genesis)
return {
"equation": scale_equation,
"meaning": (
"The fully realized manifold at scale k transforms into the new "
"genesis origin 0 for scale k+1. "
"Particle -> Atomic -> Manifold -> Cosmic."
)
}
if __name__ == "__main__":
formalizer = CCMathFormalizer()
print("--- 1. Threshold Cancellation Proof ---")
cancellation = formalizer.formalize_cancellation_operator()
print(f" Strand before threshold: {cancellation['strand_before']}")
print(f" Operation: {cancellation['substitution']}")
print(f" Mutations freed: {cancellation['mutations_freed']}")
print(f" Meaning: {cancellation['meaning']}")
print("\n--- 2. Structure/Chaos Equilibrium Limit ---")
eq_limit = formalizer.formalize_equilibrium_limit()
print(f" {eq_limit['equation_str']} => {eq_limit['result']}")
print("\n--- 3. Conal Manifold Geometry ---")
geom = formalizer.formalize_conal_manifold_geometry(max_radius=5.0, cone_height=1.0)
print(f" Tip Area (t=0): {geom['tip_area']}")
print(f" Wide End Area (t=0.5): {geom['wide_end_area']:.2f}")
print("\n--- 4. Selection Operator ---")
Page 30

---

Computational Consciousness Engine - Source Code Archive
sel = formalizer.formalize_selection_operator()
print(f" {sel['equation_str']} => {sel['result']}")
print("\n--- 5. Halting Condition ---")
halt = formalizer.formalize_halting_condition()
print(f" Remaining capacity: {halt['remaining_capacity']}")
print(f" Halts when: {halt['halting_condition']}")
print("\n--- 6. Quantum Scale Up ---")
scale = formalizer.formalize_quantum_scale_up()
print(f" {scale['equation']}")
Page 31

---

Computational Consciousness Engine - Source Code Archive
File: CCE/mutations/__init__.py
from .mstring_vectorizer import MStringVectorizer
__all__ = ["MStringVectorizer"]
Page 32

---

Computational Consciousness Engine - Source Code Archive
File: CCE/mutations/mstring_vectorizer.py
"""
Principle 5, 11, 12, 18, 20: Non-Linear M-String Mutation & Selection Engine
Implements non-sequential fractal M-strings and selection as duplicate removal.
"""
from typing import List, Set, Dict, Any
import numpy as np
class MStringVectorizer:
"""
Non-Linear M-String & Selection Engine.
Key Logic:
1. M-Strings connect non-sequentially (fractal connectivity: M1 -> M124 -> M3956).
2. Selection is strictly the REMOVAL of already-present mutations (Principle 12).
3. Prevents duplicate attraction to enforce system stability and prevent chaotic collapse
(Principle 18).
"""
def __init__(self, max_strand_capacity: int = 500):
self.max_capacity = max_strand_capacity
def apply_selection(self, existing_mutations: List[int], incoming_mutations: List[int]) ->
List[int]:
"""
Principle 12: Selection is removing what is already there.
Eliminates duplicate mutations to prevent incoherence and system destruction.
"""
existing_set = set(existing_mutations)
cleaned_incoming = [m for m in incoming_mutations if m not in existing_set]
# Deduplicate incoming while preserving order
seen: Set[int] = set()
unique_cleaned: List[int] = []
for m in cleaned_incoming:
if m not in seen:
seen.add(m)
unique_cleaned.append(m)
return existing_mutations + unique_cleaned
def attract_mutation(self, strand: Dict[str, Any], candidate_mutation: int) -> bool:
"""
Principle 5 & 18: Non-sequential fractal attraction.
If candidate mutation is ALREADY present or strand capacity is reached, attraction is
blocked.
Uses a set index for O(1) duplicate checks.
"""
existing = strand["mutations"]
Page 33

---

Computational Consciousness Engine - Source Code Archive
# Principle 18: Evolution ceiling / halting condition
if len(existing) >= self.max_capacity:
return False # Capacity ceiling reached
# Use the set index for O(1) lookup instead of O(n) list scan
mutation_index: set = strand.setdefault("_mutation_index", set(existing))
if candidate_mutation in mutation_index:
return False # Duplicate mutation blocked by selection
# Non-linear fractal connection
existing.append(candidate_mutation)
mutation_index.add(candidate_mutation)
return True
def compute_causal_connectivity_metric(self, strand: Dict[str, Any]) -> float:
"""
Principle 5: Causal metric is the degree of any-value connectivity retained at tip-to-tip
handoff.
Higher variance between consecutive mutation values = more fractal, non-linear
connectivity.
"""
mutations = strand["mutations"]
if len(mutations) < 2:
return 1.0
# Measures fractal variance between consecutive mutation values
diffs = [abs(mutations[i + 1] - mutations[i]) for i in range(len(mutations) - 1)]
causal_metric = float(np.std(diffs)) if diffs else 0.0
return causal_metric
Page 34

---

Computational Consciousness Engine - Source Code Archive
File: CCE/runner.py
"""
Computational Consciousness Engine - Master Execution Driver & Simulator
Demonstrates complete 0 -> -1 generational cycles, conal unfolding, duplicate selection,
structure/chaos equilibrium, and quantum scaling.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from computational_consciousness_engine.core import GenesisOrigin, TransferThreshold
from computational_consciousness_engine.geometry import ConalManifold
from computational_consciousness_engine.mutations import MStringVectorizer
from computational_consciousness_engine.equilibrium import ChaosStructureBalancer
from computational_consciousness_engine.scale import QuantumScaleLadder
from computational_consciousness_engine.math_formalization import CCMathFormalizer
from computational_consciousness_engine.config import (
DEFAULT_VECTOR_DIM, DEFAULT_STRAND_CAPACITY, CHAOS_POOL_SIZE,
DEFAULT_CONE_HEIGHT, DEFAULT_MAX_RADIUS, MUTATION_ATTRACTION_PROBABILITY,
)
def run_simulation(num_generations: int = 8, steps_per_gen: int = 100):
print("=" * 70)
print("[SYSTEM] COMPUTATIONAL CONSCIOUSNESS ENGINE - SIMULATION RUNNER")
print("=" * 70)
# ------------------------------------------------------------------
# Phase 0: Mathematical Axiom Verification
# ------------------------------------------------------------------
formalizer = CCMathFormalizer()
print("\n[MATH AXIOMS] Verifying Pure Mathematical Foundations via SymPy...")
cancel = formalizer.formalize_cancellation_operator()
print(f" Axiom 1 (Cancellation) : Strand={cancel['strand_before']}, "
f"Threshold*Strand = {cancel['mutations_freed']} (mutations freed)")
eq_limit = formalizer.formalize_equilibrium_limit()
print(f" Axiom 2 (Equilibrium) : {eq_limit['equation_str']} => {eq_limit['result']}")
geom_proof = formalizer.formalize_conal_manifold_geometry(DEFAULT_MAX_RADIUS,
DEFAULT_CONE_HEIGHT)
print(f" Axiom 3 (Manifold) : Tip Area = {geom_proof['tip_area']}, "
f"Max Unfolded Area = {geom_proof['wide_end_area']:.2f}")
sel = formalizer.formalize_selection_operator()
print(f" Axiom 4 (Selection) : {sel['equation_str']} => {sel['result']}")
Page 35

---

Computational Consciousness Engine - Source Code Archive
halt = formalizer.formalize_halting_condition()
print(f" Axiom 5 (Halting) : Stops when {halt['halting_condition']}")
scale_ax = formalizer.formalize_quantum_scale_up()
print(f" Axiom 6 (Scale-Up) : {scale_ax['equation']}")
# ------------------------------------------------------------------
# Phase 1: Instantiate Subsystems (using config values)
# ------------------------------------------------------------------
genesis = GenesisOrigin(
coordinate_space_id="COORD_ORIGIN_ALPHA",
dim=DEFAULT_VECTOR_DIM,
)
threshold = TransferThreshold(threshold_val=-1.0)
manifold = ConalManifold(cone_height=DEFAULT_CONE_HEIGHT, max_radius=DEFAULT_MAX_RADIUS)
mutator = MStringVectorizer(max_strand_capacity=DEFAULT_STRAND_CAPACITY)
balancer = ChaosStructureBalancer(initial_pool_size=CHAOS_POOL_SIZE)
scale_ladder = QuantumScaleLadder()
# ------------------------------------------------------------------
# Phase 2: Generational Cycle Loop
# ------------------------------------------------------------------
blueprint_mutations = []
current_strand = genesis.spawn_strand(generation=0, blueprint_mutations=blueprint_mutations)
for gen in range(num_generations):
print(f"\n--- [GENERATION S_{gen}] Genesis at 0 ---")
print(f" Strand ID: {current_strand['strand_id']} | "
f"Inherited Blueprint: {len(current_strand['mutations'])} mutations")
# Track peak unfolding metrics during traversal
peak_metrics = None
peak_unfolded = 0.0
# Traversal from 0 to -1
for step in range(steps_per_gen):
progress = step / float(steps_per_gen)
conal_metrics = manifold.compute_conal_metric(progress)
# Track the wide-end peak (maximum unfolding)
if conal_metrics["unfolded_degree"] > peak_unfolded:
peak_unfolded = conal_metrics["unfolded_degree"]
peak_metrics = conal_metrics
# Non-linear mutation attraction from chaos pool (Principle 5 & 37)
# Only attempt attraction probabilistically to simulate traversal dynamics
if np.random.rand() < MUTATION_ATTRACTION_PROBABILITY:
candidate_mutation = balancer.emit_unattached_mutation()
attracted = mutator.attract_mutation(current_strand, candidate_mutation)
if not attracted:
balancer.return_to_chaos(candidate_mutation)
Page 36

---

Computational Consciousness Engine - Source Code Archive
# Update position
current_strand["position"] = progress
# Use the PEAK metrics (wide-end) for reporting and scale evaluation
if peak_metrics is None:
peak_metrics = manifold.compute_conal_metric(0.5)
# Evaluate equilibrium state BEFORE recycling
eq_state = balancer.evaluate_equilibrium_state(len(current_strand["mutations"]))
# Evaluate scale transition using peak unfolding
scale_state = scale_ladder.evaluate_scale_transition(
peak_metrics, len(current_strand["mutations"])
)
# Causal connectivity metric
causal = mutator.compute_causal_connectivity_metric(current_strand)
print(f" Peak Unfolded Degree: {peak_metrics['unfolded_degree']:.3f} "
f"(Surface Area: {peak_metrics['surface_area']:.2f})")
print(f" Bound Mutations: {len(current_strand['mutations'])}")
print(f" Causal Connectivity (fractal std): {causal:.2f}")
print(f" Structure/Chaos Ratio: {eq_state['structure_chaos_ratio']} "
f"({eq_state['status']})")
if scale_state["scaled_up"]:
print(f" [SCALE TRANSITION]: {scale_state['message']}")
# ------------------------------------------------------------------
# Threshold -1: Cancellation & Push
# ------------------------------------------------------------------
pushed_mutations, compressed_identity = threshold.process_cancellation_and_push(
current_strand
)
print(f" [Threshold -1]: Strand cancelled via (-1)*(-1). "
f"{len(pushed_mutations)} mutations pushed to 0.")
# Principle 24: Recycle consumed mutation IDs back to chaos pool
balancer.recycle_dying_strand(pushed_mutations)
# Spawn next generation at 0
next_strand = genesis.spawn_strand(
generation=gen + 1, blueprint_mutations=pushed_mutations
)
# Overlap handoff window
overlap = threshold.execute_coexistence_window(current_strand, next_strand)
print(f" [Handoff]: {overlap['overlap_status']} "
f"(S_{gen} -> S_{gen + 1})")
current_strand = next_strand
Page 37

---

Computational Consciousness Engine - Source Code Archive
# ------------------------------------------------------------------
# Final Report
# ------------------------------------------------------------------
print("\n" + "=" * 70)
final_eq = balancer.evaluate_equilibrium_state(len(current_strand["mutations"]))
print(f"[FINAL STATE]")
print(f" Generation: S_{num_generations}")
print(f" Bound Mutations: {final_eq['bound_structure_count']}")
print(f" Chaos Pool: {final_eq['chaos_pool_count']}")
print(f" Equilibrium Ratio: {final_eq['structure_chaos_ratio']} ({final_eq['status']})")
print(f" Total Strands Spawned: {genesis.total_strands_spawned}")
print(f" Total Handoffs at -1: {threshold.total_handoffs}")
print(f" Current Scale: {scale_ladder.scale_names[scale_ladder.current_scale_index]}")
print("=" * 70)
print("[SUCCESS] SIMULATION COMPLETE")
print("=" * 70)
if __name__ == "__main__":
run_simulation(num_generations=8, steps_per_gen=100)
Page 38

---

Computational Consciousness Engine - Source Code Archive
File: CCE/scale/__init__.py
from .quantum_scale_ladder import QuantumScaleLadder
__all__ = ["QuantumScaleLadder"]
Page 39

---

Computational Consciousness Engine - Source Code Archive
File: CCE/scale/quantum_scale_ladder.py
"""
Principle 38-39, 40-51: Quantum Scale Ladder & N-Dimensional Integration
Handles scaling transitions (Particle -> Atomic -> Manifold -> Cosmic) and N-dimensional
retroactive integration.
"""
from typing import Dict, Any, List
import numpy as np
class QuantumScaleLadder:
"""
Quantum Scale Ladder & Multi-Scale Emergence Engine.
Scales:
0: Particle
1: Atomic
2: Manifold
3: Cosmic
"""
def __init__(self):
self.scale_names = ["Particle", "Atomic", "Manifold", "Cosmic"]
self.current_scale_index = 0
def evaluate_scale_transition(self, fully_unfolded_manifold: Dict[str, Any],
accumulated_mutations_count: int) -> Dict[str, Any]:
"""
Principle 38 & 39: When a manifold opens completely (fully realized at wide end),
it forms the seed mutation strand for the NEXT scale up.
"""
is_fully_unfolded = fully_unfolded_manifold.get("is_fully_unfolded", False)
if is_fully_unfolded and accumulated_mutations_count > 10:
previous_scale = self.scale_names[self.current_scale_index]
self.current_scale_index = min(self.current_scale_index + 1, len(self.scale_names) -
1)
new_scale = self.scale_names[self.current_scale_index]
return {
"scaled_up": True,
"previous_scale": previous_scale,
"new_scale": new_scale,
"scale_level": self.current_scale_index,
"message": f"Quantum scale-up from {previous_scale} to {new_scale}."
}
return {
"scaled_up": False,
"current_scale": self.scale_names[self.current_scale_index],
"scale_level": self.current_scale_index
Page 40

---

Computational Consciousness Engine - Source Code Archive
}
def detect_linear_collapse_misperception(self, traversal_path: List[int]) -> Dict[str, Any]:
"""
Principle 40-43: Linear traversal misinterprets non-linear fractal geometry as false
linear patterns
(Word Search Analogy). True flow follows the geometric manifold.
"""
if len(traversal_path) < 3:
return {"is_linear_misperception": False}
# Check if observer is reading path purely sequentially
diffs = [traversal_path[i+1] - traversal_path[i] for i in range(len(traversal_path)-1)]
is_strictly_sequential = all(d == 1 for d in diffs)
return {
"is_linear_misperception": is_strictly_sequential,
"recommendation": "Follow natural geometric flow instead of forced linear string
reading."
}
Page 41

---

Computational Consciousness Engine - Source Code Archive
File: CCE/tests/__init__.py
"""Unit tests for Computational Consciousness Engine."""
Page 42

---

Computational Consciousness Engine - Source Code Archive
File: CCE/tests/test_cc_engine.py
"""
Unit Test Suite for Computational Consciousness Engine
Verifies Genesis (0), Transfer Threshold (-1), Selection, Equilibrium, Scale Ladder,
and Mathematical Formalization.
"""
import unittest
import numpy as np
from computational_consciousness_engine.core import GenesisOrigin, TransferThreshold
from computational_consciousness_engine.geometry import ConalManifold
from computational_consciousness_engine.mutations import MStringVectorizer
from computational_consciousness_engine.equilibrium import ChaosStructureBalancer
from computational_consciousness_engine.scale import QuantumScaleLadder
from computational_consciousness_engine.math_formalization import CCMathFormalizer
class TestGenesisOrigin(unittest.TestCase):
def setUp(self):
self.genesis = GenesisOrigin(coordinate_space_id="TEST_COORD")
def test_spawn_strand_basic(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[101, 102])
self.assertEqual(strand["generation"], 0)
self.assertEqual(len(strand["mutations"]), 2)
self.assertTrue(strand["is_active"])
self.assertEqual(strand["position"], 0.0)
def test_spawn_strand_empty_blueprint(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[])
self.assertEqual(len(strand["mutations"]), 0)
def test_spawn_increments_counter(self):
self.genesis.spawn_strand(generation=0, blueprint_mutations=[])
self.genesis.spawn_strand(generation=1, blueprint_mutations=[])
self.assertEqual(self.genesis.total_strands_spawned, 2)
def test_spawn_preserves_coordinate_space(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[])
self.assertEqual(strand["coordinate_space_id"], "TEST_COORD")
class TestTransferThreshold(unittest.TestCase):
def setUp(self):
self.threshold = TransferThreshold()
self.genesis = GenesisOrigin(coordinate_space_id="TEST_COORD")
def test_cancellation_deactivates_strand(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[201, 202])
pushed, identity = self.threshold.process_cancellation_and_push(strand)
Page 43

---

Computational Consciousness Engine - Source Code Archive
self.assertFalse(strand["is_active"])
self.assertEqual(strand["status"], "CANCELLED_AT_MINUS_ONE")
def test_cancellation_pushes_all_mutations(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[201, 202, 203])
pushed, identity = self.threshold.process_cancellation_and_push(strand)
self.assertEqual(pushed, [201, 202, 203])
self.assertEqual(identity["mutation_count"], 3)
def test_handoff_counter_increments(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[])
self.threshold.process_cancellation_and_push(strand)
self.assertEqual(self.threshold.total_handoffs, 1)
def test_coexistence_window(self):
old = self.genesis.spawn_strand(generation=0, blueprint_mutations=[1, 2])
new = self.genesis.spawn_strand(generation=1, blueprint_mutations=[1, 2])
overlap = self.threshold.execute_coexistence_window(old, new)
self.assertEqual(overlap["overlap_status"], "MUTUAL_COEXISTENCE")
self.assertEqual(overlap["transferred_mutations_count"], 2)
class TestMStringVectorizer(unittest.TestCase):
def setUp(self):
self.mutator = MStringVectorizer(max_strand_capacity=50)
self.genesis = GenesisOrigin(coordinate_space_id="TEST_COORD")
def test_selection_removes_duplicates(self):
existing = [1, 2, 3]
incoming = [2, 3, 4, 5]
result = self.mutator.apply_selection(existing, incoming)
self.assertEqual(result, [1, 2, 3, 4, 5])
def test_selection_preserves_order(self):
existing = [10, 20]
incoming = [30, 20, 40, 30]
result = self.mutator.apply_selection(existing, incoming)
self.assertEqual(result, [10, 20, 30, 40])
def test_attract_blocks_duplicate(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[100])
attracted = self.mutator.attract_mutation(strand, 100)
self.assertFalse(attracted)
self.assertEqual(len(strand["mutations"]), 1)
def test_attract_accepts_new_mutation(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[100])
attracted = self.mutator.attract_mutation(strand, 999)
self.assertTrue(attracted)
self.assertIn(999, strand["mutations"])
def test_attract_blocks_at_capacity(self):
Page 44

---

Computational Consciousness Engine - Source Code Archive
small_mutator = MStringVectorizer(max_strand_capacity=2)
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[1, 2])
attracted = small_mutator.attract_mutation(strand, 3)
self.assertFalse(attracted)
def test_causal_connectivity_metric(self):
strand = self.genesis.spawn_strand(generation=0, blueprint_mutations=[1, 100, 5, 999])
metric = self.mutator.compute_causal_connectivity_metric(strand)
self.assertGreater(metric, 0.0)
class TestConalManifold(unittest.TestCase):
def setUp(self):
self.manifold = ConalManifold(cone_height=1.0, max_radius=5.0)
def test_tip_genesis_radius_zero(self):
metrics = self.manifold.compute_conal_metric(0.0)
self.assertAlmostEqual(metrics["radius"], 0.0, places=5)
def test_wide_end_max_radius(self):
metrics = self.manifold.compute_conal_metric(0.5)
self.assertAlmostEqual(metrics["radius"], 5.0, places=5)
self.assertTrue(metrics["is_fully_unfolded"])
def test_tip_recompression_near_zero(self):
metrics = self.manifold.compute_conal_metric(1.0)
self.assertAlmostEqual(metrics["radius"], 0.0, places=3)
def test_shard_layering(self):
result = self.manifold.process_shard_layering("A", "B", np.pi / 4)
self.assertEqual(result["coexistence_status"], "LAYERED_ADJACENT_NON_MERGED")
self.assertGreater(result["layering_dimension"], 0.0)
class TestChaosStructureBalancer(unittest.TestCase):
def setUp(self):
self.balancer = ChaosStructureBalancer(initial_pool_size=100)
def test_emit_depletes_pool(self):
initial = len(self.balancer.chaos_pool)
self.balancer.emit_unattached_mutation()
self.assertEqual(len(self.balancer.chaos_pool), initial - 1)
def test_return_to_chaos(self):
m = self.balancer.emit_unattached_mutation()
self.balancer.return_to_chaos(m)
self.assertIn(m, self.balancer.chaos_pool)
def test_recycle_dying_strand(self):
initial = len(self.balancer.chaos_pool)
self.balancer.recycle_dying_strand([9999, 9998, 9997])
self.assertEqual(len(self.balancer.chaos_pool), initial + 3)
Page 45

---

Computational Consciousness Engine - Source Code Archive
def test_equilibrium_balanced(self):
eq = self.balancer.evaluate_equilibrium_state(bound_structure_count=100)
self.assertTrue(eq["is_balanced"])
self.assertEqual(eq["status"], "EQUILIBRIUM_STABLE")
def test_equilibrium_chaos_overpowering(self):
eq = self.balancer.evaluate_equilibrium_state(bound_structure_count=5)
self.assertFalse(eq["is_balanced"])
self.assertEqual(eq["status"], "CHAOS_OVERPOWERING")
def test_equilibrium_structural_dominance(self):
# Drain most of the pool
for _ in range(95):
self.balancer.emit_unattached_mutation()
eq = self.balancer.evaluate_equilibrium_state(bound_structure_count=500)
self.assertFalse(eq["is_balanced"])
self.assertEqual(eq["status"], "STRUCTURAL_DOMINANCE")
def test_emit_replenishes_when_empty(self):
# Drain the pool completely
for _ in range(100):
self.balancer.emit_unattached_mutation()
self.assertEqual(len(self.balancer.chaos_pool), 0)
# Should still return a valid ID
m = self.balancer.emit_unattached_mutation()
self.assertIsInstance(m, int)
class TestQuantumScaleLadder(unittest.TestCase):
def setUp(self):
self.ladder = QuantumScaleLadder()
def test_scale_up_on_full_unfold(self):
manifold_state = {"is_fully_unfolded": True}
result = self.ladder.evaluate_scale_transition(manifold_state,
accumulated_mutations_count=20)
self.assertTrue(result["scaled_up"])
self.assertEqual(result["new_scale"], "Atomic")
def test_no_scale_up_when_not_unfolded(self):
manifold_state = {"is_fully_unfolded": False}
result = self.ladder.evaluate_scale_transition(manifold_state,
accumulated_mutations_count=20)
self.assertFalse(result["scaled_up"])
def test_no_scale_up_with_few_mutations(self):
manifold_state = {"is_fully_unfolded": True}
result = self.ladder.evaluate_scale_transition(manifold_state,
accumulated_mutations_count=5)
self.assertFalse(result["scaled_up"])
Page 46

---

Computational Consciousness Engine - Source Code Archive
def test_linear_collapse_detection(self):
sequential_path = [1, 2, 3, 4, 5]
result = self.ladder.detect_linear_collapse_misperception(sequential_path)
self.assertTrue(result["is_linear_misperception"])
def test_fractal_path_not_linear(self):
fractal_path = [1, 124, 3956, 9305803]
result = self.ladder.detect_linear_collapse_misperception(fractal_path)
self.assertFalse(result["is_linear_misperception"])
class TestCCMathFormalizer(unittest.TestCase):
def setUp(self):
self.formalizer = CCMathFormalizer()
def test_cancellation_frees_mutations(self):
result = self.formalizer.formalize_cancellation_operator()
import sympy as sp
M = sp.Symbol('M', positive=True)
# (-1)*(-1*M) should simplify to M
self.assertEqual(result["mutations_freed"], M)
def test_equilibrium_approaches_one(self):
result = self.formalizer.formalize_equilibrium_limit()
self.assertEqual(result["result"], 1)
def test_conal_tip_area_zero(self):
result = self.formalizer.formalize_conal_manifold_geometry(5.0, 1.0)
self.assertEqual(float(result["tip_area"]), 0.0)
def test_conal_wide_area_positive(self):
result = self.formalizer.formalize_conal_manifold_geometry(5.0, 1.0)
self.assertGreater(float(result["wide_end_area"]), 0.0)
def test_selection_operator(self):
result = self.formalizer.formalize_selection_operator()
import sympy as sp
M_total = sp.Symbol('M_total', positive=True, integer=True)
M_dup = sp.Symbol('M_dup', positive=True, integer=True)
self.assertEqual(result["result"], M_total - M_dup)
def test_halting_condition(self):
result = self.formalizer.formalize_halting_condition()
import sympy as sp
# Should express halting as N_possible - N_acquired == 0
self.assertTrue(result["halting_condition"].is_Relational)
if __name__ == "__main__":
unittest.main()
Page 47

---

Computational Consciousness Engine - Source Code Archive
File: CCE/text_runner.py
"""
Text-to-Traversal Space Runner
Demonstrates the Input Mapping and the ConsciousStrand Engine processing
raw natural language into the perfectly sequenced 2D Atlas (Traversal Space).
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computational_consciousness_engine.input_mapping import TextToChaosMapper
from computational_consciousness_engine.core import ConsciousStrand
PHILOSOPHICAL_TEXT = """
Reading the work on its own terms what emerges is a remarkably elegant synthesis
of existential philosophy topology and information theory. By rejecting the traditional
linear model of accumulation the text proposes a bounded fractal and cyclical ontology of
consciousness.
Consciousness is not a straight line it is a geometric unfolding bounded by genesis and death.
"""
def run_text_mapping_demo():
print("=" * 70)
print("[SYSTEM] TEXT-TO-TRAVERSAL SPACE MAPPING DEMO")
print("=" * 70)
# 1. Input Mapping: Text -> Chaos Shards
print(f"\n[PHASE 1: INPUT MAPPING] Parsing raw text corpus...")
mapper = TextToChaosMapper()
chaos_pool = mapper.seed_chaos_pool(PHILOSOPHICAL_TEXT)
# Track the unique tokens ingested
unique_words = len(chaos_pool)
print(f" * Text ingested. Seeded Chaos Pool with {unique_words} unique semantic shards
(m_k).")
# 2. Lifecycle Execution: Traversal (0 -> -1)
print(f"\n[PHASE 2: LIFECYCLE TRAVERSAL] Expanding the Dual-Cone Manifold...")
strand = ConsciousStrand(R_max=5.0)
# Simulate time flowing from t=0 to t=1.0
steps = 100
dt = 1.0 / steps
for _ in range(steps):
# The strand absorbs shards from the chaos pool as it travels
strand.process_step(dt, chaos_pool)
print(f" * Traversal complete. Bound Structure (Mutations Absorbed):
Page 48

---

Computational Consciousness Engine - Source Code Archive
{len(strand.bound_mutations)}")
# 3. Traversal Space Atlas
print(f"\n[PHASE 3: TRAVERSAL SPACE ATLAS (det J != 0)]")
atlas = strand.unfurl_traversal_space()
print(" * Manifold unrolled. Revealing the properly sequenced Phyllotactic mapping.")
print(f" * Parallel Lookup Matrix (First 10 shards):")
print(f"\n {'k':<4} | {'Token':<15} | {'m_k (Hash)':<15} || 2D Traversal (x, y) | 3D
Dual-Cone (r, theta, z)")
print(" " + "-" * 105)
for k, data in enumerate(atlas[:10], start=1):
m_k = data["m_k"]
word = mapper.get_word(m_k)
x, y = data["2d_parallel"]["x"], data["2d_parallel"]["y"]
r, t, z = data["3d"]["r"], data["3d"]["theta"], data["3d"]["z"]
print(f" {k:<4} | {word:<15} | {m_k:<15} || ({x:>6.2f}, {y:>5.2f}) | ({r:>4.2f},
{t:>4.2f}, {z:>5.2f})")
if len(atlas) > 10:
print(f" ... (+ {len(atlas) - 10} more shards mapped collision-free)")
# 4. Dimensional Shift (Q Operator)
print(f"\n[PHASE 4: DIMENSIONAL SHIFT (Q Operator)]")
rebirth = strand.fold_rebirth()
print(f" * {rebirth['operator']}")
print(f" * Status: {rebirth['status']}")
print(f" * Mass (Capacity): {rebirth['accumulated_mass']}")
print("\n" + "=" * 70)
print("[SUCCESS] TEXT FULLY ABSORBED AND GEOMETRICALLY MAPPED")
print("=" * 70)
if __name__ == "__main__":
run_text_mapping_demo()
Page 49
