"""
AST tools for Python code structure analysis.
Detects LangGraph patterns, Pydantic models, state reducers, and structural properties.
"""
import ast
from pathlib import Path
from typing import Dict, List, Optional, Set
from src.utils.sandbox import validate_file_access, SandboxViolation, ResourceLimits


def detect_langgraph_patterns(file_path: Path) -> Dict:
    """
    Analyze Python file for LangGraph patterns using AST with sandboxing.
    Enhanced with deeper structural checks.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Dict with detected patterns and structural properties
    """
    try:
        # Validate file access with size limits
        validate_file_access(file_path, max_size_mb=ResourceLimits.MAX_FILE_SIZE_MB)
        
        with open(file_path) as f:
            content = f.read()
            tree = ast.parse(content)
    except SandboxViolation as e:
        return {"error": f"Sandbox violation: {e}"}
    except (SyntaxError, FileNotFoundError) as e:
        return {"error": f"Failed to parse file: {e}"}
    
    findings = {
        "has_state_graph": False,
        "has_add_node": False,
        "has_add_edge": False,
        "has_conditional_edges": False,
        "has_compile": False,
        "parallel_branches": 0,
        "node_names": [],
        "edge_count": 0,
        "imports_langgraph": "langgraph" in content
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
                    findings["edge_count"] += 1
                
                # Detect add_conditional_edges
                elif node.func.attr == "add_conditional_edges":
                    findings["has_conditional_edges"] = True
                
                # Detect compile() call
                elif node.func.attr == "compile":
                    findings["has_compile"] = True
    
    # Estimate parallelism (unique nodes suggest parallel execution)
    findings["parallel_branches"] = len(set(findings["node_names"]))
    
    return findings


def analyze_code_structure(file_path: Path) -> Dict:
    """
    Deep structural analysis with sandboxing: complexity, imports, function signatures.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Dict with structural metrics
    """
    try:
        validate_file_access(file_path, max_size_mb=ResourceLimits.MAX_FILE_SIZE_MB)
        with open(file_path) as f:
            tree = ast.parse(f.read())
    except (SandboxViolation, SyntaxError, FileNotFoundError):
        return {"error": "Failed to parse"}
    
    metrics = {
        "function_count": 0,
        "class_count": 0,
        "import_count": 0,
        "max_nesting_depth": 0,
        "has_type_hints": False,
        "has_docstrings": False
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            metrics["function_count"] += 1
            if node.returns or any(arg.annotation for arg in node.args.args):
                metrics["has_type_hints"] = True
            if ast.get_docstring(node):
                metrics["has_docstrings"] = True
        
        elif isinstance(node, ast.ClassDef):
            metrics["class_count"] += 1
        
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            metrics["import_count"] += 1
    
    return metrics


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
