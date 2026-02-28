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
    """Forensic evidence collected by Detective agents.
    
    All fields are validated at runtime. Confidence must be [0.0, 1.0].
    Goal and rationale must be non-empty strings.
    """
    goal: str = Field(
        min_length=1,
        description="What this evidence was meant to verify (e.g., 'StateGraph usage')"
    )
    found: bool = Field(
        description="Whether the artifact exists (True) or is missing (False)"
    )
    content: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Extracted content or code snippet (max 10K chars for performance)"
    )
    location: str = Field(
        min_length=1,
        description="File path, commit hash, or page number (e.g., 'src/graph.py:L15')"
    )
    rationale: str = Field(
        min_length=10,
        description="Detective's reasoning for confidence level (min 10 chars for quality)"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score [0.0, 1.0] where 1.0 = certain, 0.0 = uncertain"
    )


class JudicialOpinion(BaseModel):
    """Opinion from a Judge persona on a specific rubric criterion.
    
    Score must be [1, 5] per rubric scale. Argument must be substantive (min 20 chars).
    Each opinion must cite at least one piece of evidence.
    """
    judge: Literal["Prosecutor", "Defense", "TechLead"] = Field(
        description="Judge persona: Prosecutor (critical), Defense (generous), TechLead (pragmatic)"
    )
    criterion_id: str = Field(
        min_length=1,
        description="ID from rubric dimension (e.g., 'typed_state_definitions')"
    )
    score: int = Field(
        ge=1,
        le=5,
        description="Score [1, 5] where 1=poor, 2=basic, 3=competent, 4=advanced, 5=expert"
    )
    argument: str = Field(
        min_length=20,
        description="Detailed reasoning for the score (min 20 chars for substantive feedback)"
    )
    cited_evidence: List[str] = Field(
        min_items=1,
        description="List of evidence locations referenced (must cite at least 1)"
    )


class RubricDimension(BaseModel):
    """Single dimension from the rubric constitution.
    
    Defines what detectives should look for and how judges should evaluate.
    """
    id: str = Field(
        min_length=1,
        description="Unique identifier (e.g., 'typed_state_definitions')"
    )
    name: str = Field(
        min_length=1,
        description="Human-readable name (e.g., 'Typed State Definitions')"
    )
    target_artifact: Literal["github_repo", "pdf_report", "pdf_images"] = Field(
        description="Which artifact to analyze: github_repo (code), pdf_report (docs), or pdf_images (diagrams)"
    )
    forensic_instruction: str = Field(
        min_length=10,
        description="Instructions for detectives on what evidence to collect"
    )
    success_pattern: str = Field(
        description="Pattern indicating successful implementation"
    )
    failure_pattern: str = Field(
        description="Pattern indicating failed or missing implementation"
    )


class AgentState(TypedDict):
    """
    Main state graph state with reducers for parallel execution safety.
    
    Reducers ensure CRDT-like behavior for concurrent writes:
    - operator.ior: Merges dicts without overwriting (|= operator, commutative)
    - operator.add: Concatenates lists (+ operator, order-preserving)
    
    Fields:
    - repo_url: GitHub repository URL to audit
    - pdf_path: Local path to interim report PDF
    - rubric_dimensions: List of evaluation criteria from rubric JSON
    - evidences: Dict mapping detective name to list of Evidence objects
    - opinions: List of JudicialOpinion objects from all judges
    - final_report: Markdown report from Chief Justice
    - errors: List of error messages from failed nodes (for graceful degradation)
    
    Reducer Strategy:
    ----------------
    Each parallel-safe field uses a specific reducer to prevent data loss:
    
    1. evidences (operator.ior):
       - Why: Dict merge where each detective writes to unique key
       - Behavior: {"repo": [...]} | {"doc": [...]} = {"repo": [...], "doc": [...]}
       - Commutative: Yes (order doesn't matter)
       - Idempotent: Yes (same write produces same result)
       - Use case: 3 detectives write evidence concurrently without conflicts
       - CRDT Proof: operator.ior implements OR-Set semantics (add-wins)
         * Concurrent writes to different keys: {a:1} | {b:2} = {a:1, b:2}
         * Concurrent writes to same key: {a:1} | {a:2} = {a:2} (last-write-wins)
         * Associative: (A | B) | C = A | (B | C)
         * Commutative: A | B = B | A
         * Idempotent: A | A = A
       - Implementation: Python dict.__ior__ (PEP 584)
    
    2. opinions (operator.add):
       - Why: List concatenation preserving all judge opinions
       - Behavior: [op1, op2] + [op3] = [op1, op2, op3]
       - Commutative: No (order matters for report readability)
       - Idempotent: No (duplicate writes append duplicates)
       - Use case: 3 judges write opinions, all must be preserved
       - CRDT Proof: operator.add implements G-Counter semantics (grow-only)
         * Concurrent appends: [a] + [b] = [a, b]
         * Associative: ([a] + [b]) + [c] = [a] + ([b] + [c])
         * NOT commutative: [a] + [b] ≠ [b] + [a] (order preserved)
         * Monotonic: len(L1 + L2) >= max(len(L1), len(L2))
       - Implementation: Python list.__add__
    
    3. errors (operator.add):
       - Why: List concatenation preserving all error messages
       - Behavior: ["err1"] + ["err2"] = ["err1", "err2"]
       - Commutative: No (chronological order useful for debugging)
       - Idempotent: No (duplicate errors indicate retry attempts)
       - Use case: Any node can report errors without blocking others
       - CRDT Proof: Same as opinions (G-Counter semantics)
    """
    repo_url: str
    pdf_path: str
    rubric_dimensions: List[RubricDimension]
    
    # Parallel-safe collections using reducers
    # operator.ior: Dict merge (|=) - each detective writes to unique key
    evidences: Annotated[Dict[str, List[Evidence]], operator.ior]
    
    # operator.add: List concat (+) - preserve all opinions from 3 judges
    opinions: Annotated[List[JudicialOpinion], operator.add]
    
    final_report: str
    
    # operator.add: List concat (+) - preserve all errors for debugging
    errors: Annotated[List[str], operator.add]
