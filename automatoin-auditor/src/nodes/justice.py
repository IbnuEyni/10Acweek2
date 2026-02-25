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
    NOT an LLM - uses hardcoded conflict resolution rules.
    """
    opinions = state["opinions"]
    synthesis_rules = get_synthesis_rules()
    
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
        
        # Rule 1: Security Override
        if any("security" in op.argument.lower() or "injection" in op.argument.lower() 
               for op in criterion_opinions):
            final_scores[criterion_id] = min(3, max(o.score for o in criterion_opinions))
            dissents.append(
                f"**{criterion_id}**: Security flaw detected. Score capped at 3 per synthesis rules."
            )
            remediation.append(
                f"- **{criterion_id}**: Address security vulnerabilities immediately. "
                f"Prosecutor noted: {prosecutor_op.argument[:100]}..."
            )
            continue
        
        # Rule 2: Fact Supremacy (Tech Lead has highest weight)
        if tech_lead_op.score <= 2:
            final_scores[criterion_id] = tech_lead_op.score
            dissents.append(
                f"**{criterion_id}**: Tech Lead ruling ({tech_lead_op.score}) overrides optimism. "
                f"Rationale: {tech_lead_op.argument[:80]}..."
            )
            remediation.append(
                f"- **{criterion_id}**: {tech_lead_op.argument[:150]}..."
            )
            continue
        
        # Rule 3: High Variance Resolution
        scores = [prosecutor_op.score, defense_op.score, tech_lead_op.score]
        variance = max(scores) - min(scores)
        
        if variance > 2:
            # Significant disagreement - use weighted average favoring Tech Lead
            weighted_score = (
                prosecutor_op.score * 0.25 +
                defense_op.score * 0.15 +
                tech_lead_op.score * 0.60
            )
            final_scores[criterion_id] = round(weighted_score)
            dissents.append(
                f"**{criterion_id}**: High variance detected (Prosecutor: {prosecutor_op.score}, "
                f"Defense: {defense_op.score}, Tech Lead: {tech_lead_op.score}). "
                f"Weighted resolution: {final_scores[criterion_id]}"
            )
        else:
            # Low variance - weighted average
            weighted_score = (
                prosecutor_op.score * 0.30 +
                defense_op.score * 0.20 +
                tech_lead_op.score * 0.50
            )
            final_scores[criterion_id] = round(weighted_score)
    
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
    report += "1. **Security Override**: Security flaws cap score at 3\n"
    report += "2. **Fact Supremacy**: Tech Lead ruling overrides opinions when score ≤ 2\n"
    report += "3. **Weighted Resolution**: Tech Lead 50%, Prosecutor 30%, Defense 20%\n\n"
    
    report += "*Report generated by Automaton Auditor - Enterprise Multi-Agent System*\n"
    
    return report
