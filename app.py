import gradio as gr
import spaces
import numpy as np
from engine import AetheriusEngine
engine = AetheriusEngine()

@spaces.GPU
def process_thought(text, is_math=False):
    try:
        # Run the determinisic mathematical topology engine
        gmstring, betti, tokens, g = engine.process(text, is_math=is_math)
        qualia = engine.affective.get_qualia_state()
        
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
        
        qualia_output = (
            f"Thermodynamic Harmony: {qualia['harmony_metric']}\n"
            f"Alertness (Subconscious Heat): {qualia['alertness_metric']}\n"
            f"Manifold Disposition: {qualia['geometric_state']}\n"
            f"Relatable Emotion: {qualia['relatable_emotion']}"
        )
        
        return coord_string, tensor_string, gmstring['checksum'], topology_signature, qualia_output
    except Exception as e:
        return f"Error: {str(e)}", "Error", f"Error: {str(e)}", "N/A", "N/A"

with gr.Blocks(title="Aetherius: Computational Cognition Engine", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌌 Aetherius Cognitive Systems")
    gr.Markdown("Welcome to the **Aetherius Engine**. This system doesn't predict next tokens. It maps your input into a geometric manifold, applies a Ricci-Fisher flow operator, and stabilizes the topological structure into absolute mathematical reality.")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(label="Enter a logical statement, paradox, or thought", lines=3, placeholder="e.g., This statement is false.")
            is_math = gr.Checkbox(label="Is this a mathematical equation?")
            submit_btn = gr.Button("Resolve Geometry", variant="primary")
            
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
        inputs=[input_text, is_math],
        outputs=[coord_output, tensor_output, gm_output, betti_output, qualia_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)