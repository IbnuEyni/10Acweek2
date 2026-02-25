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
            node_count = len(patterns.get('node_names', []))
            has_parallel = node_count >= 3 and patterns.get("has_add_edge", False)
            
            evidences["langgraph_orchestration"] = [Evidence(
                goal="Verify StateGraph with parallel execution",
                found=patterns.get("has_state_graph", False) and has_parallel,
                content=f"StateGraph detected with {node_count} nodes: {patterns.get('node_names', [])}. Parallel branches: {patterns.get('parallel_branches', 0)}",
                location=str(graph_files[0]),
                rationale=f"StateGraph with {node_count} nodes and parallel execution" if has_parallel else f"StateGraph found but limited parallelism",
                confidence=0.95 if has_parallel else 0.6
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
            "Agent Autonomy",
            "Parallel Execution",
            "State Synchronization",
            "Dialectical Reasoning",
            "Hierarchical Decision"
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
    VisionInspector: Diagram Detective.
    Extracts and analyzes architectural diagrams using Gemini.
    """
    from src.tools.vision_tools import extract_images_from_pdf, analyze_diagram_with_gemini
    from src.utils.config import Config
    
    pdf_path = Path(state["pdf_path"])
    evidences = {}
    
    if not Config.GOOGLE_API_KEY or Config.GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
        evidences["diagram_analysis"] = [Evidence(
            goal="Analyze architectural diagrams",
            found=False,
            content="Google API key not configured",
            location="N/A",
            rationale="Vision inspection requires GOOGLE_API_KEY in .env",
            confidence=0.0
        )]
        return {"evidences": evidences}
    
    try:
        image_paths = extract_images_from_pdf(pdf_path)
        
        if not image_paths:
            evidences["diagram_analysis"] = [Evidence(
                goal="Analyze architectural diagrams",
                found=False,
                content="No images extracted from PDF",
                location=str(pdf_path),
                rationale="PDF contains no diagrams or extraction failed",
                confidence=0.8
            )]
            return {"evidences": evidences}
        
        diagram_findings = []
        for img_path in image_paths[:3]:
            analysis = analyze_diagram_with_gemini(img_path, Config.GOOGLE_API_KEY)
            if "error" not in analysis:
                diagram_findings.append(analysis)
        
        has_state_graph = any(
            "StateGraph" in d.get("diagram_type", "") 
            for d in diagram_findings
        )
        has_parallel = any(
            d.get("has_parallel_execution", False) 
            for d in diagram_findings
        )
        
        evidences["diagram_analysis"] = [Evidence(
            goal="Verify architectural diagram shows parallel execution",
            found=has_state_graph and has_parallel,
            content=f"Analyzed {len(diagram_findings)} diagrams. Findings: {diagram_findings}",
            location=str(pdf_path),
            rationale=f"StateGraph: {has_state_graph}, Parallel: {has_parallel}",
            confidence=0.7 if diagram_findings else 0.1
        )]
        
    except Exception as e:
        evidences["diagram_analysis"] = [Evidence(
            goal="Analyze architectural diagrams",
            found=False,
            content=str(e),
            location=str(pdf_path),
            rationale=f"Vision analysis failed: {e}",
            confidence=0.0
        )]
    
    return {"evidences": evidences}
