"""
LangGraph orchestration with parallel execution.
Implements fan-out/fan-in architecture for detective and judicial layers.

Key Patterns:
- StateGraph: LangGraph's declarative workflow engine
- Fan-Out: Single node branches to multiple parallel nodes
- Fan-In: Multiple nodes converge to single aggregator
- Parallel Execution: Nodes without dependencies run concurrently
"""
from langgraph.graph import StateGraph, END
from langgraph.graph.graph import CompiledGraph
from src.state import AgentState
from src.nodes.detectives import (
    repo_investigator_node,
    doc_analyst_node,
    vision_inspector_node
)
from src.nodes.aggregator import evidence_aggregator_node
from src.nodes.judges import prosecutor_node, defense_node, tech_lead_node
from src.nodes.justice import chief_justice_node


def build_audit_graph() -> CompiledGraph:
    """
    Build the multi-agent audit graph with parallel execution.
    
    Architecture:
        Detective Layer (Parallel) → Aggregator (Fan-In) → 
        Judicial Layer (Parallel) → Chief Justice → Report
    
    Parallel Execution:
        - Detective layer: 3 nodes run concurrently (repo, doc, vision)
        - Judicial layer: 3 nodes run concurrently (prosecutor, defense, tech_lead)
        - State reducers (operator.ior, operator.add) ensure thread-safe merging
    
    Returns:
        CompiledGraph: LangGraph StateGraph ready for execution
    """
    graph = StateGraph(AgentState)
    
    # Layer 1: Detective Layer (Parallel Evidence Collection)
    graph.add_node("repo_investigator", repo_investigator_node)
    graph.add_node("doc_analyst", doc_analyst_node)
    graph.add_node("vision_inspector", vision_inspector_node)
    
    # Layer 2: Evidence Aggregation (Fan-In)
    graph.add_node("evidence_aggregator", evidence_aggregator_node)
    
    # Layer 3: Judicial Layer (Parallel Evaluation)
    graph.add_node("prosecutor", prosecutor_node)
    graph.add_node("defense", defense_node)
    graph.add_node("tech_lead", tech_lead_node)
    
    # Layer 4: Supreme Court (Synthesis)
    graph.add_node("chief_justice", chief_justice_node)
    
    # Wire Detective Layer (Fan-Out)
    graph.set_entry_point("repo_investigator")
    graph.add_edge("repo_investigator", "evidence_aggregator")
    
    graph.set_entry_point("doc_analyst")
    graph.add_edge("doc_analyst", "evidence_aggregator")
    
    graph.set_entry_point("vision_inspector")
    graph.add_edge("vision_inspector", "evidence_aggregator")
    
    # Wire Judicial Layer (Fan-Out from Aggregator)
    graph.add_edge("evidence_aggregator", "prosecutor")
    graph.add_edge("evidence_aggregator", "defense")
    graph.add_edge("evidence_aggregator", "tech_lead")
    
    # Wire Supreme Court (Fan-In to Chief Justice)
    graph.add_edge("prosecutor", "chief_justice")
    graph.add_edge("defense", "chief_justice")
    graph.add_edge("tech_lead", "chief_justice")
    
    # End
    graph.add_edge("chief_justice", END)
    
    return graph.compile()
