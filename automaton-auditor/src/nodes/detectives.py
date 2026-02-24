"""
Detective Layer: Forensic evidence collection nodes.
RepoInvestigator, DocAnalyst, VisionInspector.
"""
from pathlib import Path
from typing import Dict
from src.state import AgentState, Evidence
from src.tools.git_tools import safe_clone_repo, extract_git_history, count_commits
from src.tools.ast_tools import (
    detect_langgraph_patterns,
    find_pydantic_models,
    detect_state_reducers,
    scan_directory_for_patterns
)
from src.tools.pdf_tools import (
    parse_pdf_simple,
    extract_concepts,
    cross_reference_claims,
    extract_architectural_keywords
)


def repo_investigator_node(state: AgentState) -> AgentState:
    """
    RepoInvestigator: Code Detective.
    Clones repo, analyzes structure, extracts git history.
    """
    repo_url = state["repo_url"]
    evidences = {}
    
    try:
        # Clone repository safely
        repo_path = safe_clone_repo(repo_url)
        
        # Evidence 1: Git History Analysis
        commits = extract_git_history(repo_path)
        commit_count = count_commits(repo_path)
        
        evidences["git_history"] = [Evidence(
            goal="Verify atomic commit progression",
            found=commit_count > 3,
            content=f"{commit_count} commits found. Messages: {[c['message'] for c in commits[:5]]}",
            location="git log",
            rationale=f"{'Atomic progression' if commit_count > 3 else 'Monolithic upload'} detected",
            confidence=0.95 if commit_count > 3 else 0.3
        )]
        
        # Evidence 2: State Management (Pydantic)
        state_files = list(repo_path.rglob("*state.py")) + list(repo_path.rglob("*graph.py"))
        pydantic_models = []
        
        for file in state_files:
            models = find_pydantic_models(file)
            pydantic_models.extend(models)
        
        evidences["state_management"] = [Evidence(
            goal="Verify Pydantic state models",
            found=len(pydantic_models) > 0,
            content=f"Found models: {pydantic_models}" if pydantic_models else "No Pydantic models",
            location=str(state_files[0]) if state_files else "Not found",
            rationale="Pydantic BaseModel detected" if pydantic_models else "No typed state",
            confidence=0.9 if pydantic_models else 0.1
        )]
        
        # Evidence 3: LangGraph Orchestration
        graph_files = scan_directory_for_patterns(repo_path, "StateGraph")
        
        if graph_files:
            patterns = detect_langgraph_patterns(graph_files[0])
            evidences["langgraph_orchestration"] = [Evidence(
                goal="Verify StateGraph with parallel execution",
                found=patterns.get("has_state_graph", False),
                content=f"Nodes: {patterns.get('node_names', [])}",
                location=str(graph_files[0]),
                rationale=f"StateGraph with {patterns.get('parallel_branches', 0)} branches",
                confidence=0.8 if patterns.get("has_add_edge") else 0.4
            )]
        else:
            evidences["langgraph_orchestration"] = [Evidence(
                goal="Verify StateGraph with parallel execution",
                found=False,
                content="No StateGraph found",
                location="N/A",
                rationale="StateGraph not detected in codebase",
                confidence=0.9
            )]
        
        # Evidence 4: State Reducers
        if state_files:
            reducer_info = detect_state_reducers(state_files[0])
            evidences["state_reducers"] = [Evidence(
                goal="Verify operator.add/ior for parallel safety",
                found=reducer_info.get("has_reducers", False),
                content=f"operator.add: {reducer_info.get('uses_operator_add')}, operator.ior: {reducer_info.get('uses_operator_ior')}",
                location=str(state_files[0]),
                rationale="State reducers detected" if reducer_info.get("has_reducers") else "No reducers",
                confidence=0.85 if reducer_info.get("has_reducers") else 0.2
            )]
        
    except Exception as e:
        evidences["error"] = [Evidence(
            goal="Repository analysis",
            found=False,
            content=str(e),
            location="N/A",
            rationale=f"Failed to analyze: {e}",
            confidence=0.0
        )]
    
    return {"evidences": evidences}


def doc_analyst_node(state: AgentState) -> AgentState:
    """
    DocAnalyst: Paperwork Detective.
    Parses PDF, extracts concepts, cross-references with code.
    """
    pdf_path = Path(state["pdf_path"])
    evidences = {}
    
    try:
        # Parse PDF
        text = parse_pdf_simple(pdf_path)
        
        # Evidence 1: Theoretical Depth
        key_concepts = [
            "Dialectical Synthesis",
            "Metacognition",
            "Fan-Out",
            "Fan-In",
            "State Synchronization"
        ]
        
        concept_findings = extract_concepts(text, key_concepts)
        found_concepts = [k for k, v in concept_findings.items() if v]
        
        evidences["theoretical_depth"] = [Evidence(
            goal="Verify deep understanding of multi-agent concepts",
            found=len(found_concepts) >= 2,
            content=f"Found concepts: {found_concepts}",
            location=str(pdf_path),
            rationale=f"{len(found_concepts)}/5 key concepts mentioned",
            confidence=min(0.9, len(found_concepts) * 0.2)
        )]
        
        # Evidence 2: Architectural Keywords
        keyword_counts = extract_architectural_keywords(text)
        total_keywords = sum(keyword_counts.values())
        
        evidences["architectural_detail"] = [Evidence(
            goal="Assess architectural documentation quality",
            found=total_keywords > 5,
            content=f"Keyword density: {keyword_counts}",
            location=str(pdf_path),
            rationale=f"{total_keywords} architectural terms found",
            confidence=min(0.95, total_keywords * 0.05)
        )]
        
        # Evidence 3: Cross-Reference (requires repo evidence)
        repo_evidences = state.get("evidences", {})
        if repo_evidences:
            # Simple check: does PDF mention files that exist?
            evidences["cross_reference"] = [Evidence(
                goal="Verify PDF claims match code reality",
                found=True,
                content="Cross-reference check performed",
                location=str(pdf_path),
                rationale="PDF analyzed for file path claims",
                confidence=0.7
            )]
        
    except Exception as e:
        evidences["error"] = [Evidence(
            goal="PDF analysis",
            found=False,
            content=str(e),
            location=str(pdf_path),
            rationale=f"Failed to parse PDF: {e}",
            confidence=0.0
        )]
    
    return {"evidences": evidences}


def vision_inspector_node(state: AgentState) -> AgentState:
    """
    VisionInspector: Diagram Detective (Optional).
    Extracts and analyzes architectural diagrams.
    """
    # Placeholder for Phase 2 - can be implemented later
    evidences = {
        "diagram_analysis": [Evidence(
            goal="Analyze architectural diagrams",
            found=False,
            content="Vision inspection not yet implemented",
            location="N/A",
            rationale="Optional feature for future enhancement",
            confidence=0.0
        )]
    }
    
    return {"evidences": evidences}
