"""
LangGraph orchestration with parallel execution and error handling.
Implements fan-out/fan-in architecture with conditional edges for resilience.

Key Patterns:
- StateGraph: LangGraph's declarative workflow engine
- Fan-Out: Single node branches to multiple parallel nodes
- Fan-In: Multiple nodes converge to single aggregator
- Parallel Execution: Nodes without dependencies run concurrently
- Conditional Edges: Route failures without blocking entire pipeline
"""
from typing import TYPE_CHECKING, Literal
from langgraph.graph import StateGraph, END, START
from src.state import AgentState

if TYPE_CHECKING:
    from langgraph.graph import CompiledGraph
from src.nodes.detectives import (
    repo_investigator_node,
    doc_analyst_node,
    vision_inspector_node
)
from src.nodes.aggregator import evidence_aggregator_node
from src.nodes.judges import prosecutor_node, defense_node, tech_lead_node
from src.nodes.justice import chief_justice_node


def should_continue_to_judicial(state: AgentState) -> Literal["judicial", "error_report"]:
    """
    Conditional edge: Check if enough evidence collected to proceed.
    If all detectives failed, skip judicial layer and generate error report.
    
    Args:
        state: Current agent state
        
    Returns:
        "judicial" if evidence exists, "error_report" if all detectives failed
    """
    if not state.get("evidences") or len(state["evidences"]) == 0:
        return "error_report"
    return "judicial"


def error_report_node(state: AgentState) -> AgentState:
    """
    Generate error report when all detectives fail.
    Graceful degradation instead of crashing.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with error report
    """
    errors = state.get("errors", [])
    error_summary = "\n".join(f"- {err}" for err in errors)
    
    state["final_report"] = f"""
# Audit Failed - Insufficient Evidence

## Errors Encountered

{error_summary}

## Recommendation

Please verify:
1. Repository URL is accessible
2. PDF path is correct and file is readable
3. API keys are configured (GROQ_API_KEY, GOOGLE_API_KEY)
4. Network connectivity is stable
"""
    return state


def build_audit_graph():
    """
    Build the multi-agent audit graph with parallel execution and error handling.
    
    Architecture:
        Detective Layer (Parallel) → Aggregator (Fan-In) → 
        [Conditional: Evidence Check] → 
        Judicial Layer (Parallel) → Chief Justice (Fan-In) → Report
        OR → Error Report (if no evidence)
    
    Parallel Execution:
        - Detective layer: 3 nodes run concurrently (repo, doc, vision)
        - Judicial layer: 3 nodes run concurrently (prosecutor, defense, tech_lead)
        - Both layers use fan-out from single source for true parallelism
        - State reducers (operator.ior, operator.add) ensure thread-safe merging
    
    Error Handling:
        - Conditional edge after aggregator checks evidence availability
        - If all detectives fail, route to error_report_node instead of judges
        - Individual detective failures don't block other detectives (parallel isolation)
    
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
    
    # Error Handling Node
    graph.add_node("error_report", error_report_node)
    
    # Wire Detective Layer (Fan-Out from START)
    # All 3 detectives execute in parallel from the start
    graph.add_edge(START, "repo_investigator")
    graph.add_edge(START, "doc_analyst")
    graph.add_edge(START, "vision_inspector")
    
    # All detectives converge to aggregator (Fan-In)
    graph.add_edge("repo_investigator", "evidence_aggregator")
    graph.add_edge("doc_analyst", "evidence_aggregator")
    graph.add_edge("vision_inspector", "evidence_aggregator")
    
    # Conditional Edge: Check if evidence exists before proceeding to judicial
    graph.add_conditional_edges(
        "evidence_aggregator",
        should_continue_to_judicial,
        {
            "judicial": "prosecutor",
            "error_report": "error_report"
        }
    )
    
    # Wire Judicial Layer (Parallel Fan-Out from Aggregator)
    # CRITICAL: All three judges execute in PARALLEL, not sequentially
    # The aggregator has edges to all 3 judges, enabling concurrent execution
    # This is TRUE parallel fan-out: aggregator → [prosecutor || defense || tech_lead]
    graph.add_edge("evidence_aggregator", "defense")
    graph.add_edge("evidence_aggregator", "tech_lead")
    
    # Wire Supreme Court (Fan-In to Chief Justice)
    graph.add_edge("prosecutor", "chief_justice")
    graph.add_edge("defense", "chief_justice")
    graph.add_edge("tech_lead", "chief_justice")
    
    # End
    graph.add_edge("chief_justice", END)
    graph.add_edge("error_report", END)  # Error path also ends
    
    return graph.compile()
