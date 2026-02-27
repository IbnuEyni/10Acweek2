"""
Unit tests for state reducers.
Verifies operator.add and operator.ior behave correctly for parallel execution.
"""
import operator
from typing import Annotated, Dict, List
from typing_extensions import TypedDict
from src.state import Evidence, JudicialOpinion, AgentState


def test_operator_ior_merges_dicts():
    """Verify operator.ior merges dicts without overwriting."""
    dict1 = {"repo": [Evidence(goal="test1", found=True, location="file1", rationale="reason for confidence", confidence=0.9)]}
    dict2 = {"doc": [Evidence(goal="test2", found=True, location="file2", rationale="another reason", confidence=0.8)]}
    
    result = operator.ior(dict1.copy(), dict2)
    
    assert "repo" in result
    assert "doc" in result
    assert len(result) == 2


def test_operator_ior_is_commutative():
    """Verify operator.ior order doesn't matter (commutative)."""
    dict1 = {"a": [1]}
    dict2 = {"b": [2]}
    
    result1 = operator.ior(dict1.copy(), dict2)
    result2 = operator.ior(dict2.copy(), dict1)
    
    assert result1.keys() == result2.keys()


def test_operator_add_concatenates_lists():
    """Verify operator.add concatenates lists preserving all elements."""
    list1 = [JudicialOpinion(judge="Prosecutor", criterion_id="test", score=1, argument="This is a detailed argument", cited_evidence=["e1"])]
    list2 = [JudicialOpinion(judge="Defense", criterion_id="test", score=5, argument="Another detailed argument", cited_evidence=["e2"])]
    
    result = operator.add(list1, list2)
    
    assert len(result) == 2
    assert result[0].judge == "Prosecutor"
    assert result[1].judge == "Defense"


def test_operator_add_preserves_order():
    """Verify operator.add preserves list order."""
    list1 = ["error1", "error2"]
    list2 = ["error3"]
    
    result = operator.add(list1, list2)
    
    assert result == ["error1", "error2", "error3"]


def test_parallel_evidence_collection_simulation():
    """Simulate 3 detectives writing evidence concurrently."""
    # Initial state
    state_evidences = {}
    
    # Detective 1: RepoInvestigator
    repo_evidence = {"repo_investigator": [
        Evidence(goal="Find StateGraph", found=True, location="src/graph.py", rationale="AST parsing found StateGraph class", confidence=0.95)
    ]}
    state_evidences = operator.ior(state_evidences, repo_evidence)
    
    # Detective 2: DocAnalyst
    doc_evidence = {"doc_analyst": [
        Evidence(goal="Find concepts", found=True, location="report.pdf", rationale="Keywords found in document", confidence=0.85)
    ]}
    state_evidences = operator.ior(state_evidences, doc_evidence)
    
    # Detective 3: VisionInspector
    vision_evidence = {"vision_inspector": [
        Evidence(goal="Find diagrams", found=True, location="diagram.png", rationale="Gemini vision analyzed diagram", confidence=0.75)
    ]}
    state_evidences = operator.ior(state_evidences, vision_evidence)
    
    # Verify all evidence preserved
    assert len(state_evidences) == 3
    assert "repo_investigator" in state_evidences
    assert "doc_analyst" in state_evidences
    assert "vision_inspector" in state_evidences


def test_parallel_judicial_opinions_simulation():
    """Simulate 3 judges writing opinions concurrently."""
    # Initial state
    state_opinions = []
    
    # Judge 1: Prosecutor
    prosecutor_opinion = [JudicialOpinion(
        judge="Prosecutor", criterion_id="forensic_accuracy", score=2,
        argument="Security flaw detected", cited_evidence=["repo_investigator_0"]
    )]
    state_opinions = operator.add(state_opinions, prosecutor_opinion)
    
    # Judge 2: Defense
    defense_opinion = [JudicialOpinion(
        judge="Defense", criterion_id="forensic_accuracy", score=5,
        argument="Excellent effort with deep understanding", cited_evidence=["repo_investigator_0"]
    )]
    state_opinions = operator.add(state_opinions, defense_opinion)
    
    # Judge 3: TechLead
    tech_lead_opinion = [JudicialOpinion(
        judge="TechLead", criterion_id="forensic_accuracy", score=3,
        argument="Functional implementation but has some gaps", cited_evidence=["repo_investigator_0"]
    )]
    state_opinions = operator.add(state_opinions, tech_lead_opinion)
    
    # Verify all opinions preserved
    assert len(state_opinions) == 3
    assert state_opinions[0].judge == "Prosecutor"
    assert state_opinions[1].judge == "Defense"
    assert state_opinions[2].judge == "TechLead"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
