from graph_generator import generate_regulatory_graph
from agents import ContextAgent, JurisdictionalAgent
from aco_swarm import ACOSwarm
from crypto_layer import CryptographicTranslationLayer
import json
import time

def run_transaction_simulation(risk_profile='medium'):
    print(f"\n--- Starting SBR^2 Transaction Simulation (Risk: {risk_profile.upper()}) ---")
    
    # 1. Instantiate Graph
    print("[1] Generating Regulatory Graph (200 nodes)...")
    G = generate_regulatory_graph(num_nodes=200)
    
    # Define source and target (e.g., US ESIGN to Swiss ZertES)
    source_node = 0
    target_node = 199 # Example target
    
    # 2. Deploy Agents
    context_agent = ContextAgent(risk_profile=risk_profile)
    constraints = context_agent.get_constraints()
    print(f"[2] Context Agent defined constraints: {constraints}")
    
    # Place a Jurisdictional Agent at an intermediate node (e.g., node 50)
    jurisdictional_agents = {
        50: JurisdictionalAgent(node_id=50, local_strength_requirement=0.8)
    }
    
    # 3. Swarm Optimization
    swarm = ACOSwarm(G, constraints)
    print("[3] Deploying ACO Swarm to find Pareto-optimal compliance pathway...")
    
    locked_path = None
    max_iterations = 50
    
    start_time = time.time()
    for iteration in range(max_iterations):
        successful_paths = swarm.find_path(source_node, target_node, jurisdictional_agents)
        locked_path = swarm.check_consensus(successful_paths)
        
        if locked_path:
            print(f"    -> Consensus Reached at Iteration {iteration + 1}!")
            break
            
    swarm_time = (time.time() - start_time) * 1000
    
    if not locked_path:
        print("[!] Swarm failed to reach temporal lock. Flagging for manual compliance triage.")
        return
        
    print(f"    -> Locked Pathway (P*): {locked_path}")
    print(f"    -> Swarm Convergence Time: {swarm_time:.2f} ms")
    
    # 4. Cryptographic Translation
    print("[4] Executing Cryptographic Translation Layer (PLONK)...")
    crypto_layer = CryptographicTranslationLayer()
    
    # Simulate payload ingestion
    payload = {"sig": "0x...", "pubkey": "0x...", "timestamp": time.time()}
    proof = crypto_layer.generate_proof(locked_path, payload)
    
    # 5. Guardrail / Decision Token
    decision_token = crypto_layer.synthesize_decision_token(locked_path, constraints, proof)
    
    print("\n=== Immutable Decision Token Generated ===")
    print(json.dumps(decision_token, indent=2))
    print("==========================================")
    print("\nTransaction successfully routed and cryptographically certified within SLAs.")

if __name__ == "__main__":
    run_transaction_simulation(risk_profile='medium')
    run_transaction_simulation(risk_profile='high')
