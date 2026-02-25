"""
Unit tests for Detective Layer tools.
"""
import pytest
from pathlib import Path
from src.tools.ast_tools import (
    detect_langgraph_patterns,
    find_pydantic_models,
    detect_state_reducers
)
from src.tools.pdf_tools import (
    extract_concepts,
    extract_architectural_keywords
)


def test_detect_langgraph_patterns():
    """Test AST detection of LangGraph patterns."""
    # Create a test file
    test_code = '''
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("detective", detective_node)
graph.add_edge("detective", "judge")
'''
    
    test_file = Path("/tmp/test_graph.py")
    test_file.write_text(test_code)
    
    result = detect_langgraph_patterns(test_file)
    
    assert result["has_state_graph"] == True
    assert result["has_add_node"] == True
    assert result["has_add_edge"] == True
    assert "detective" in result["node_names"]
    
    test_file.unlink()


def test_find_pydantic_models():
    """Test detection of Pydantic models."""
    test_code = '''
from pydantic import BaseModel

class Evidence(BaseModel):
    goal: str
    found: bool

class JudicialOpinion(BaseModel):
    judge: str
    score: int
'''
    
    test_file = Path("/tmp/test_models.py")
    test_file.write_text(test_code)
    
    models = find_pydantic_models(test_file)
    
    assert "Evidence" in models
    assert "JudicialOpinion" in models
    assert len(models) == 2
    
    test_file.unlink()


def test_detect_state_reducers():
    """Test detection of state reducers."""
    test_code = '''
import operator
from typing import Annotated

class AgentState(TypedDict):
    evidences: Annotated[Dict, operator.ior]
    opinions: Annotated[List, operator.add]
'''
    
    test_file = Path("/tmp/test_reducers.py")
    test_file.write_text(test_code)
    
    result = detect_state_reducers(test_file)
    
    assert result["has_reducers"] == True
    assert result["uses_operator_add"] == True
    assert result["uses_operator_ior"] == True
    assert result["has_annotated"] == True
    
    test_file.unlink()


def test_extract_concepts():
    """Test concept extraction from text."""
    text = """
    This system implements Dialectical Synthesis through three judges.
    The architecture uses Fan-Out and Fan-In patterns for parallel execution.
    Metacognition is achieved through the Chief Justice node.
    """
    
    concepts = ["Dialectical Synthesis", "Fan-Out", "Metacognition", "Missing Concept"]
    result = extract_concepts(text, concepts)
    
    assert len(result["Dialectical Synthesis"]) > 0
    assert len(result["Fan-Out"]) > 0
    assert len(result["Metacognition"]) > 0
    assert len(result["Missing Concept"]) == 0


def test_extract_architectural_keywords():
    """Test keyword counting in documents."""
    text = """
    The LangGraph StateGraph uses Pydantic models for state management.
    Multi-Agent systems require Parallel Execution with proper synchronization.
    LangGraph provides the foundation for this architecture.
    """
    
    counts = extract_architectural_keywords(text)
    
    assert counts["LangGraph"] == 2
    assert counts["Pydantic"] == 1
    assert counts["Multi-Agent"] == 1
    assert counts["Parallel Execution"] == 1
    assert counts["StateGraph"] == 1
