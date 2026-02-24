"""
Core state models for the Automaton Auditor.
Implements strict typing with Pydantic and state reducers for parallel execution.
"""
import operator
from typing import Annotated, Dict, List, Optional
from pydantic import BaseModel, Field
try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict


class Evidence(BaseModel):
    """Forensic evidence collected by Detective agents."""
    goal: str = Field(description="What this evidence was meant to verify")
    found: bool = Field(description="Whether the artifact exists")
    content: Optional[str] = Field(default=None, description="Extracted content or code snippet")
    location: str = Field(description="File path, commit hash, or page number")
    rationale: str = Field(description="Detective's reasoning for confidence level")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")


class JudicialOpinion(BaseModel):
    """Opinion from a Judge persona on a specific rubric criterion."""
    judge: Literal["Prosecutor", "Defense", "TechLead"]
    criterion_id: str = Field(description="ID from rubric dimension")
    score: int = Field(ge=1, le=5, description="Score 1-5 per rubric")
    argument: str = Field(description="Detailed reasoning for the score")
    cited_evidence: List[str] = Field(description="List of evidence locations referenced")


class RubricDimension(BaseModel):
    """Single dimension from the rubric constitution."""
    id: str
    name: str
    target_artifact: Literal["github_repo", "pdf_report"]
    forensic_instruction: str
    judicial_logic: Dict[str, str]


class AgentState(TypedDict):
    """
    Main state graph state with reducers for parallel execution safety.
    
    Reducers:
    - operator.ior: Merges dicts without overwriting (|= operator)
    - operator.add: Concatenates lists (+ operator)
    """
    repo_url: str
    pdf_path: str
    rubric_dimensions: List[RubricDimension]
    
    # Parallel-safe collections using reducers
    evidences: Annotated[Dict[str, List[Evidence]], operator.ior]
    opinions: Annotated[List[JudicialOpinion], operator.add]
    
    final_report: str
    errors: Annotated[List[str], operator.add]
