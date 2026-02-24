# Automaton Auditor Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     AUTOMATON AUDITOR                            │
│              Enterprise Multi-Agent Audit System                 │
└─────────────────────────────────────────────────────────────────┘

INPUT: GitHub URL + PDF Report
  │
  ├─────────────────────────────────────────────────────────────┐
  │                                                              │
  ▼                                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 1: DETECTIVE LAYER                      │
│                   (Parallel Evidence Collection)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ RepoInvestigator │  │   DocAnalyst     │  │   Vision     │ │
│  │  (Code Detective)│  │(Paper Detective) │  │  Inspector   │ │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────┤ │
│  │ • Git clone      │  │ • PDF parse      │  │ • Extract    │ │
│  │ • AST parsing    │  │ • Concept search │  │   images     │ │
│  │ • Git history    │  │ • Cross-ref      │  │ • Classify   │ │
│  │ • StateGraph     │  │ • Hallucination  │  │   diagrams   │ │
│  │   detection      │  │   detection      │  │ • Flow check │ │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘ │
│           │                     │                    │          │
│           └─────────────────────┼────────────────────┘          │
│                                 │                                │
└─────────────────────────────────┼────────────────────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │  Evidence Aggregator     │
                    │  (Synchronization Node)  │
                    │                          │
                    │  Collects all Evidence   │
                    │  objects into state      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 2: JUDICIAL LAYER                       │
│                  (Parallel Dialectical Analysis)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │  Prosecutor  │    │   Defense    │    │  Tech Lead   │     │
│  │ (Critical)   │    │ (Optimistic) │    │ (Pragmatic)  │     │
│  ├──────────────┤    ├──────────────┤    ├──────────────┤     │
│  │ Philosophy:  │    │ Philosophy:  │    │ Philosophy:  │     │
│  │ "Trust No    │    │ "Reward      │    │ "Does it     │     │
│  │  One"        │    │  Effort"     │    │  Work?"      │     │
│  │              │    │              │    │              │     │
│  │ Looks for:   │    │ Looks for:   │    │ Looks for:   │     │
│  │ • Security   │    │ • Intent     │    │ • Function   │     │
│  │ • Gaps       │    │ • Creativity │    │ • Maintainab.│     │
│  │ • Laziness   │    │ • Process    │    │ • Tech debt  │     │
│  │              │    │              │    │              │     │
│  │ Output:      │    │ Output:      │    │ Output:      │     │
│  │ Score: 1-5   │    │ Score: 1-5   │    │ Score: 1-5   │     │
│  │ + Argument   │    │ + Argument   │    │ + Argument   │     │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
│         │                   │                   │              │
│         └───────────────────┼───────────────────┘              │
│                             │                                   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
                ┌──────────────────────────────┐
                │   LAYER 3: SUPREME COURT     │
                │      (Chief Justice)         │
                ├──────────────────────────────┤
                │                              │
                │  Deterministic Synthesis:    │
                │                              │
                │  1. Security Override Rule   │
                │  2. Fact Supremacy Rule      │
                │  3. Conflict Resolution      │
                │                              │
                │  NOT an LLM prompt!          │
                │  Hardcoded Python logic      │
                │                              │
                └──────────────┬───────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FINAL REPORT      │
                    │   (Markdown)        │
                    ├─────────────────────┤
                    │ • Executive Summary │
                    │ • Criterion Scores  │
                    │ • Dissent Analysis  │
                    │ • Remediation Plan  │
                    └─────────────────────┘
```

## State Flow

```
AgentState {
  repo_url: str
  pdf_path: str
  rubric_dimensions: List[RubricDimension]
  
  // Parallel-safe with reducers
  evidences: Dict[str, List[Evidence]]  // operator.ior
  opinions: List[JudicialOpinion]       // operator.add
  
  final_report: str
  errors: List[str]
}
```

## Data Models

```
Evidence                    JudicialOpinion              RubricDimension
├─ goal: str               ├─ judge: Literal            ├─ id: str
├─ found: bool             ├─ criterion_id: str         ├─ name: str
├─ content: Optional[str]  ├─ score: int (1-5)          ├─ target_artifact
├─ location: str           ├─ argument: str             ├─ forensic_instruction
├─ rationale: str          └─ cited_evidence: List[str] └─ judicial_logic: Dict
└─ confidence: float
```

## Execution Flow

```
1. INITIALIZATION
   ├─ Load rubric.json
   ├─ Parse repo_url and pdf_path
   └─ Initialize AgentState

2. DETECTIVE PHASE (Parallel)
   ├─ RepoInvestigator → Evidence[]
   ├─ DocAnalyst → Evidence[]
   └─ VisionInspector → Evidence[]
   
3. AGGREGATION
   └─ Merge all Evidence into state.evidences

4. JUDICIAL PHASE (Parallel)
   ├─ Prosecutor → JudicialOpinion[]
   ├─ Defense → JudicialOpinion[]
   └─ TechLead → JudicialOpinion[]

5. SYNTHESIS
   └─ ChiefJustice → final_report (Markdown)

6. OUTPUT
   └─ Write to audit/report_*.md
```

## Key Patterns

### Fan-Out / Fan-In
```
        START
          │
    ┌─────┼─────┐
    │     │     │
   [A]   [B]   [C]  ← Parallel execution
    │     │     │
    └─────┼─────┘
          │
       SYNC NODE   ← Aggregation
          │
    ┌─────┼─────┐
    │     │     │
   [D]   [E]   [F]  ← Parallel execution
    │     │     │
    └─────┼─────┘
          │
         END
```

### State Reducers
```python
# Without reducer (WRONG - data loss)
state["opinions"] = [opinion1]  # Overwrites!

# With reducer (CORRECT - accumulates)
state["opinions"] = [opinion1]  # Appends via operator.add
```

## Technology Stack

- **Orchestration**: LangGraph (StateGraph)
- **LLMs**: OpenAI GPT-4o / Anthropic Claude
- **Validation**: Pydantic 2.x
- **Git Operations**: GitPython
- **PDF Parsing**: Docling
- **Observability**: LangSmith
- **Testing**: pytest
- **Deployment**: Docker

## Security Features

1. **Sandboxed Git Clone**: tempfile.TemporaryDirectory()
2. **No Shell Injection**: subprocess with check=True
3. **API Key Management**: Environment variables only
4. **Timeout Guards**: All external operations have timeouts
5. **Input Validation**: Pydantic models enforce constraints

---

**Architecture Status**: ✅ Designed and Validated
**Implementation Status**: Phase 1 Complete, Phase 2 Ready
