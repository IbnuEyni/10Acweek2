# Automaton Auditor

Enterprise-grade multi-agent system for autonomous code auditing using LangGraph.

## Architecture

```
Detective Layer (Parallel) → Evidence Aggregation → Judicial Layer (Parallel) → Chief Justice → Report
```

### Layers
1. **Detective Layer**: RepoInvestigator, DocAnalyst, VisionInspector (forensic evidence collection)
2. **Judicial Layer**: Prosecutor, Defense, TechLead (dialectical analysis)
3. **Supreme Court**: ChiefJustice (deterministic synthesis)

## Setup

### Prerequisites
- Python 3.11+
- Git
- API keys for OpenAI or Anthropic
- LangSmith account (for observability)

### Installation

```bash
# Install uv package manager (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required variables:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- `LANGSMITH_API_KEY`

## Usage

```bash
# Run audit on a repository
python -m src.main \
  --repo-url https://github.com/username/repo \
  --pdf-path path/to/report.pdf \
  --output audit/report_onpeer_generated/
```

## Project Structure

```
automaton-auditor/
├── src/
│   ├── state.py              # Pydantic state models
│   ├── graph.py              # LangGraph orchestration
│   ├── nodes/                # Detective, Judge, Justice nodes
│   ├── tools/                # Git, AST, PDF tools
│   └── utils/                # Config, rubric loader
├── rubric/
│   └── week2_rubric.json     # Machine-readable constitution
├── audit/                    # Output directory
└── tests/                    # Unit and integration tests
```

## Development

```bash
# Run tests
pytest tests/

# View LangSmith traces
# Visit https://smith.langchain.com/
```

## Key Features

- **Type Safety**: 100% Pydantic validation with state reducers
- **Parallel Execution**: Fan-out/fan-in architecture for speed
- **Security**: Sandboxed git operations, no shell injection
- **Observability**: Full LangSmith tracing
- **Deterministic**: Chief Justice uses hardcoded rules, not LLM synthesis
