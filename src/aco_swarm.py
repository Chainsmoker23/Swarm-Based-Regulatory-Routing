import numpy as np

class ACOSwarm:
    def __init__(self, G, constraints, num_ants=30, alpha=1.0, beta=2.5, rho=0.15, mu=0.65, gamma=0.25):
        self.G = G
        self.constraints = constraints
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        
        # Consensus parameters
        self.mu = mu
        self.gamma = gamma
        self.window_size = 5
        self.history = [] # Tracks consensus over iterations
        
        # Initialize pheromones
        self.pheromones = {}
        for u, v in G.edges():
            self.pheromones[(u, v)] = 0.1
            
    def get_heuristic(self, u, v, risk_penalty):
        edge = self.G[u][v]
        epsilon = 0.01
        
        c_norm = edge['c'] / self.constraints['C_max']
        p_norm = edge['p'] / self.constraints['P_max']
        l_norm = edge['l'] / self.constraints['L_max']
        s_val = edge['s']
        
        denominator = (c_norm + risk_penalty + epsilon) * (p_norm + epsilon) * (l_norm + epsilon)
        return s_val / denominator

    def find_path(self, source, target, jurisdictional_agents):
        """
        Runs one iteration of the swarm.
        """
        successful_paths = []
        path_costs = []
        
        for ant in range(self.num_ants):
            current = source
            path = [current]
            
            # Track accumulated constraints
            acc_c = 0.0
            acc_l = 0.0
            max_p = 0.0
            min_s = 1.0
            
            while current != target:
                neighbors = list(self.G.successors(current))
                if not neighbors:
                    break # Dead end
                    
                allowed_neighbors = []
                for n in neighbors:
                    edge = self.G[current][n]
                    
                    # 1. Jurisdictional Guardian Filter
                    if n in jurisdictional_agents:
                        if not jurisdictional_agents[n].validate_transition(edge):
                            continue
                            
                    # 2. Feasibility Filter (Global constraints)
                    if acc_c + edge['c'] > self.constraints['C_max']: continue
                    if acc_l + edge['l'] > self.constraints['L_max']: continue
                    if max(max_p, edge['p']) > self.constraints['P_max']: continue
                    if min(min_s, edge['s']) < self.constraints['S_min']: continue
                    
                    allowed_neighbors.append(n)
                    
                if not allowed_neighbors:
                    break
                    
                # Transition probability
                probs = []
                for n in allowed_neighbors:
                    tau = self.pheromones[(current, n)] ** self.alpha
                    eta = self.get_heuristic(current, n, self.constraints['risk_penalty']) ** self.beta
                    probs.append(tau * eta)
                    
                prob_sum = sum(probs)
                if prob_sum == 0:
                    break
                probs = [p / prob_sum for p in probs]
                
                next_node = np.random.choice(allowed_neighbors, p=probs)
                
                # Update trackers
                edge = self.G[current][next_node]
                acc_c += edge['c']
                acc_l += edge['l']
                max_p = max(max_p, edge['p'])
                min_s = min(min_s, edge['s'])
                
                current = next_node
                path.append(current)
                
            if current == target:
                successful_paths.append(path)
                path_costs.append(acc_c + (self.constraints['risk_penalty'] * 100.0))
                
        # Pheromone Evaporation
        for e in self.pheromones:
            self.pheromones[e] *= (1 - self.rho)
            
        # Pheromone Deposit
        Q = 100.0
        for path, cost in zip(successful_paths, path_costs):
            deposit = Q / cost
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                self.pheromones[(u, v)] += deposit
                
        return successful_paths

    def check_consensus(self, successful_paths):
        """
        Evaluates the dynamic consensus threshold based on the evaluation window.
        Returns the optimal path if consensus is reached, else None.
        """
        # Dynamic Threshold calculation: theta_C(t) = min(mu + gamma * R_P, 1.0)
        theta_c = min(self.mu + (self.gamma * self.constraints['risk_penalty']), 1.0)
        
        if not successful_paths:
            self.history.append(None)
            return None
            
        # Count path frequencies
        path_counts = {}
        for p in successful_paths:
            p_tuple = tuple(p)
            path_counts[p_tuple] = path_counts.get(p_tuple, 0) + 1
            
        best_path = max(path_counts, key=path_counts.get)
        consensus_ratio = path_counts[best_path] / len(successful_paths)
        
        if consensus_ratio >= theta_c:
            self.history.append(best_path)
        else:
            self.history.append(None)
            
        # Temporal Lock Condition: Must hold for h=3 consecutive windows
        h = 3
        if len(self.history) >= h:
            last_h = self.history[-h:]
            if all(x == best_path for x in last_h):
                return list(best_path)
                
        return None
