"""
Test to verify parallel judicial execution.
"""
import pytest
from src.graph import build_audit_graph
from src.state import RubricDimension


def test_judicial_parallel_execution():
    """Verify all 3 judges execute in parallel from aggregator."""
    graph = build_audit_graph()
    
    # Get the compiled graph structure
    graph_dict = graph.get_graph().to_json()
    
    # Verify evidence_aggregator has edges to all 3 judges
    aggregator_edges = []
    for edge in graph_dict.get("edges", []):
        if edge.get("source") == "evidence_aggregator":
            aggregator_edges.append(edge.get("target"))
    
    # All 3 judges should be reachable from aggregator
    assert "prosecutor" in aggregator_edges, "Prosecutor not connected to aggregator"
    assert "defense" in aggregator_edges, "Defense not connected to aggregator"
    assert "tech_lead" in aggregator_edges, "Tech Lead not connected to aggregator"
    
    # Verify all 3 judges converge to chief_justice
    justice_inputs = []
    for edge in graph_dict.get("edges", []):
        if edge.get("target") == "chief_justice":
            justice_inputs.append(edge.get("source"))
    
    assert "prosecutor" in justice_inputs, "Prosecutor doesn't feed to chief_justice"
    assert "defense" in justice_inputs, "Defense doesn't feed to chief_justice"
    assert "tech_lead" in justice_inputs, "Tech Lead doesn't feed to chief_justice"
    
    print("✅ Parallel judicial execution verified!")
    print(f"   Aggregator → {aggregator_edges}")
    print(f"   {justice_inputs} → Chief Justice")


if __name__ == "__main__":
    test_judicial_parallel_execution()
