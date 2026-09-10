# Swarm-Based Regulatory Routing (SBR²)

This repository contains the simulation codebase for the paper: **"Swarm-Based Regulatory Routing: Context-Aware Compliance and Cryptographic Translation in Cross-Border Banking."**

## Disclaimer
Due to commercial confidentiality constraints, the complete production-grade source code (including enterprise rule engine API integrations, production QTSP handoffs, and full universal SRS parameters) is not publicly available for commercial use. 

This repository provides a fully functional simulation subset of the architecture to support reproducibility and understanding of the core mathematical and algorithmic concepts presented in the manuscript.

## Architecture Overview
SBR² resolves the multi-jurisdictional compliance friction in cross-border banking by treating regulatory translation as a Multi-Constrained Path (MCP) problem.
- **Swarm Intelligence Layer**: Uses Ant Colony Optimization (ACO) governed by Jurisdictional and Context Agents to probabilistically navigate cost, privacy, strength, and latency bounds.
- **Cryptographic Translation Layer**: Uses PLONK Zero-Knowledge Proofs to certify the signature, key entropy, freshness, and the exact pathway hash selected by the swarm.
- **Guardrails**: Synthesizes the execution into an immutable Decision Token ($T_{dec}$) for auditability.

## Structure
- `src/graph_generator.py`: Generates the regulatory DAG using Price's model logic.
- `src/agents.py`: Implements the `ContextAgent` and `JurisdictionalAgent`.
- `src/aco_swarm.py`: Core logic for the Ant Colony Optimization routing layer, including pheromone decay, heuristic desirability, and temporal consensus locking.
- `src/crypto_layer.py`: Simulates the PLONK cryptographic translation layer and Decision Token synthesis.
- `src/main_simulation.py`: Entry point to run transaction simulations under varying risk profiles.
- `src/circuit_template.circom`: A Circom template demonstrating the formalized arithmetic predicates.

## Usage
Install requirements and run the simulation:
```bash
pip install -r requirements.txt
python src/main_simulation.py
```

## License
Refer to the `LICENSE` file for details on usage rights.
