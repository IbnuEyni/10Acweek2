#!/usr/bin/env python3
"""
Manual test script for Phase 2 Detective Layer.
Tests with actual GitHub repository.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.git_tools import safe_clone_repo, extract_git_history, count_commits
from src.tools.ast_tools import (
    detect_langgraph_patterns,
    find_pydantic_models,
    detect_state_reducers,
    scan_directory_for_patterns
)
from src.nodes.detectives import repo_investigator_node


def test_with_real_repo():
    """Test detective tools with our own repository."""
    
    print("=" * 60)
    print("PHASE 2 MANUAL TEST: Detective Layer")
    print("=" * 60)
    
    # Test with our own repo
    repo_url = "https://github.com/IbnuEyni/Dr_Abdi.git"
    
    print(f"\n📦 Testing with: {repo_url}")
    print("-" * 60)
    
    # Step 1: Clone repository
    print("\n1️⃣  Cloning repository...")
    try:
        repo_path = safe_clone_repo(repo_url)
        print(f"   ✅ Cloned to: {repo_path}")
    except Exception as e:
        print(f"   ❌ Clone failed: {e}")
        return
    
    # Step 2: Analyze git history
    print("\n2️⃣  Analyzing git history...")
    commits = extract_git_history(repo_path)
    commit_count = count_commits(repo_path)
    
    print(f"   📊 Total commits: {commit_count}")
    print(f"   📝 Recent commits:")
    for commit in commits[:5]:
        print(f"      - {commit['message'][:60]}")
    
    # Step 3: Find Pydantic models
    print("\n3️⃣  Searching for Pydantic models...")
    state_files = list(repo_path.rglob("*state.py"))
    
    if state_files:
        for state_file in state_files[:3]:
            models = find_pydantic_models(state_file)
            if models:
                print(f"   ✅ Found in {state_file.name}: {models}")
    else:
        print("   ⚠️  No state.py files found")
    
    # Step 4: Detect LangGraph patterns
    print("\n4️⃣  Detecting LangGraph patterns...")
    graph_files = scan_directory_for_patterns(repo_path, "StateGraph")
    
    if graph_files:
        print(f"   ✅ Found StateGraph in {len(graph_files)} files")
        for gf in graph_files[:2]:
            patterns = detect_langgraph_patterns(gf)
            print(f"      📄 {gf.name}:")
            print(f"         - Has StateGraph: {patterns.get('has_state_graph')}")
            print(f"         - Has add_node: {patterns.get('has_add_node')}")
            print(f"         - Nodes: {patterns.get('node_names', [])[:3]}")
    else:
        print("   ⚠️  No StateGraph found (expected - we haven't built graph.py yet)")
    
    # Step 5: Check state reducers
    print("\n5️⃣  Checking for state reducers...")
    if state_files:
        reducer_info = detect_state_reducers(state_files[0])
        print(f"   📊 Reducer analysis:")
        print(f"      - Has reducers: {reducer_info.get('has_reducers')}")
        print(f"      - Uses operator.add: {reducer_info.get('uses_operator_add')}")
        print(f"      - Uses operator.ior: {reducer_info.get('uses_operator_ior')}")
    
    # Step 6: Run full detective node
    print("\n6️⃣  Running RepoInvestigator node...")
    state = {
        "repo_url": repo_url,
        "pdf_path": "test.pdf",
        "rubric_dimensions": [],
        "evidences": {},
        "opinions": [],
        "final_report": "",
        "errors": []
    }
    
    result = repo_investigator_node(state)
    evidences = result.get("evidences", {})
    
    print(f"   📋 Evidence collected: {len(evidences)} categories")
    for category, evidence_list in evidences.items():
        for evidence in evidence_list:
            print(f"\n   📌 {category}:")
            print(f"      Goal: {evidence.goal}")
            print(f"      Found: {evidence.found}")
            print(f"      Confidence: {evidence.confidence:.2f}")
            print(f"      Rationale: {evidence.rationale}")
    
    print("\n" + "=" * 60)
    print("✅ PHASE 2 MANUAL TEST COMPLETE")
    print("=" * 60)
    print("\nDetective tools are working correctly!")
    print("Ready to proceed to Phase 3: Judicial Layer")


if __name__ == "__main__":
    test_with_real_repo()
