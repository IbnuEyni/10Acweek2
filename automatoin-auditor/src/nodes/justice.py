"""
Supreme Court Layer: Chief Justice synthesis.
Deterministic conflict resolution with hardcoded rules.
"""
from typing import Dict, List
from collections import defaultdict
from src.state import AgentState, JudicialOpinion
from src.utils.rubric_loader import get_synthesis_rules


def chief_justice_node(state: AgentState) -> AgentState:
    """
    Chief Justice: Deterministic synthesis of judicial opinions.
    Enterprise-grade conflict resolution using statistical methods.
    """
    opinions = state["opinions"]
    
    # Group opinions by criterion
    opinions_by_criterion = defaultdict(list)
    for opinion in opinions:
        opinions_by_criterion[opinion.criterion_id].append(opinion)
    
    # Synthesize final scores
    final_scores = {}
    dissents = []
    remediation = []
    
    for criterion_id, criterion_opinions in opinions_by_criterion.items():
        # Extract scores and arguments
        prosecutor_op = next((o for o in criterion_opinions if o.judge == "Prosecutor"), None)
        defense_op = next((o for o in criterion_opinions if o.judge == "Defense"), None)
        tech_lead_op = next((o for o in criterion_opinions if o.judge == "TechLead"), None)
        
        if not all([prosecutor_op, defense_op, tech_lead_op]):
            continue
        
        scores = [prosecutor_op.score, defense_op.score, tech_lead_op.score]
        
        # Rule 1: Critical Security Veto
        # If security controls are missing AND Prosecutor flags security, cap at 2
        has_security_concern = "security" in prosecutor_op.argument.lower() or "injection" in prosecutor_op.argument.lower()
        has_security_evidence = "security_sandboxing" in str(state.get("evidences", {}))
        
        if has_security_concern and not has_security_evidence:
            final_scores[criterion_id] = 2
            dissents.append(
                f"**{criterion_id}**: Critical security flaw without controls. Score: 2/5."
            )
            remediation.append(
                f"- **{criterion_id}**: CRITICAL - Implement sandboxing and input validation immediately."
            )
            continue
        
        # Rule 2: Consensus Detection
        # If all judges agree within 1 point, use median (robust to outliers)
        variance = max(scores) - min(scores)
        if variance <= 1:
            final_scores[criterion_id] = sorted(scores)[1]  # Median
            continue
        
        # Rule 3: Weighted Average (Enterprise Standard)
        # Tech Lead: 50% (validates functionality)
        # Prosecutor: 30% (ensures quality standards)
        # Defense: 20% (considers effort and intent)
        weighted_score = (
            tech_lead_op.score * 0.50 +
            prosecutor_op.score * 0.30 +
            defense_op.score * 0.20
        )
        
        # Rule 4: Statistical Rounding
        # Use standard rounding (0.5 rounds up)
        final_scores[criterion_id] = round(weighted_score)
        
        # Document high variance cases
        if variance > 2:
            dissents.append(
                f"**{criterion_id}**: High variance (P:{prosecutor_op.score}, D:{defense_op.score}, T:{tech_lead_op.score}). "
                f"Weighted average: {weighted_score:.2f} → {final_scores[criterion_id]}"
            )
    
    # Generate markdown report
    report = generate_markdown_report(
        final_scores,
        dissents,
        opinions_by_criterion,
        remediation,
        state
    )
    
    return {"final_report": report}


def generate_markdown_report(
    final_scores: Dict[str, int],
    dissents: List[str],
    opinions_by_criterion: Dict[str, List[JudicialOpinion]],
    remediation: List[str],
    state: AgentState
) -> str:
    """Generate comprehensive markdown audit report."""
    
    report = f"""# Automaton Auditor Report

## Executive Summary

**Repository**: {state['repo_url']}
**Report Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Overall Assessment

"""
    
    # Calculate overall score
    if final_scores:
        overall_score = sum(final_scores.values()) / len(final_scores)
        report += f"**Overall Score**: {overall_score:.2f}/5.0\n\n"
        
        if overall_score >= 4.5:
            report += "🏆 **Grade**: Master Thinker - Exceptional implementation\n"
        elif overall_score >= 3.5:
            report += "✅ **Grade**: Competent Orchestrator - Solid work\n"
        else:
            report += "⚠️ **Grade**: Needs Improvement - Review remediation plan\n"
    
    report += "\n---\n\n## Criterion Breakdown\n\n"
    
    # Detail each criterion
    for criterion_id, score in final_scores.items():
        criterion_ops = opinions_by_criterion.get(criterion_id, [])
        
        report += f"### {criterion_id.replace('_', ' ').title()}\n\n"
        report += f"**Final Score**: {score}/5\n\n"
        
        # Show each judge's opinion
        for opinion in criterion_ops:
            report += f"#### {opinion.judge} Opinion\n"
            report += f"- **Score**: {opinion.score}/5\n"
            report += f"- **Argument**: {opinion.argument}\n"
            report += f"- **Evidence Cited**: {', '.join(opinion.cited_evidence) if opinion.cited_evidence else 'None'}\n\n"
        
        report += "---\n\n"
    
    # Dissent section
    if dissents:
        report += "## Chief Justice Dissent Analysis\n\n"
        report += "*Why the Prosecutor and Defense disagreed:*\n\n"
        for dissent in dissents:
            report += f"- {dissent}\n"
        report += "\n---\n\n"
    
    # Remediation plan
    if remediation:
        report += "## Remediation Plan\n\n"
        report += "*Specific actions to improve the score:*\n\n"
        for item in remediation:
            report += f"{item}\n"
        report += "\n---\n\n"
    
    report += "## Synthesis Rules Applied\n\n"
    report += "1. **Critical Security Veto**: Missing security controls = 2/5 (enterprise standard)\n"
    report += "2. **Consensus Detection**: Variance ≤ 1 point = use median (robust to outliers)\n"
    report += "3. **Weighted Average**: Tech Lead 50%, Prosecutor 30%, Defense 20%\n"
    report += "4. **Statistical Rounding**: Standard rounding (0.5 rounds up)\n\n"
    
    report += "*Report generated by Automaton Auditor - Enterprise Multi-Agent System*\n"
    
    return report
