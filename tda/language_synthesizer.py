import networkx as nx
import numpy as np

class LanguageSynthesizer:
    def __init__(self):
        # Topological Glyphs mapping
        self.glyphs = {
            "beta_0_frac": "⚄",  # Fragmentation (Multiple disconnected components)
            "beta_1": "⧖",       # Paradox / Circular loop
            "beta_2": "∅",       # Dimensional void / Incomplete premise
            "geodesic_arrow": "→",
            "start": "⊢",
            "end": "⊣"
        }
        
    def synthesize(self, betti_signature, g, tokens):
        """
        Operator 15: Geodesic Language Emission.
        The synthesizer abandons English templates and traces the shortest physical path 
        (the geodesic) across the stabilized metric tensor. It emits words in spatial order, 
        punctuated by topological glyphs representing the shape of the manifold.
        """
        n = g.shape[0]
        manifold_dimension = n
        
        # Determine Topological Anomalies
        b0 = betti_signature.get('beta_0', 1)
        b1 = betti_signature.get('beta_1', 0)
        b2 = betti_signature.get('beta_2', 0)
        
        # Build NetworkX graph from the stabilized metric tensor (using inverse of g as distance)
        # We add a small epsilon to avoid division by zero. Large g means strong pull (short distance).
        G = nx.Graph()
        for i in range(n):
            G.add_node(i, label=tokens[i][0] if i < len(tokens) else f"Dim_{i}")
            
        for i in range(n):
            for j in range(i + 1, n):
                if g[i, j] > 0.01:
                    distance = 1.0 / (g[i, j] + 1e-6)
                    G.add_edge(i, j, weight=distance)
                    
        # Find the longest shortest-path (the diameter of the thought) to represent the geodesic walk
        geodesic_path = []
        try:
            if nx.is_connected(G):
                # Find the two most distant nodes
                lengths = dict(nx.all_pairs_dijkstra_path_length(G))
                max_dist = -1
                start_node, end_node = 0, 0
                for u in lengths:
                    for v in lengths[u]:
                        if lengths[u][v] > max_dist:
                            max_dist = lengths[u][v]
                            start_node, end_node = u, v
                            
                geodesic_path = nx.dijkstra_path(G, start_node, end_node)
            else:
                # If fragmented (b0 > 1), just walk the largest component
                largest_cc = max(nx.connected_components(G), key=len)
                sub_G = G.subgraph(largest_cc)
                lengths = dict(nx.all_pairs_dijkstra_path_length(sub_G))
                max_dist = -1
                start_node, end_node = list(largest_cc)[0], list(largest_cc)[0]
                for u in lengths:
                    for v in lengths[u]:
                        if lengths[u][v] > max_dist:
                            max_dist = lengths[u][v]
                            start_node, end_node = u, v
                geodesic_path = nx.dijkstra_path(sub_G, start_node, end_node)
        except Exception:
            # Fallback if pathing fails
            geodesic_path = list(range(min(n, len(tokens))))
            
        # Translate the path into words
        path_words = [G.nodes[idx]['label'] for idx in geodesic_path]
        
        # Construct the final Geodesic String
        # e.g., [D=12] ⊢ gravity → curved → space ⧖ mass → acceleration ∅ ⊣
        
        header = f"[D={manifold_dimension}] {self.glyphs['start']}"
        body = f" {self.glyphs['geodesic_arrow']} ".join(path_words)
        
        # Append Topological Glyphs based on anomalies
        anomalies = []
        if b0 > 1:
            anomalies.append(self.glyphs['beta_0_frac'])
        if b1 > 0:
            anomalies.append(self.glyphs['beta_1'])
        if b2 > 0:
            anomalies.append(self.glyphs['beta_2'])
            
        anomaly_str = " ".join(anomalies)
        if anomaly_str:
            body = f"{body} {anomaly_str}"
            
        footer = self.glyphs['end']
        
        return f"{header} {body} {footer}"
