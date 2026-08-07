import argparse
import numpy as np
from engine import AetheriusEngine

def run_simulation(text, use_hardcoded_adj=False):
    engine = AetheriusEngine()
    
    # We will artificially boost the step counter check to force a cascade in the prototype
    engine.cascade_mgr.tau_depth = 5 
    
    custom_adj = None
    if use_hardcoded_adj:
        # 0:truth, 1:lie, 2:real, 3:believed, 4:false, 5:reality
        custom_adj = np.zeros((6, 6))
        custom_adj[0, 1] = custom_adj[1, 0] = -0.9
        custom_adj[0, 2] = custom_adj[2, 0] = 0.8
        custom_adj[1, 2] = custom_adj[2, 1] = 0.8
        custom_adj[2, 3] = custom_adj[3, 2] = 0.7
        custom_adj[2, 4] = custom_adj[4, 2] = -0.9
        custom_adj[1, 4] = custom_adj[4, 1] = 0.8
        custom_adj[4, 5] = custom_adj[5, 4] = 0.8
        custom_adj[0, 5] = custom_adj[5, 0] = 0.9

    print("====================================================")
    print("INITIALIZING AETHERIUS PHYSICS ENGINE...")
    print("====================================================\\n")
    
    gmstring, betti = engine.process(text, custom_adjacency=custom_adj)
    
    print("\\n====================================================")
    print("[OUTPUT] Cognitive Resolution complete.")
    print("====================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aetherius Unified Engine CLI")
    parser.add_argument("--paradox", action="store_true", help="Run the hardcoded paradox simulation")
    parser.add_argument("--text", type=str, help="Run a custom sentence through the dynamic heuristic engine")
    args = parser.parse_args()
    
    if args.paradox:
        text = "The truth is a lie that becomes real only when believed, yet it remains false even after it changes reality."
        run_simulation(text, use_hardcoded_adj=True)
    elif args.text:
        run_simulation(args.text, use_hardcoded_adj=False)
    else:
        print('Please provide input text via --text "Your sentence here" or run the demo with --paradox')
