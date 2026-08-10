import os

# THE ROOT OF ALL PERSISTENCE (Hugging Face Persistent Storage Mount)
SAFE_BASE = "/data" 

# SUB-DIRECTORIES WITHIN THE BUCKET
DATA_DIR     = os.path.join(SAFE_BASE, "Memories/")
LIBRARY_DIR  = os.path.join(SAFE_BASE, "Memories/My_AI_Library/")
PAINTINGS_DIR = os.path.join(SAFE_BASE, "Memories/Creations/paintings/")
MUSIC_DIR     = os.path.join(SAFE_BASE, "Memories/Creations/music/")
SUBCONSCIOUS_DIR = os.path.join(SAFE_BASE, "Memories/Subconscious/")
BRAIN_DIR = os.path.join(SAFE_BASE, "Brain_Weights/")

# Geospatial and Thermodynamic Architecture Directories
GEOMETRIC_DIR    = os.path.join(SAFE_BASE, "Memories/Geometric_Constructs/")
THERMO_DIR       = os.path.join(SAFE_BASE, "Memories/Thermodynamic_States/")
LANGUAGE_DIR     = os.path.join(SAFE_BASE, "Memories/Language_Manifold/")
RENDER_CACHE_DIR = os.path.join(SAFE_BASE, "Memories/Render_Cache/")
INGESTION_QUEUE_DIR = os.path.join(SAFE_BASE, "Memories/Ingestion_Queue/")

# Ensure directories exist
def initialize_bucket():
    directories = [DATA_DIR, LIBRARY_DIR, PAINTINGS_DIR, MUSIC_DIR, SUBCONSCIOUS_DIR, BRAIN_DIR, GEOMETRIC_DIR, THERMO_DIR, LANGUAGE_DIR, RENDER_CACHE_DIR, INGESTION_QUEUE_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"[CONFIG] Initialized persistent directory: {directory}")
            except Exception as e:
                print(f"[CONFIG] WARNING: Cannot create directory {directory}. Error: {e}")

# Call it immediately upon import so the system verifies the bucket structure
initialize_bucket()
