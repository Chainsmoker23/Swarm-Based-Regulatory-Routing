import networkx as nx
import numpy as np

def generate_regulatory_graph(num_nodes=200, seed=42, weight_seed=7):
    """
    Generates a Directed Acyclic Graph (DAG) representing the multi-jurisdictional 
    regulatory environment. The paper uses Price's citation model (approximated here 
    by ensuring strict directionality in a scale-free network).
    """
    # Generate a scale-free directed graph
    G_raw = nx.scale_free_graph(num_nodes, seed=seed)
    
    # Enforce DAG property by removing self loops and backward edges
    G = nx.DiGraph()
    G.add_nodes_from(G_raw.nodes())
    for u, v in G_raw.edges():
        if u < v:  # Strict ordering guarantees a DAG
            G.add_edge(u, v)
            
    # Remove isolated nodes and reconnect to ensure pathways exist
    # For a regulatory graph, we assume a connected component
    
    np.random.seed(weight_seed)
    
    # Assign the 4-dimensional weight vector to each edge:
    # w_ij = (c_ij, p_ij, s_ij, l_ij)
    for u, v in G.edges():
        G[u][v]['c'] = np.random.uniform(10, 200)   # Computational cost (ms)
        G[u][v]['p'] = np.random.uniform(0, 1)      # Privacy exposure
        G[u][v]['s'] = np.random.uniform(0.5, 1.0)  # Compliance strength
        G[u][v]['l'] = np.random.uniform(5, 50)     # Latency (ms)
        
    return G

if __name__ == "__main__":
    G = generate_regulatory_graph()
    print(f"Generated Regulatory DAG with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    if G.number_of_edges() > 0:
        sample_edge = list(G.edges(data=True))[0]
        print(f"Sample edge weight vector: {sample_edge}")
