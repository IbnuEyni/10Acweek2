"""
AST tools for Python code structure analysis.
Detects LangGraph patterns, Pydantic models, and state reducers.
"""
import ast
from pathlib import Path
from typing import Dict, List, Optional


def detect_langgraph_patterns(file_path: Path) -> Dict:
    """
    Analyze Python file for LangGraph patterns using AST.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Dict with detected patterns
    """
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
    except (SyntaxError, FileNotFoundError):
        return {"error": "Failed to parse file"}
    
    findings = {
        "has_state_graph": False,
        "has_add_node": False,
        "has_add_edge": False,
        "parallel_branches": 0,
        "node_names": []
    }
    
    for node in ast.walk(tree):
        # Detect StateGraph instantiation
        if isinstance(node, ast.Call):
            if hasattr(node.func, 'id') and node.func.id == "StateGraph":
                findings["has_state_graph"] = True
            
            # Detect add_node calls
            if hasattr(node.func, 'attr'):
                if node.func.attr == "add_node":
                    findings["has_add_node"] = True
                    if node.args and isinstance(node.args[0], ast.Constant):
                        findings["node_names"].append(node.args[0].value)
                
                # Detect add_edge calls
                elif node.func.attr == "add_edge":
                    findings["has_add_edge"] = True
    
    # Estimate parallelism (multiple edges from same source)
    findings["parallel_branches"] = len(set(findings["node_names"]))
    
    return findings


def find_pydantic_models(file_path: Path) -> List[str]:
    """
    Find Pydantic BaseModel classes in file.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        List of class names
    """
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
    except (SyntaxError, FileNotFoundError):
        return []
    
    models = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseModel":
                    models.append(node.name)
    
    return models


def detect_state_reducers(file_path: Path) -> Dict:
    """
    Detect use of operator.add or operator.ior for state reducers.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Dict with reducer usage
    """
    try:
        with open(file_path) as f:
            content = f.read()
            tree = ast.parse(content)
    except (SyntaxError, FileNotFoundError):
        return {"has_reducers": False}
    
    findings = {
        "has_reducers": False,
        "uses_operator_add": "operator.add" in content,
        "uses_operator_ior": "operator.ior" in content,
        "has_annotated": False
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "Annotated":
            findings["has_annotated"] = True
    
    findings["has_reducers"] = (
        findings["uses_operator_add"] or 
        findings["uses_operator_ior"]
    )
    
    return findings


def scan_directory_for_patterns(directory: Path, pattern: str) -> List[Path]:
    """
    Recursively scan directory for Python files matching pattern.
    
    Args:
        directory: Root directory to scan
        pattern: Pattern to search for (e.g., "StateGraph", "BaseModel")
        
    Returns:
        List of file paths containing pattern
    """
    matching_files = []
    
    for py_file in directory.rglob("*.py"):
        try:
            with open(py_file) as f:
                if pattern in f.read():
                    matching_files.append(py_file)
        except (IOError, UnicodeDecodeError):
            continue
    
    return matching_files
