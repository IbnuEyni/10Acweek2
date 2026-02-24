# Quick Reference Guide

## Setup (First Time)

```bash
# 1. Install dependencies
bash setup.sh

# 2. Configure API keys
cp .env.example .env
nano .env  # Add your keys

# 3. Validate
python3 validate_phase1.py
```

## Project Structure

```
src/
├── state.py           # Data models (Evidence, JudicialOpinion, AgentState)
├── graph.py           # [Phase 2] LangGraph orchestration
├── nodes/
│   ├── detectives.py  # [Phase 2] RepoInvestigator, DocAnalyst, VisionInspector
│   ├── judges.py      # [Phase 3] Prosecutor, Defense, TechLead
│   └── justice.py     # [Phase 4] ChiefJustice synthesis
├── tools/
│   ├── git_tools.py   # [Phase 2] Safe git operations
│   ├── ast_tools.py   # [Phase 2] AST parsing
│   ├── pdf_tools.py   # [Phase 2] PDF parsing
│   └── vision_tools.py # [Phase 2] Image analysis
└── utils/
    ├── config.py      # ✅ Environment management
    └── rubric_loader.py # ✅ Rubric parsing
```

## Key Files

| File | Purpose | Status |
|------|---------|--------|
| `src/state.py` | Pydantic models + state reducers | ✅ Complete |
| `src/utils/config.py` | API keys, paths, safety limits | ✅ Complete |
| `src/utils/rubric_loader.py` | Parse rubric JSON | ✅ Complete |
| `rubric/week2_rubric.json` | Evaluation constitution | ✅ Complete |
| `tests/test_state.py` | State model tests | ✅ Complete |
| `tests/test_rubric_loader.py` | Rubric loader tests | ✅ Complete |

## Common Commands

```bash
# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_state.py::test_evidence_model -v

# Validate Phase 1
python3 validate_phase1.py

# Check imports
python3 -c "from src.state import Evidence; print('✅ OK')"

# Load rubric
python3 -c "from src.utils.rubric_loader import load_rubric; print(load_rubric())"
```

## State Models Cheat Sheet

### Evidence
```python
from src.state import Evidence

evidence = Evidence(
    goal="Verify StateGraph exists",
    found=True,
    content="class StateGraph...",
    location="src/graph.py:10",
    rationale="AST parsing confirmed",
    confidence=0.95
)
```

### JudicialOpinion
```python
from src.state import JudicialOpinion

opinion = JudicialOpinion(
    judge="Prosecutor",  # or "Defense", "TechLead"
    criterion_id="forensic_accuracy_code",
    score=3,  # 1-5
    argument="Code exists but lacks error handling",
    cited_evidence=["src/tools/git_tools.py:25"]
)
```

### AgentState
```python
from src.state import AgentState

state: AgentState = {
    "repo_url": "https://github.com/user/repo",
    "pdf_path": "/path/to/report.pdf",
    "rubric_dimensions": [],
    "evidences": {},      # Dict[str, List[Evidence]]
    "opinions": [],       # List[JudicialOpinion]
    "final_report": "",
    "errors": []
}
```

## Rubric Access

```python
from src.utils.rubric_loader import (
    load_rubric,
    get_rubric_dimensions,
    get_synthesis_rules,
    filter_dimensions_by_artifact
)

# Get all dimensions
dimensions = get_rubric_dimensions()

# Filter by artifact type
repo_dims = filter_dimensions_by_artifact("github_repo")
pdf_dims = filter_dimensions_by_artifact("pdf_report")

# Get synthesis rules for Chief Justice
rules = get_synthesis_rules()
```

## Configuration Access

```python
from src.utils.config import Config

# Paths
print(Config.PROJECT_ROOT)
print(Config.RUBRIC_PATH)
print(Config.AUDIT_OUTPUT_DIR)

# Model settings
print(Config.DEFAULT_LLM_MODEL)
print(Config.DEFAULT_TEMPERATURE)

# Safety limits
print(Config.GIT_CLONE_TIMEOUT)
print(Config.MAX_FILE_SIZE_MB)
```

## Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
LANGSMITH_API_KEY=lsv2_...

# Optional
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM_MODEL=gpt-4o
DEFAULT_TEMPERATURE=0.0
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=automaton-auditor
```

## Troubleshooting

### Import Errors
```bash
# Upgrade typing-extensions
python3 -m pip install --upgrade typing-extensions pydantic

# Reinstall dependencies
bash setup.sh
```

### Missing .env
```bash
cp .env.example .env
# Then edit .env with your keys
```

### Test Failures
```bash
# Run with verbose output
pytest tests/ -v -s

# Run single test
pytest tests/test_state.py -v
```

## Next Steps (Phase 2)

1. Implement `src/tools/git_tools.py`
   - `safe_clone_repo(url) -> Path`
   - `extract_git_history(path) -> List[Dict]`

2. Implement `src/tools/ast_tools.py`
   - `detect_langgraph_patterns(file) -> Dict`
   - `find_pydantic_models(file) -> List[str]`

3. Implement `src/tools/pdf_tools.py`
   - `parse_pdf(path) -> str`
   - `extract_concepts(text) -> List[str]`

4. Implement `src/nodes/detectives.py`
   - `repo_investigator_node(state) -> state`
   - `doc_analyst_node(state) -> state`
   - `vision_inspector_node(state) -> state`

## Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [LangSmith](https://smith.langchain.com/)

---

**Phase 1 Status**: ✅ COMPLETE
**Ready for**: Phase 2 - Detective Layer
