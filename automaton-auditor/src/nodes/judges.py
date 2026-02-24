"""
Judicial Layer: Judge persona nodes.
Prosecutor, Defense, TechLead - dialectical reasoning.
"""
from typing import Dict, List
from src.state import AgentState, JudicialOpinion, Evidence
from src.utils.prompts import PROSECUTOR_PROMPT, DEFENSE_PROMPT, TECH_LEAD_PROMPT
from src.utils.config import Config


def create_llm():
    """Create LLM instance based on configured provider."""
    if Config.GROQ_API_KEY:
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=Config.DEFAULT_LLM_MODEL,
            temperature=Config.DEFAULT_TEMPERATURE,
            api_key=Config.GROQ_API_KEY
        )
    elif Config.OPENAI_API_KEY:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=Config.DEFAULT_LLM_MODEL,
            temperature=Config.DEFAULT_TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
    elif Config.GOOGLE_API_KEY:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=Config.DEFAULT_LLM_MODEL,
            temperature=Config.DEFAULT_TEMPERATURE,
            google_api_key=Config.GOOGLE_API_KEY
        )
    else:
        raise ValueError("No LLM provider configured")


def format_evidence_summary(evidences: Dict[str, List[Evidence]]) -> str:
    """Format evidence for judge consumption."""
    summary = []
    for category, evidence_list in evidences.items():
        for idx, evidence in enumerate(evidence_list):
            summary.append(f"""
Evidence ID: {category}_{idx}
Goal: {evidence.goal}
Found: {evidence.found}
Content: {evidence.content}
Location: {evidence.location}
Rationale: {evidence.rationale}
Confidence: {evidence.confidence:.2f}
""")
    return "\n".join(summary)


def evaluate_criterion(
    llm,
    prompt_template: str,
    judge_name: str,
    criterion,
    evidences: Dict[str, List[Evidence]]
) -> JudicialOpinion:
    """
    Evaluate a single criterion with a judge persona.
    
    Args:
        llm: Language model instance
        prompt_template: Judge-specific prompt
        judge_name: "Prosecutor", "Defense", or "TechLead"
        criterion: RubricDimension object
        evidences: Collected evidence
        
    Returns:
        JudicialOpinion with score and reasoning
    """
    evidence_summary = format_evidence_summary(evidences)
    
    # Get judicial logic for this judge
    judicial_logic = criterion.judicial_logic.get(
        judge_name.lower().replace("techlead", "tech_lead"),
        "Apply standard evaluation"
    )
    
    prompt = prompt_template.format(
        criterion_name=criterion.name,
        judicial_logic=judicial_logic,
        evidence_summary=evidence_summary
    )
    
    try:
        # Simple text generation with JSON parsing
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        # Parse JSON from response
        import json
        import re
        
        # Extract JSON from markdown code blocks if present
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'{.*}', content, re.DOTALL)
            json_str = json_match.group(0) if json_match else content
        
        data = json.loads(json_str)
        
        return JudicialOpinion(
            judge=judge_name,
            criterion_id=criterion.id,
            score=int(data.get("score", 3)),
            argument=data.get("argument", content[:200]),
            cited_evidence=data.get("cited_evidence", [])
        )
    except Exception as e:
        # Fallback opinion on error
        return JudicialOpinion(
            judge=judge_name,
            criterion_id=criterion.id,
            score=3,
            argument=f"Error during evaluation: {str(e)}",
            cited_evidence=[]
        )


def prosecutor_node(state: AgentState) -> AgentState:
    """Prosecutor: Critical lens evaluation."""
    llm = create_llm()
    opinions = []
    
    for criterion in state["rubric_dimensions"]:
        opinion = evaluate_criterion(
            llm,
            PROSECUTOR_PROMPT,
            "Prosecutor",
            criterion,
            state["evidences"]
        )
        opinions.append(opinion)
    
    return {"opinions": opinions}


def defense_node(state: AgentState) -> AgentState:
    """Defense: Optimistic lens evaluation."""
    llm = create_llm()
    opinions = []
    
    for criterion in state["rubric_dimensions"]:
        opinion = evaluate_criterion(
            llm,
            DEFENSE_PROMPT,
            "Defense",
            criterion,
            state["evidences"]
        )
        opinions.append(opinion)
    
    return {"opinions": opinions}


def tech_lead_node(state: AgentState) -> AgentState:
    """Tech Lead: Pragmatic lens evaluation."""
    llm = create_llm()
    opinions = []
    
    for criterion in state["rubric_dimensions"]:
        opinion = evaluate_criterion(
            llm,
            TECH_LEAD_PROMPT,
            "TechLead",
            criterion,
            state["evidences"]
        )
        opinions.append(opinion)
    
    return {"opinions": opinions}
