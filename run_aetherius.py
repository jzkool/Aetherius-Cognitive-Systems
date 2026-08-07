import argparse
import numpy as np
from engine import AetheriusEngine

def run_paradox_simulation():
    engine = AetheriusEngine()
    
    # Inject the exact paradox matrix we simulated earlier
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

    text = "The truth is a lie that becomes real only when believed, yet it remains false even after it changes reality."
    
    # We will artifically boost the step counter check to force a cascade in the prototype
    engine.cascade_mgr.tau_depth = 5 
    
    gmstring, betti = engine.process(text, custom_adjacency=custom_adj)
    print("\n[OUTPUT] Cognitive Resolution complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aetherius Unified Engine CLI")
    parser.add_argument("--paradox", action="store_true", help="Run the hardcoded paradox simulation")
    args = parser.parse_args()
    
    if args.paradox:
        run_paradox_simulation()
    else:
        print("Run with --paradox to see the live simulation!")
