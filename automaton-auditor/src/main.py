"""
CLI entry point for Automaton Auditor.
Executes full audit pipeline from repository URL to final report.
"""
import argparse
from pathlib import Path
from datetime import datetime
from src.graph import build_audit_graph
from src.utils.rubric_loader import load_rubric
from src.state import AgentState


def main():
    """Execute audit on target repository."""
    parser = argparse.ArgumentParser(
        description="Automaton Auditor - Enterprise Multi-Agent Code Review System"
    )
    parser.add_argument(
        "--repo-url",
        required=True,
        help="GitHub repository URL to audit"
    )
    parser.add_argument(
        "--pdf-path",
        required=True,
        help="Path to architectural report PDF"
    )
    parser.add_argument(
        "--output",
        default="audit/report_generated/",
        help="Output directory for audit report"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🤖 AUTOMATON AUDITOR - Enterprise Code Review System")
    print("=" * 60)
    print(f"\n📦 Repository: {args.repo_url}")
    print(f"📄 Report: {args.pdf_path}")
    print(f"📁 Output: {args.output}\n")
    
    # Load rubric
    print("⚖️  Loading evaluation rubric...")
    rubric = load_rubric()
    print(f"   ✅ Loaded {len(rubric['dimensions'])} evaluation criteria\n")
    
    # Initialize state
    initial_state: AgentState = {
        "repo_url": args.repo_url,
        "pdf_path": args.pdf_path,
        "rubric_dimensions": rubric["dimensions"],
        "evidences": {},
        "opinions": [],
        "final_report": "",
        "errors": []
    }
    
    # Build and execute graph
    print("🔧 Building audit graph...")
    graph = build_audit_graph()
    print("   ✅ Graph compiled with parallel execution\n")
    
    print("🚀 Executing audit pipeline...")
    print("   → Detective Layer (parallel evidence collection)")
    print("   → Judicial Layer (dialectical evaluation)")
    print("   → Chief Justice (deterministic synthesis)\n")
    
    try:
        result = graph.invoke(initial_state)
        
        # Save report
        output_path = Path(args.output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"audit_report_{timestamp}.md"
        report_file.write_text(result["final_report"])
        
        # Summary
        evidence_count = sum(len(v) for v in result.get("evidences", {}).values())
        opinion_count = len(result.get("opinions", []))
        error_count = len(result.get("errors", []))
        
        print("=" * 60)
        print("✅ AUDIT COMPLETE")
        print("=" * 60)
        print(f"\n📊 Statistics:")
        print(f"   Evidence Collected: {evidence_count}")
        print(f"   Judicial Opinions: {opinion_count}")
        print(f"   Errors: {error_count}")
        print(f"\n📄 Report saved to: {report_file}")
        print(f"   Size: {len(result['final_report'])} characters\n")
        
        if error_count > 0:
            print("⚠️  Errors encountered:")
            for error in result["errors"][:3]:
                print(f"   - {error}")
        
    except Exception as e:
        print(f"\n❌ Audit failed: {e}")
        raise


if __name__ == "__main__":
    main()
