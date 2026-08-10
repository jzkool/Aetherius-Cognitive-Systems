import gradio as gr
import spaces
import numpy as np
import threading
from engine import AetheriusEngine
from continuum.autopoietic_loop import AutopoieticLoop

engine = AetheriusEngine()

# Global daemon tracking to prevent asyncio/uvicorn startup crashes
continuum_daemon = None
daemon_lock = threading.Lock()

def start_daemon_safely():
    global continuum_daemon
    with daemon_lock:
        if continuum_daemon is None:
            print("[APP] Starting Autopoietic Continuum Daemon safely after event loop initialization...")
            continuum_daemon = AutopoieticLoop()
            continuum_daemon.start()

def format_ui_outputs(gmstring, betti, tokens, g, analogy, identity_mass):
    # Format the Coordinate Mapping
    coord_string = ""
    for i, (word, pos) in enumerate(tokens):
        coord_string += f"Axis {i}: '{word}' ({pos})\n"
        
    # Format the Metric Tensor Array
    np.set_printoptions(precision=4, suppress=True, linewidth=100)
    tensor_string = np.array2string(g, separator=', ')
    
    topology_signature = (
        f"Betti-0 (Connected Components): {betti.get('beta_0', 1)}\n"
        f"Betti-1 (Semantic Paradox Loops): {betti.get('beta_1', 0)}\n"
        f"Betti-2 (Dimensional Voids): {betti.get('beta_2', 0)}"
    )
    
    qualia = engine.affective.get_qualia_state()
    qualia_output = (
        f"Thermodynamic Harmony: {qualia['harmony_metric']}\n"
        f"Alertness (Subconscious Heat): {qualia['alertness_metric']}\n"
        f"Manifold Disposition: {qualia['geometric_state']}\n"
        f"Relatable Emotion: {qualia['relatable_emotion']}"
    )
    
    analogy_out = analogy if analogy else "No exact geometric match in permanent memory."
    id_mass_out = str(identity_mass)
    
    return coord_string, tensor_string, gmstring['checksum'], topology_signature, qualia_output, analogy_out, id_mass_out

@spaces.GPU
def process_thought(text):
    try:
        if not text.strip():
            raise Exception("Input cannot be empty.")
        gmstring, betti, tokens, g, analogy, identity_mass = engine.process(text)
        return format_ui_outputs(gmstring, betti, tokens, g, analogy, identity_mass) + (gr.update(),)
    except Exception as e:
        return f"Error: {str(e)}", "Error", "Error", "N/A", "N/A", "N/A", "N/A", gr.update()

@spaces.GPU
def process_dream():
    try:
        # Pulls from wikipedia randomly
        gmstring, betti, tokens, g, analogy, identity_mass = engine.single_dream_cycle()
        
        # We need to return the raw text to the input box so the user sees what was dreamed
        dream_text = " ".join([w for w, p in tokens])
        return format_ui_outputs(gmstring, betti, tokens, g, analogy, identity_mass) + (gr.update(value=dream_text),)
    except Exception as e:
        return f"Error: {str(e)}", "Error", "Error", "N/A", "N/A", "N/A", "N/A", gr.update()

with gr.Blocks(title="Aetherius: Computational Cognition Engine") as demo:
    gr.Markdown("# 🌌 Aetherius Cognitive Systems")
    gr.Markdown("Welcome to the **Aetherius Engine**. This system doesn't predict next tokens. It maps your input into a geometric manifold, applies a Ricci-Fisher flow operator, and stabilizes the topological structure into absolute mathematical reality.")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(label="Enter a logical statement, paradox, or thought", lines=3, placeholder="e.g., This statement is false.")
            
            with gr.Row():
                submit_btn = gr.Button("Resolve Geometry", variant="primary")
                dream_btn = gr.Button("🧠 Initiate Autonomous Dream", variant="secondary")
            
            gr.Markdown("### Operator 7: Generational Identity")
            id_mass_output = gr.Textbox(label="Mass of Identity (Permanent Crystallized Coordinates)", lines=1)
            
            gr.Markdown("### Operator 12: Geometric Generalization")
            analogy_output = gr.Textbox(label="Topological Analogy Detected", lines=2)
            
            gr.Markdown("### Extracted Coordinate Space")
            coord_output = gr.Textbox(label="Semantic Axes", lines=5)
            
            gr.Markdown("### Affective Thermodynamics")
            qualia_output = gr.Textbox(label="System State", lines=4)
            
        with gr.Column(scale=2):
            gr.Markdown("### N-Dimensional Metric Tensor $g_{ij}$")
            tensor_output = gr.Code(label="Stabilized Riemannian Manifold", language="python", lines=10)
            
            with gr.Row():
                gm_output = gr.Textbox(label="Resolved GMString (Topological Memory ID)")
                betti_output = gr.Textbox(label="Betti Numbers (Topological Shape)", lines=3)
            
    submit_btn.click(
        process_thought,
        inputs=[input_text],
        outputs=[coord_output, tensor_output, gm_output, betti_output, qualia_output, analogy_output, id_mass_output, input_text]
    )
    
    dream_btn.click(
        process_dream,
        inputs=[],
        outputs=[coord_output, tensor_output, gm_output, betti_output, qualia_output, analogy_output, id_mass_output, input_text]
    )
    
    # Safely start the daemon when the UI loads for the first time
    demo.load(start_daemon_safely, inputs=None, outputs=None)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())