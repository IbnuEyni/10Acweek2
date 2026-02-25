#!/usr/bin/env python3
"""
End-to-end integration test for complete audit pipeline.
Tests graph orchestration with all layers.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.graph import build_audit_graph
from src.utils.rubric_loader import load_rubric
from src.state import AgentState, RubricDimension


def test_full_audit_pipeline():
    """Test complete audit from initialization to report generation."""
    
    print("=" * 60)
    print("END-TO-END INTEGRATION TEST")
    print("=" * 60)
    
    # Load rubric
    print("\n1️⃣  Loading rubric...")
    rubric = load_rubric()
    dimensions = [RubricDimension(**d) for d in rubric["dimensions"]]
    print(f"   ✅ Loaded {len(dimensions)} dimensions")
    
    # Initialize state
    print("\n2️⃣  Initializing state...")
    initial_state: AgentState = {
        "repo_url": "https://github.com/IbnuEyni/Dr_Abdi.git",
        "pdf_path": "test.pdf",  # Will fail gracefully if not exists
        "rubric_dimensions": dimensions,
        "evidences": {},
        "opinions": [],
        "final_report": "",
        "errors": []
    }
    print("   ✅ State initialized")
    
    # Build graph
    print("\n3️⃣  Building audit graph...")
    try:
        graph = build_audit_graph()
        print("   ✅ Graph compiled successfully")
        print("   📊 Nodes: Detective Layer (3) + Aggregator (1) + Judicial Layer (3) + Chief Justice (1)")
    except Exception as e:
        print(f"   ❌ Graph build failed: {e}")
        return
    
    # Execute graph
    print("\n4️⃣  Executing audit pipeline...")
    print("   🔍 Detective Layer (parallel)...")
    print("      - RepoInvestigator: Git + AST analysis")
    print("      - DocAnalyst: PDF parsing")
    print("      - VisionInspector: Diagram analysis")
    
    try:
        result = graph.invoke(initial_state)
        print("   ✅ Pipeline execution complete")
    except Exception as e:
        print(f"   ❌ Execution failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Validate results
    print("\n5️⃣  Validating results...")
    
    # Check evidences
    evidences = result.get("evidences", {})
    evidence_count = sum(len(v) for v in evidences.values())
    print(f"   📋 Evidence collected: {evidence_count} items in {len(evidences)} categories")
    
    if evidence_count == 0:
        print("   ⚠️  Warning: No evidence collected")
    else:
        print("   ✅ Evidence collection successful")
        for category in list(evidences.keys())[:3]:
            print(f"      - {category}: {len(evidences[category])} items")
    
    # Check opinions
    opinions = result.get("opinions", [])
    print(f"\n   ⚖️  Judicial opinions: {len(opinions)}")
    
    if len(opinions) == 0:
        print("   ⚠️  Warning: No opinions generated")
    else:
        print("   ✅ Judicial evaluation successful")
        # Count by judge
        from collections import Counter
        judge_counts = Counter(op.judge for op in opinions)
        for judge, count in judge_counts.items():
            print(f"      - {judge}: {count} opinions")
    
    # Check report
    report = result.get("final_report", "")
    print(f"\n   📄 Final report: {len(report)} characters")
    
    if len(report) == 0:
        print("   ❌ Report generation failed")
    else:
        print("   ✅ Report generated successfully")
        print("\n   Report preview:")
        print("   " + "-" * 56)
        for line in report.split("\n")[:10]:
            print(f"   {line}")
        print("   " + "-" * 56)
    
    # Check errors
    errors = result.get("errors", [])
    if errors:
        print(f"\n   ⚠️  Errors encountered: {len(errors)}")
        for error in errors[:3]:
            print(f"      - {error}")
    else:
        print("\n   ✅ No errors")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    checks = [
        ("Graph compilation", True),
        ("Pipeline execution", True),
        ("Evidence collection", evidence_count > 0),
        ("Judicial evaluation", len(opinions) > 0),
        ("Report generation", len(report) > 0),
        ("Error-free execution", len(errors) == 0)
    ]
    
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    print(f"\n✅ Passed: {passed}/{total}")
    for check, status in checks:
        icon = "✅" if status else "❌"
        print(f"   {icon} {check}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - System ready for production!")
    else:
        print(f"\n⚠️  {total - passed} checks failed - review issues above")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_full_audit_pipeline()
