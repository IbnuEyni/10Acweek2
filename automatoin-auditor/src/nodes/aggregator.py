"""
Evidence Aggregator: Synchronization node between Detective and Judicial layers.
"""
from src.state import AgentState


def evidence_aggregator_node(state: AgentState) -> AgentState:
    """
    Synchronization point: Ensures all detective evidence is collected
    before passing to judges.
    
    This is the Fan-In node in the architecture.
    """
    evidences = state.get("evidences", {})
    
    # Validate we have evidence
    if not evidences:
        return {
            "errors": ["No evidence collected by detectives"],
            "evidences": {}
        }
    
    # Evidence is already aggregated via operator.ior reducer
    # This node just validates and passes through
    return {"evidences": evidences}
