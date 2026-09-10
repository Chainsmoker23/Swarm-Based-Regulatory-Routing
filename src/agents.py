class ContextAgent:
    """
    Context Agents continuously evaluate the situational variables surrounding a specific transaction.
    They adjust the required constraints (C_max, P_max, S_min, L_max) based on risk.
    """
    def __init__(self, risk_profile='medium'):
        self.risk_profile = risk_profile

    def get_constraints(self):
        # Baseline constraints from the paper
        c_max = 500.0  # Max computational cost (ms)
        s_min = 0.7    # Min legal compliance strength
        l_max = 150.0  # Max latency (ms)

        if self.risk_profile == 'high':
            p_max = 0.15          # Stricter privacy for high risk
            risk_penalty = 0.8    # High dynamic risk penalty
        elif self.risk_profile == 'medium':
            p_max = 0.30
            risk_penalty = 0.4
        else: # low risk
            p_max = 0.50
            risk_penalty = 0.1

        return {
            'C_max': c_max, 
            'P_max': p_max, 
            'S_min': s_min, 
            'L_max': l_max, 
            'risk_penalty': risk_penalty
        }


class JurisdictionalAgent:
    """
    Jurisdictional Agents serve as immutable representatives of localized statutory law.
    They sit at the nodes and strictly enforce local parameters.
    """
    def __init__(self, node_id, local_strength_requirement=0.5):
        self.node_id = node_id
        self.local_strength_requirement = local_strength_requirement

    def validate_transition(self, edge_data):
        """
        Assesses if an incoming transition satisfies local statutory constraints.
        If a path doesn't meet this, it is blocked immediately by the guardian node.
        """
        # Simulated check: Edge compliance strength must meet the local requirement
        if edge_data['s'] < self.local_strength_requirement:
            return False
        return True
