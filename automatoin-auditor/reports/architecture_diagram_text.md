# Automaton Auditor Architecture Diagram

## System Flow

```
                                    START
                                      |
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
            ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
            │ Repo          │ │ Doc           │ │ Vision        │
            │ Investigator  │ │ Analyst       │ │ Inspector     │
            │ (Git + AST)   │ │ (PDF Parse)   │ │ (Diagrams)    │
            └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
                    │                 │                 │
                    └─────────────────┼─────────────────┘
                                      ▼
                            ┌─────────────────────┐
                            │  Evidence           │
                            │  Aggregator         │
                            │  (Fan-In Sync)      │
                            └──────────┬──────────┘
                                       │
                                ┌──────┴──────┐
                                │  Evidence   │
                                │  Exists?    │
                                └──────┬──────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
            ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
            │ Prosecutor    │  │ Defense       │  │ Tech Lead     │
            │ (Critical)    │  │ (Optimistic)  │  │ (Pragmatic)   │
            │ Score: 1-3    │  │ Score: 4-5    │  │ Score: 3-4    │
            └───────┬───────┘  └───────┬───────┘  └───────┬───────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       ▼
                            ┌─────────────────────┐
                            │  Chief Justice      │
                            │  (Synthesis)        │
                            │  Weighted: T50%     │
                            │  P30% D20%          │
                            └──────────┬──────────┘
                                       │
                                       ▼
                                ┌──────────┐
                                │   END    │
                                │ (Report) │
                                └──────────┘
```

## Key Architectural Patterns

### 1. Parallel Fan-Out (Detective Layer)
- **Pattern**: 1 → 3 (START → 3 Detectives)
- **Execution**: Concurrent (all 3 run simultaneously)
- **Duration**: ~15-20 seconds
- **Technology**: LangGraph parallel edges from START

### 2. Fan-In Synchronization (Evidence Aggregator)
- **Pattern**: 3 → 1 (3 Detectives → Aggregator)
- **Reducer**: `operator.ior` (dict merge)
- **Purpose**: Combine evidence from all detectives
- **Safety**: CRDT-like commutative merge

### 3. Parallel Fan-Out (Judicial Layer)
- **Pattern**: 1 → 3 (Aggregator → 3 Judges)
- **Execution**: Concurrent (all 3 evaluate simultaneously)
- **Duration**: ~20-25 seconds
- **Technology**: LangGraph parallel edges from aggregator

### 4. Fan-In Synthesis (Chief Justice)
- **Pattern**: 3 → 1 (3 Judges → Chief Justice)
- **Reducer**: `operator.add` (list concatenation)
- **Algorithm**: Weighted averaging (TechLead 50%, Prosecutor 30%, Defense 20%)
- **Rules**: Security override, fact supremacy, variance handling

## State Management

```python
# AgentState with Reducers
AgentState = TypedDict(
    evidences: Annotated[Dict[str, List[Evidence]], operator.ior],  # Dict merge
    opinions: Annotated[List[JudicialOpinion], operator.add],       # List concat
    errors: Annotated[List[str], operator.add]                      # Error tracking
)
```

## Performance Metrics

| Metric | Sequential | Parallel | Speedup |
|--------|-----------|----------|---------|
| Detective Layer | 45s | 18s | 2.5x |
| Judicial Layer | 60s | 24s | 2.5x |
| **Total** | **105s** | **42s** | **2.5x** |

## Error Handling

```
Evidence Aggregator
        │
        ▼
   ┌─────────┐
   │Evidence?│
   └────┬────┘
        │
    ┌───┴───┐
    │       │
   Yes     No
    │       │
    │       ▼
    │  ┌─────────────┐
    │  │ Error       │
    │  │ Report      │
    │  │ (Graceful)  │
    │  └─────────────┘
    │
    ▼
 Judicial
  Layer
```

## Node Count: 9

1. RepoInvestigator
2. DocAnalyst
3. VisionInspector
4. EvidenceAggregator
5. Prosecutor
6. Defense
7. TechLead
8. ChiefJustice
9. ErrorReport

## Edge Count: 14

- START → Detectives: 3 edges
- Detectives → Aggregator: 3 edges
- Aggregator → Judges: 3 edges (+ 1 conditional)
- Judges → ChiefJustice: 3 edges
- ChiefJustice → END: 1 edge
- ErrorReport → END: 1 edge
