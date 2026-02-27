"""
Integration tests for fan-in synchronization.
Verifies evidence aggregation from parallel detectives works correctly.
"""
import pytest
from src.state import AgentState, Evidence
from src.nodes.aggregator import evidence_aggregator_node


def test_aggregator_merges_all_detective_evidence():
    """Verify aggregator preserves evidence from all 3 detectives."""
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": [],
        "evidences": {
            "repo_investigator": [
                Evidence(
                    goal="Find StateGraph",
                    found=True,
                    location="src/graph.py",
                    rationale="AST parsing detected StateGraph instantiation",
                    confidence=0.95
                )
            ],
            "doc_analyst": [
                Evidence(
                    goal="Find concepts",
                    found=True,
                    location="report.pdf",
                    rationale="Found 5 key multi-agent concepts",
                    confidence=0.85
                )
            ],
            "vision_inspector": [
                Evidence(
                    goal="Find diagrams",
                    found=True,
                    location="diagram.png",
                    rationale="Gemini detected parallel execution pattern",
                    confidence=0.75
                )
            ]
        },
        "opinions": [],
        "errors": [],
        "final_report": ""
    }
    
    result = evidence_aggregator_node(state)
    
    # Verify all evidence preserved
    assert len(result["evidences"]) == 3
    assert "repo_investigator" in result["evidences"]
    assert "doc_analyst" in result["evidences"]
    assert "vision_inspector" in result["evidences"]
    
    # Verify evidence content intact
    assert result["evidences"]["repo_investigator"][0].goal == "Find StateGraph"
    assert result["evidences"]["doc_analyst"][0].goal == "Find concepts"
    assert result["evidences"]["vision_inspector"][0].goal == "Find diagrams"


def test_aggregator_handles_partial_detective_failure():
    """Verify aggregator works when some detectives fail."""
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": [],
        "evidences": {
            "repo_investigator": [
                Evidence(
                    goal="Find StateGraph",
                    found=True,
                    location="src/graph.py",
                    rationale="AST parsing successful",
                    confidence=0.95
                )
            ],
            "doc_analyst": [
                Evidence(
                    goal="Find concepts",
                    found=False,
                    location="N/A",
                    rationale="PDF parsing failed",
                    confidence=0.0
                )
            ]
            # vision_inspector missing (failed completely)
        },
        "opinions": [],
        "errors": ["VisionInspector: Google API key not configured"],
        "final_report": ""
    }
    
    result = evidence_aggregator_node(state)
    
    # Verify partial evidence preserved
    assert len(result["evidences"]) == 2
    assert "repo_investigator" in result["evidences"]
    assert "doc_analyst" in result["evidences"]
    assert "vision_inspector" not in result["evidences"]


def test_aggregator_handles_empty_evidence():
    """Verify aggregator handles case when all detectives fail."""
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": [],
        "evidences": {},  # All detectives failed
        "opinions": [],
        "errors": [
            "RepoInvestigator: Clone failed",
            "DocAnalyst: PDF not found",
            "VisionInspector: API key missing"
        ],
        "final_report": ""
    }
    
    result = evidence_aggregator_node(state)
    
    # Verify empty evidence dict preserved
    assert len(result["evidences"]) == 0
    
    # Verify aggregator adds error message
    assert "errors" in result
    assert "No evidence collected" in result["errors"][0]


def test_aggregator_preserves_evidence_order():
    """Verify aggregator maintains evidence list order within each detective."""
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": [],
        "evidences": {
            "repo_investigator": [
                Evidence(
                    goal="Evidence 1",
                    found=True,
                    location="file1.py",
                    rationale="First evidence collected",
                    confidence=0.9
                ),
                Evidence(
                    goal="Evidence 2",
                    found=True,
                    location="file2.py",
                    rationale="Second evidence collected",
                    confidence=0.8
                ),
                Evidence(
                    goal="Evidence 3",
                    found=True,
                    location="file3.py",
                    rationale="Third evidence collected",
                    confidence=0.7
                )
            ]
        },
        "opinions": [],
        "errors": [],
        "final_report": ""
    }
    
    result = evidence_aggregator_node(state)
    
    # Verify order preserved
    evidence_list = result["evidences"]["repo_investigator"]
    assert len(evidence_list) == 3
    assert evidence_list[0].goal == "Evidence 1"
    assert evidence_list[1].goal == "Evidence 2"
    assert evidence_list[2].goal == "Evidence 3"


def test_aggregator_no_data_loss():
    """Verify no evidence is lost during aggregation."""
    state: AgentState = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": [],
        "evidences": {
            "repo_investigator": [
                Evidence(goal=f"Repo evidence {i}", found=True, location=f"file{i}.py",
                         rationale=f"Evidence {i}", confidence=0.9)
                for i in range(5)
            ],
            "doc_analyst": [
                Evidence(goal=f"Doc evidence {i}", found=True, location=f"page{i}",
                         rationale=f"Evidence {i}", confidence=0.8)
                for i in range(3)
            ],
            "vision_inspector": [
                Evidence(goal=f"Vision evidence {i}", found=True, location=f"diagram{i}.png",
                         rationale=f"Evidence {i}", confidence=0.7)
                for i in range(2)
            ]
        },
        "opinions": [],
        "errors": [],
        "final_report": ""
    }
    
    result = evidence_aggregator_node(state)
    
    # Count total evidence
    total_evidence = sum(len(ev_list) for ev_list in result["evidences"].values())
    assert total_evidence == 10  # 5 + 3 + 2
    
    # Verify each detective's evidence count
    assert len(result["evidences"]["repo_investigator"]) == 5
    assert len(result["evidences"]["doc_analyst"]) == 3
    assert len(result["evidences"]["vision_inspector"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
