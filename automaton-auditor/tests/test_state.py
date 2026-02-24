"""
Unit tests for state models.
"""
import pytest
from src.state import Evidence, JudicialOpinion, RubricDimension, AgentState


def test_evidence_model():
    """Test Evidence Pydantic model validation."""
    evidence = Evidence(
        goal="Verify StateGraph exists",
        found=True,
        content="class StateGraph...",
        location="src/graph.py:10",
        rationale="AST parsing confirmed StateGraph class",
        confidence=0.95
    )
    assert evidence.found is True
    assert evidence.confidence == 0.95


def test_judicial_opinion_model():
    """Test JudicialOpinion score constraints."""
    opinion = JudicialOpinion(
        judge="Prosecutor",
        criterion_id="forensic_accuracy_code",
        score=3,
        argument="Code exists but lacks error handling",
        cited_evidence=["src/tools/git_tools.py:25"]
    )
    assert opinion.score == 3
    
    # Test score validation
    with pytest.raises(ValueError):
        JudicialOpinion(
            judge="Prosecutor",
            criterion_id="test",
            score=6,  # Invalid: must be 1-5
            argument="test",
            cited_evidence=[]
        )


def test_rubric_dimension_model():
    """Test RubricDimension parsing."""
    dim = RubricDimension(
        id="test_dim",
        name="Test Dimension",
        target_artifact="github_repo",
        forensic_instruction="Test instruction",
        judicial_logic={"prosecutor": "Test logic"}
    )
    assert dim.target_artifact == "github_repo"


def test_agent_state_structure():
    """Test AgentState TypedDict structure."""
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "/path/to/report.pdf",
        "rubric_dimensions": [],
        "evidences": {},
        "opinions": [],
        "final_report": "",
        "errors": []
    }
    assert state["repo_url"] == "https://github.com/test/repo"
