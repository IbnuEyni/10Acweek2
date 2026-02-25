"""
Unit tests for rubric loader.
"""
import pytest
from src.utils.rubric_loader import (
    load_rubric,
    get_rubric_dimensions,
    get_synthesis_rules,
    filter_dimensions_by_artifact
)


def test_load_rubric():
    """Test rubric JSON loading."""
    rubric = load_rubric()
    assert "rubric_metadata" in rubric
    assert "dimensions" in rubric
    assert rubric["rubric_metadata"]["version"] == "2.0.0"


def test_get_rubric_dimensions():
    """Test parsing dimensions into Pydantic models."""
    dimensions = get_rubric_dimensions()
    assert len(dimensions) == 4
    assert all(hasattr(dim, "id") for dim in dimensions)
    assert all(hasattr(dim, "judicial_logic") for dim in dimensions)


def test_get_synthesis_rules():
    """Test extraction of synthesis rules."""
    rules = get_synthesis_rules()
    assert "security_override" in rules
    assert "fact_supremacy" in rules
    assert "dissent_requirement" in rules


def test_filter_dimensions_by_artifact():
    """Test filtering dimensions by target artifact."""
    repo_dims = filter_dimensions_by_artifact("github_repo")
    pdf_dims = filter_dimensions_by_artifact("pdf_report")
    
    assert len(repo_dims) == 3  # forensic_accuracy_code, judicial_nuance, langgraph_architecture
    assert len(pdf_dims) == 1   # forensic_accuracy_docs
    
    assert all(dim.target_artifact == "github_repo" for dim in repo_dims)
    assert all(dim.target_artifact == "pdf_report" for dim in pdf_dims)
