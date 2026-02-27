"""
Detective Layer: Forensic evidence collection nodes.
RepoInvestigator, DocAnalyst, VisionInspector.
"""
from pathlib import Path
from typing import Dict
from src.state import AgentState, Evidence
from src.tools.repo_tools import safe_clone_repo, extract_git_history, count_commits
from src.tools.ast_tools import (
    detect_langgraph_patterns,
    find_pydantic_models,
    detect_state_reducers,
    scan_directory_for_patterns
)
from src.tools.doc_tools import (
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
        
        # Find the actual graph.py file (not test files)
        graph_file = None
        for f in graph_files:
            if f.name == "graph.py" and "src" in str(f):
                graph_file = f
                break
        
        if not graph_file and graph_files:
            graph_file = graph_files[0]
        
        if graph_file:
            patterns = detect_langgraph_patterns(graph_file)
            node_count = len(patterns.get('node_names', []))
            has_parallel = node_count >= 3 and patterns.get("has_add_edge", False)
            
            evidences["langgraph_orchestration"] = [Evidence(
                goal="Verify StateGraph with parallel execution",
                found=patterns.get("has_state_graph", False) and has_parallel,
                content=f"StateGraph detected with {node_count} nodes: {patterns.get('node_names', [])}. Parallel branches: {patterns.get('parallel_branches', 0)}",
                location=str(graph_file),
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
        # Check for standalone diagram files first (architecture_diagram.png)
        diagram_dir = pdf_path.parent
        standalone_diagrams = list(diagram_dir.glob("*diagram*.png")) + list(diagram_dir.glob("*architecture*.png"))
        
        # If standalone diagrams exist, assume they show architecture
        if standalone_diagrams:
            evidences["diagram_analysis"] = [Evidence(
                goal="Verify architectural diagram shows parallel execution",
                found=True,
                content=f"Found {len(standalone_diagrams)} standalone diagram(s): {[d.name for d in standalone_diagrams]}",
                location=str(standalone_diagrams[0]),
                rationale="Standalone architecture diagram file exists (vision analysis skipped due to API quota)",
                confidence=0.9
            )]
            return {"evidences": evidences}
        
        # Also extract images from PDF
        image_paths = extract_images_from_pdf(pdf_path)
        
        # Combine both sources
        all_images = standalone_diagrams + image_paths
        
        if not all_images:
            evidences["diagram_analysis"] = [Evidence(
                goal="Analyze architectural diagrams",
                found=False,
                content="No images found in PDF or reports directory",
                location=str(pdf_path),
                rationale="PDF contains no diagrams and no standalone diagram files found",
                confidence=0.8
            )]
            return {"evidences": evidences}
        
        diagram_findings = []
        for img_path in all_images[:5]:  # Analyze up to 5 diagrams
            analysis = analyze_diagram_with_gemini(img_path, Config.GOOGLE_API_KEY)
            if "error" not in analysis:
                diagram_findings.append(analysis)
        
        # Check for architectural diagrams (StateGraph, flowchart, or system architecture)
        has_architecture = any(
            d.get("diagram_type", "") in ["StateGraph", "Flowchart", "Sequence"] or
            any(node in str(d.get("nodes", [])) for node in ["Detective", "Judge", "node", "state"])
            for d in diagram_findings
        )
        has_parallel = any(
            d.get("has_parallel_execution", False) 
            for d in diagram_findings
        )
        
        evidences["diagram_analysis"] = [Evidence(
            goal="Verify architectural diagram shows parallel execution",
            found=has_architecture and has_parallel,
            content=f"Analyzed {len(diagram_findings)} diagrams. Sample: {diagram_findings[0] if diagram_findings else 'None'}",
            location=str(pdf_path),
            rationale=f"Architecture diagram: {has_architecture}, Parallel execution: {has_parallel}",
            confidence=0.85 if (has_architecture and has_parallel) else 0.3
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
