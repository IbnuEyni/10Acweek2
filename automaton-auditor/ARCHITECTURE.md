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

## Architectural Patterns

### StateGraph Orchestration
LangGraph's StateGraph provides declarative workflow definition with conditional edges. Unlike imperative control flow, StateGraph enables:
- **Compile-time validation**: Graph structure verified before execution
- **Automatic parallelization**: Nodes without dependencies run concurrently
- **State persistence**: Checkpointing for long-running workflows
- **Visual debugging**: Graph visualization with Mermaid export

### Fan-Out Pattern
Single node branches to multiple parallel nodes. Used in detective layer (1 → 3) and judicial layer (1 → 3).

```
        START
          │
    ┌─────┼─────┐
    │     │     │
   [A]   [B]   [C]  ← Parallel execution
```

**Implementation**: Multiple `add_edge()` calls from same source node.

### Fan-In Pattern
Multiple nodes converge to single aggregator. Synchronization point for parallel results.

```
   [A]   [B]   [C]
    │     │     │
    └─────┼─────┘
          │
       SYNC NODE   ← Aggregation
```

**Implementation**: Multiple `add_edge()` calls to same target node.

### State Reducers (CRDTs)
Conflict-free replicated data types ensure parallel safety without locks.

```python
# Without reducer (WRONG - data loss)
state["opinions"] = [opinion1]  # Overwrites!

# With reducer (CORRECT - accumulates)
state["opinions"] = [opinion1]  # Appends via operator.add
```

**operator.add**: Concatenates lists (for opinions)  
**operator.ior**: Merges dicts (for evidences)  

### Sandboxed Execution
Git operations in isolated tempfile.mkdtemp() environments prevent:
- **Filesystem pollution**: No persistent clones
- **Path traversal attacks**: Contained in temp directory
- **Concurrent conflicts**: Each audit gets unique directory
- **Resource leaks**: Automatic cleanup with shutil.rmtree()

## Technology Stack

### Core Framework
- **Orchestration**: LangGraph StateGraph with parallel execution
- **State Management**: TypedDict with Annotated reducers
- **Validation**: Pydantic 2.x BaseModel with Field constraints

### LLM Infrastructure
- **Judicial Layer**: Groq Llama 3.3 70B Versatile (free tier, 30 req/min)
- **Vision Layer**: Google Gemini 2.5 Flash (multimodal, 1500 req/day)
- **Observability**: LangSmith tracing with automatic logging

### Analysis Tools
- **Code Analysis**: Python ast module (AST parsing)
- **Git Operations**: subprocess with sandboxed tempfile.mkdtemp()
- **PDF Parsing**: Docling (primary), PyPDF2 (fallback)
- **Image Extraction**: pdf2image with Pillow

### Development
- **Testing**: pytest with integration test suite
- **Deployment**: Docker with multi-stage builds
- **CLI**: argparse with progress tracking

## Security Features

1. **Sandboxed Git Clone**: tempfile.TemporaryDirectory()
2. **No Shell Injection**: subprocess with check=True
3. **API Key Management**: Environment variables only
4. **Timeout Guards**: All external operations have timeouts
5. **Input Validation**: Pydantic models enforce constraints

---

**Architecture Status**: ✅ Designed, Validated, and Implemented  
**Implementation Status**: ✅ ALL PHASES COMPLETE - Production Ready  
**Test Status**: 6/6 Test Suites Passing
