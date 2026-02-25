"""
Test Phase 3: Judicial Layer
"""
import pytest
from src.state import AgentState, Evidence, RubricDimension, JudicialOpinion
from src.nodes.judges import prosecutor_node, defense_node, tech_lead_node
from src.nodes.justice import chief_justice_node


def test_judge_evaluation():
    """Test that judges can evaluate evidence."""
    
    # Create mock state with evidence
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": [
            RubricDimension(
                id="test_criterion",
                name="Test Criterion",
                target_artifact="github_repo",
                forensic_instruction="Test instruction",
                judicial_logic={
                    "prosecutor": "Be critical",
                    "defense": "Be supportive",
                    "tech_lead": "Be pragmatic"
                }
            )
        ],
        "evidences": {
            "test_evidence": [
                Evidence(
                    goal="Test goal",
                    found=True,
                    content="Test content",
                    location="test.py",
                    rationale="Test rationale",
                    confidence=0.8
                )
            ]
        },
        "opinions": [],
        "final_report": "",
        "errors": []
    }
    
    # Test Prosecutor
    result = prosecutor_node(state)
    assert len(result["opinions"]) == 1
    assert result["opinions"][0].judge == "Prosecutor"
    assert 1 <= result["opinions"][0].score <= 5
    
    # Test Defense
    result = defense_node(state)
    assert len(result["opinions"]) == 1
    assert result["opinions"][0].judge == "Defense"
    
    # Test Tech Lead
    result = tech_lead_node(state)
    assert len(result["opinions"]) == 1
    assert result["opinions"][0].judge == "TechLead"


def test_chief_justice_synthesis():
    """Test Chief Justice synthesis logic."""
    
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": [],
        "evidences": {},
        "opinions": [
            JudicialOpinion(
                judge="Prosecutor",
                criterion_id="test_criterion",
                score=2,
                argument="Critical issues found",
                cited_evidence=["test_1"]
            ),
            JudicialOpinion(
                judge="Defense",
                criterion_id="test_criterion",
                score=4,
                argument="Good effort shown",
                cited_evidence=["test_1"]
            ),
            JudicialOpinion(
                judge="TechLead",
                criterion_id="test_criterion",
                score=3,
                argument="Functional but needs work",
                cited_evidence=["test_1"]
            )
        ],
        "final_report": "",
        "errors": []
    }
    
    result = chief_justice_node(state)
    
    assert "final_report" in result
    assert len(result["final_report"]) > 0
    assert "Automaton Auditor Report" in result["final_report"]
    assert "Test Criterion" in result["final_report"]  # Title case in report


if __name__ == "__main__":
    print("Testing Phase 3: Judicial Layer...")
    print("\n⚠️  Note: These tests require LLM API access")
    print("Run with: pytest tests/test_judges.py -v")
