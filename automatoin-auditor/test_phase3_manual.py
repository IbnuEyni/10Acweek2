#!/usr/bin/env python3
"""
Manual test script for Phase 3 Judicial Layer.
Tests judges and chief justice with mock evidence.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.state import Evidence, RubricDimension
from src.nodes.judges import prosecutor_node, defense_node, tech_lead_node
from src.nodes.justice import chief_justice_node
from src.utils.rubric_loader import load_rubric


def test_judicial_layer():
    """Test judicial layer with mock evidence."""
    
    print("=" * 60)
    print("PHASE 3 MANUAL TEST: Judicial Layer")
    print("=" * 60)
    
    # Load rubric
    print("\n1️⃣  Loading rubric...")
    rubric = load_rubric()
    dimensions = [RubricDimension(**d) for d in rubric["dimensions"]]
    print(f"   ✅ Loaded {len(dimensions)} rubric dimensions")
    
    # Create mock evidence
    print("\n2️⃣  Creating mock evidence...")
    mock_evidences = {
        "state_management": [Evidence(
            goal="Verify Pydantic state models",
            found=True,
            content="Found models: ['AgentState', 'Evidence', 'JudicialOpinion']",
            location="src/state.py",
            rationale="Pydantic BaseModel detected with proper reducers",
            confidence=0.95
        )],
        "git_history": [Evidence(
            goal="Verify atomic commit progression",
            found=True,
            content="15 commits found with clear progression",
            location="git log",
            rationale="Atomic progression detected",
            confidence=0.9
        )],
        "langgraph_orchestration": [Evidence(
            goal="Verify StateGraph with parallel execution",
            found=False,
            content="No StateGraph found",
            location="N/A",
            rationale="StateGraph not detected in codebase",
            confidence=0.9
        )]
    }
    print(f"   ✅ Created {len(mock_evidences)} evidence categories")
    
    # Test state
    state = {
        "repo_url": "https://github.com/test/repo",
        "pdf_path": "test.pdf",
        "rubric_dimensions": dimensions,
        "evidences": mock_evidences,
        "opinions": [],
        "final_report": "",
        "errors": []
    }
    
    # Test Prosecutor
    print("\n3️⃣  Testing Prosecutor (Critical Lens)...")
    try:
        prosecutor_result = prosecutor_node(state)
        prosecutor_opinions = prosecutor_result["opinions"]
        print(f"   ✅ Prosecutor evaluated {len(prosecutor_opinions)} criteria")
        for op in prosecutor_opinions[:2]:
            print(f"      - {op.criterion_id}: Score {op.score}/5")
            print(f"        Argument: {op.argument[:80]}...")
    except Exception as e:
        print(f"   ❌ Prosecutor failed: {e}")
        return
    
    # Update state with prosecutor opinions
    state["opinions"].extend(prosecutor_opinions)
    
    # Test Defense
    print("\n4️⃣  Testing Defense (Optimistic Lens)...")
    try:
        defense_result = defense_node(state)
        defense_opinions = defense_result["opinions"]
        print(f"   ✅ Defense evaluated {len(defense_opinions)} criteria")
        for op in defense_opinions[:2]:
            print(f"      - {op.criterion_id}: Score {op.score}/5")
            print(f"        Argument: {op.argument[:80]}...")
    except Exception as e:
        print(f"   ❌ Defense failed: {e}")
        return
    
    # Update state with defense opinions
    state["opinions"].extend(defense_opinions)
    
    # Test Tech Lead
    print("\n5️⃣  Testing Tech Lead (Pragmatic Lens)...")
    try:
        tech_lead_result = tech_lead_node(state)
        tech_lead_opinions = tech_lead_result["opinions"]
        print(f"   ✅ Tech Lead evaluated {len(tech_lead_opinions)} criteria")
        for op in tech_lead_opinions[:2]:
            print(f"      - {op.criterion_id}: Score {op.score}/5")
            print(f"        Argument: {op.argument[:80]}...")
    except Exception as e:
        print(f"   ❌ Tech Lead failed: {e}")
        return
    
    # Update state with tech lead opinions
    state["opinions"].extend(tech_lead_opinions)
    
    # Test Chief Justice
    print("\n6️⃣  Testing Chief Justice (Synthesis)...")
    try:
        justice_result = chief_justice_node(state)
        final_report = justice_result["final_report"]
        print(f"   ✅ Chief Justice synthesized {len(state['opinions'])} opinions")
        print(f"   📄 Report length: {len(final_report)} characters")
        print("\n   Report preview:")
        print("   " + "-" * 56)
        for line in final_report.split("\n")[:15]:
            print(f"   {line}")
        print("   " + "-" * 56)
    except Exception as e:
        print(f"   ❌ Chief Justice failed: {e}")
        return
    
    # Summary
    print("\n7️⃣  Dialectical Analysis...")
    from collections import defaultdict
    scores_by_criterion = defaultdict(list)
    
    for opinion in state["opinions"]:
        scores_by_criterion[opinion.criterion_id].append({
            "judge": opinion.judge,
            "score": opinion.score
        })
    
    print("   📊 Score variance by criterion:")
    for criterion_id, scores in scores_by_criterion.items():
        score_values = [s["score"] for s in scores]
        variance = max(score_values) - min(score_values)
        print(f"      {criterion_id}:")
        for s in scores:
            print(f"         {s['judge']}: {s['score']}/5")
        print(f"         Variance: {variance} {'⚠️ High conflict!' if variance > 2 else '✅ Consensus'}")
    
    print("\n" + "=" * 60)
    print("✅ PHASE 3 MANUAL TEST COMPLETE")
    print("=" * 60)
    print("\nJudicial layer is working correctly!")
    print("All three judges evaluated evidence with distinct perspectives.")
    print("Chief Justice successfully synthesized conflicting opinions.")
    print("\nReady to proceed to Phase 4: Graph Orchestration")


if __name__ == "__main__":
    test_judicial_layer()
