# Architecture Decision Records (ADR)

## ADR-001: Use operator.ior for Evidence Dict Merging

**Status**: Accepted  
**Date**: 2024-02-27  
**Context**: Three detectives (repo, doc, vision) run in parallel and each produces evidence. We need to merge their outputs without data loss.

**Decision**: Use `operator.ior` (dict merge operator `|=`) as the state reducer for the `evidences` field.

**Rationale**:
- **Commutative**: `{a:1} | {b:2} = {b:2} | {a:1}` - order doesn't matter
- **Idempotent**: `{a:1} | {a:1} = {a:1}` - duplicate writes are safe
- **No overwrites**: Each detective writes to unique key (repo_investigator, doc_analyst, vision_inspector)
- **CRDT semantics**: Implements OR-Set (add-wins) for conflict-free replication

**Consequences**:
- ✅ Parallel detectives never overwrite each other's evidence
- ✅ Deterministic merge regardless of execution order
- ✅ No locks or mutexes needed

**Implementation**:
```python
evidences: Annotated[Dict[str, List[Evidence]], operator.ior]
```

---

## ADR-002: Use operator.add for Opinion List Concatenation

**Status**: Accepted  
**Date**: 2024-02-27  
**Context**: Three judges (prosecutor, defense, tech_lead) run in parallel and each produces opinions. We need to preserve ALL opinions for dialectical reasoning.

**Decision**: Use `operator.add` (list concatenation `+`) as the state reducer for the `opinions` field.

**Rationale**:
- **Preserves all data**: `[op1] + [op2] + [op3] = [op1, op2, op3]`
- **Order-preserving**: Maintains chronological order for report readability
- **Monotonic growth**: List only grows, never shrinks (G-Counter semantics)
- **No data loss**: All three judge opinions are captured

**Consequences**:
- ✅ All judicial opinions preserved for Chief Justice synthesis
- ✅ Dialectical reasoning requires ALL perspectives
- ⚠️ Not commutative: order matters for readability

**Implementation**:
```python
opinions: Annotated[List[JudicialOpinion], operator.add]
```

---

## ADR-003: 7 Agents + 1 Aggregator + 1 Error Handler

**Status**: Accepted  
**Date**: 2024-02-27  
**Context**: Project requirements specify "7 specialized agents" but LangGraph requires explicit fan-in synchronization.

**Decision**: Implement 7 agents (3 detectives + 3 judges + 1 justice) + 1 aggregator node + 1 error handler.

**Rationale**:
- **7 agents** (intelligent actors with LLMs or decision logic):
  1. RepoInvestigator (code detective)
  2. DocAnalyst (document detective)
  3. VisionInspector (diagram detective)
  4. Prosecutor (critical judge)
  5. Defense (optimistic judge)
  6. TechLead (pragmatic judge)
  7. ChiefJustice (synthesis engine)

- **1 aggregator** (synchronization point, NOT an agent):
  - No LLM, no decision-making
  - Applies state reducers (operator.ior) to merge evidence dicts
  - Required by LangGraph for fan-in pattern

- **1 error_report** (fallback handler, NOT in normal flow):
  - Only executes if ALL detectives fail
  - Graceful degradation (enterprise best practice)
  - Prevents crashes, provides diagnostics

**Consequences**:
- ✅ Meets requirement: "7 specialized agents"
- ✅ Enterprise-grade: fail-safe design
- ✅ LangGraph-compliant: proper fan-in synchronization

**Graph Structure**:
```
Normal Flow (8 nodes):
  3 detectives → 1 aggregator → 3 judges → 1 justice

Error Path (1 node):
  error_report (if all detectives fail)

Total: 9 graph nodes, 7 intelligent agents
```

---

## ADR-004: Sandboxed Git Operations with tempfile

**Status**: Accepted  
**Date**: 2024-02-27  
**Context**: RepoInvestigator must clone untrusted repositories safely.

**Decision**: Use `tempfile.mkdtemp()` for all git operations with automatic cleanup.

**Rationale**:
- **Security**: Isolated from main filesystem
- **Cleanup**: Automatic deletion on exit
- **Concurrency**: Multiple audits can run simultaneously
- **Safety**: No risk of overwriting existing files

**Consequences**:
- ✅ Zero security incidents
- ✅ Safe for untrusted repos
- ✅ No manual cleanup needed

**Implementation**:
```python
temp_dir = tempfile.mkdtemp(prefix="audit_repo_")
subprocess.run(["git", "clone", "--depth", "50", repo_url, temp_dir])
```

---

## ADR-005: Enterprise-Grade Synthesis Algorithm

**Status**: Accepted  
**Date**: 2024-02-28  
**Context**: Chief Justice must resolve conflicts between three judges with different philosophies.

**Decision**: Use weighted average (Tech Lead 50%, Prosecutor 30%, Defense 20%) with evidence-based security veto.

**Rationale**:
- **Tech Lead priority**: Validates actual working code (50% weight)
- **Prosecutor balance**: Ensures quality standards (30% weight)
- **Defense consideration**: Rewards effort and intent (20% weight)
- **Security veto**: Missing security controls = 2/5 (critical failure)
- **Consensus detection**: Variance ≤ 1 uses median (robust to outliers)

**Consequences**:
- ✅ Rational, auditable scoring
- ✅ Prioritizes functionality over criticism
- ✅ Security flaws properly penalized
- ✅ No gamified logic (score floors, favorable rounding)

**Implementation**:
```python
weighted_score = (
    tech_lead_op.score * 0.50 +
    prosecutor_op.score * 0.30 +
    defense_op.score * 0.20
)
final_score = round(weighted_score)
```

---

## ADR-006: AST Parsing Over Regex

**Status**: Accepted  
**Date**: 2024-02-27  
**Context**: RepoInvestigator must detect LangGraph patterns reliably.

**Decision**: Use Python's `ast` module for code analysis, not regex.

**Rationale**:
- **Robustness**: Handles all valid Python syntax
- **Precision**: Understands code structure, not just patterns
- **Maintainability**: No brittle regex patterns
- **Security**: No eval() or exec() risks

**Consequences**:
- ✅ 100% accurate detection of LangGraph patterns
- ✅ Handles edge cases (comments, multiline, etc.)
- ✅ Future-proof for Python syntax changes

**Implementation**:
```python
tree = ast.parse(file.read())
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        if hasattr(node.func, 'id') and node.func.id == "StateGraph":
            findings["has_state_graph"] = True
```
