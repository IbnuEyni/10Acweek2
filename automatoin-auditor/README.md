# 🤖 Automaton Auditor

> **Enterprise-grade multi-agent system for autonomous code auditing using LangGraph**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-green.svg)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

Automaton Auditor implements a **"Digital Courtroom"** architecture where autonomous agents conduct forensic code analysis through dialectical reasoning. The system uses parallel execution, state synchronization, and deterministic synthesis to produce comprehensive audit reports.

### ✨ Key Achievements

- ✅ **Multi-Agent Orchestration**: 7 specialized agents with parallel execution
- ✅ **Dialectical Reasoning**: Prosecutor, Defense, and Tech Lead provide adversarial evaluation
- ✅ **Production-Grade**: Type-safe with Pydantic, sandboxed operations, full observability
- ✅ **Multi-LLM Support**: Groq, DeepSeek, OpenAI, Anthropic

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    START AUDIT                          │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│Repo          │ │Doc       │ │Vision        │
│Investigator  │ │Analyst   │ │Inspector     │
│(Git + AST)   │ │(PDF)     │ │(Gemini)      │
└──────┬───────┘ └────┬─────┘ └──────┬───────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │  EVIDENCE AGGREGATOR    │
        └─────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│Prosecutor    │ │Defense   │ │Tech Lead     │
│(Critical)    │ │(Generous)│ │(Pragmatic)   │
└──────┬───────┘ └────┬─────┘ └──────┬───────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   CHIEF JUSTICE         │
        │   (Deterministic)       │
        └─────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │    AUDIT REPORT         │
        └─────────────────────────┘
```

### 🎭 The Digital Courtroom

| Layer             | Agents    | Role                         | Technology               |
| ----------------- | --------- | ---------------------------- | ------------------------ |
| **Detective**     | 3 agents  | Forensic evidence collection | Git, AST, PDF, Vision AI |
| **Judicial**      | 3 judges  | Dialectical evaluation       | Groq/DeepSeek LLMs       |
| **Supreme Court** | 1 justice | Deterministic synthesis      | Python rules             |

---

## 🚀 Quick Start

**⚡ New to the project? See [QUICKSTART.md](QUICKSTART.md) for one-command setup!**

### Runtime Requirements

- **Python**: 3.11.0+ (specified in `.python-version`)
- **Git**: 2.0+
- **Dependencies**: Locked in `requirements.txt` (pip-freeze snapshot)
- **API Keys**: At least one LLM provider (Groq recommended for free tier)

### Installation

```bash
# Clone repository
git clone https://github.com/IbnuEyni/10Acweek2
cd 10Acweek2/automatoin-auditor

# Verify Python version
python3 --version  # Should be 3.11.0 or higher

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install locked dependencies (reproducible builds)
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY from https://console.groq.com/keys
```

### Complete End-to-End Example

**Scenario**: Audit this repository against its own interim report

```bash
# Step 1: Ensure you're in the project directory
cd /path/to/10Acweek2/automatoin-auditor

# Step 2: Activate virtual environment
source venv/bin/activate

# Step 3: Run detective graph against sample repo and PDF
python -m src.main \
  --repo-url https://github.com/IbnuEyni/10Acweek2 \
  --pdf-path reports/interim_report.pdf \
  --output audit/self_audit_example/

# Expected output:
# ✅ Cloning repository...
# ✅ Detective Layer: RepoInvestigator found 8 StateGraph nodes
# ✅ Detective Layer: DocAnalyst found 17 architectural keywords
# ✅ Detective Layer: VisionInspector analyzing diagrams...
# ✅ Judicial Layer: 3 judges evaluating 4 criteria (12 opinions)
# ✅ Chief Justice: Synthesizing final scores...
# ✅ Audit complete: audit/self_audit_example/audit_report.md

# Step 4: View results
cat audit/self_audit_example/audit_report.md

# Step 5: Check LangSmith trace (if LANGSMITH_API_KEY configured)
cat audit/self_audit_example/langsmith_trace_url.txt
```

**Output Structure**:
```
audit/self_audit_example/
├── audit_report.md          # Full markdown report (~15KB)
├── audit_report.json        # Structured JSON data
├── evidence_summary.json    # Detective findings
└── langsmith_trace_url.txt  # Observability link
```

### Alternative: Streamlit UI Example

```bash
# Start web interface
streamlit run app.py

# In browser (http://localhost:8501):
# 1. Select LLM Provider: Groq (free)
# 2. Enter Repo URL: https://github.com/IbnuEyni/10Acweek2
# 3. Upload PDF: reports/interim_report.pdf
# 4. Click "Run Audit"
# 5. View results in real-time with progress indicators
```

---

## 💡 Features

### 🔬 Forensic Analysis

### Advanced AST Analysis

**Structural Property Verification**:
- ✅ Detects `StateGraph` instantiation and compilation
- ✅ Verifies `add_node()`, `add_edge()`, `add_conditional_edges()` usage
- ✅ Counts nodes and edges for parallelism estimation
- ✅ Checks for LangGraph imports and type hints
- ✅ Analyzes function signatures, class inheritance, docstrings
- ✅ Validates Pydantic `BaseModel` usage and `Annotated` types

**Example**: Detecting conditional edges in graph.py
```python
# AST traversal finds:
findings = {
    "has_conditional_edges": True,
    "has_compile": True,
    "edge_count": 10,
    "node_names": ["repo_investigator", "doc_analyst", ...]
}
```

### Semantic PDF Chunking

**Queryable Document Access**:
- ✅ Splits large PDFs into overlapping chunks (2000 chars, 200 overlap)
- ✅ Sentence-boundary detection for clean breaks
- ✅ Keyword-based search with relevance scoring
- ✅ Returns top-N most relevant chunks for targeted analysis
- ✅ Ready for embedding-based semantic search

**Example**: Querying PDF for specific concepts
```python
# Instead of loading entire 20-page PDF:
chunks = query_chunks(pdf_text, "StateGraph architecture", max_chunks=3)
# Returns only relevant sections with context
```

### Git Analysis
- **Atomic commit verification**: Detects monolithic vs incremental commits
- **History analysis**: Extracts commit messages, timestamps, patterns
- **URL validation**: Regex-based GitHub URL verification
- **Edge case handling**: Empty repos, auth failures, timeouts

### Vision Analysis
- **Diagram classification**: StateGraph vs generic flowchart detection
- **Flow analysis**: Fan-out/fan-in pattern recognition with Gemini 2.5 Flash
- **Node identification**: Extracts component names from diagrams

### ⚖️ Dialectical Reasoning

- **Prosecutor**: Critical lens (security-focused, harsh scoring)
- **Defense**: Optimistic lens (effort-focused, generous scoring)
- **Tech Lead**: Pragmatic lens (functionality-focused, realistic scoring)

### 🧠 Deterministic Synthesis

- **Security Override**: Security flaws cap score at 3
- **Fact Supremacy**: Tech Lead overrides when score ≤ 2
- **Weighted Resolution**: Tech Lead 50%, Prosecutor 30%, Defense 20%

### 🔒 Production-Grade

- ✅ **Type Safety**: 100% Pydantic validation
- ✅ **Sandboxing**: Isolated git operations with tempfile
- ✅ **Parallel Safety**: State reducers (operator.add, operator.ior)
- ✅ **Observability**: Full LangSmith tracing
- ✅ **Error Handling**: Graceful degradation, retry logic

---

## 📊 Performance

| Metric                 | Value                          |
| ---------------------- | ------------------------------ |
| **Audit Duration**     | ~45 seconds                    |
| **Evidence Collected** | 7 categories                   |
| **Judicial Opinions**  | 12 (3 judges × 4 criteria)     |
| **Parallel Speedup**   | 2.5x vs sequential             |
| **Cost (DeepSeek)**    | $0.02 per audit                |
| **Cost (Groq)**        | $0 (free tier, 3-4 audits/day) |

---

## 📦 Dependency Management

### Locked Dependencies

**File**: `requirements.txt` (pip-freeze snapshot)
- ✅ All dependencies pinned to exact versions
- ✅ Includes transitive dependencies
- ✅ Reproducible builds across environments
- ✅ Generated from working production environment

**Key Dependencies**:
```
langgraph==0.2.59        # StateGraph orchestration
langchain==0.3.18        # LLM framework
pydantic==2.10.6         # Type-safe state models
streamlit==1.41.1        # Web UI
groq==0.13.1             # Groq LLM provider
google-generativeai==0.8.3  # Gemini vision
```

### Python Version

**File**: `.python-version`
```
3.11.0
```

**Why Python 3.11+**:
- ✅ Native `TypedDict` with `Annotated` support
- ✅ Better error messages for type hints
- ✅ Performance improvements (10-60% faster than 3.10)
- ✅ `tomllib` for pyproject.toml parsing

### Reproducible Setup

```bash
# Exact environment recreation
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Verify installation
python -c "import langgraph; print(langgraph.__version__)"  # 0.2.59
```

---

## 🛠️ Technology Stack

### Core Framework

- **LangGraph**: StateGraph with parallel execution
- **Pydantic**: Type-safe state management
- **Python 3.11+**: Modern async/await patterns

### LLM Providers

- **Groq**: Llama 3.3 70B (free, fast)
- **DeepSeek**: DeepSeek V3 (cheap, unlimited)
- **OpenAI**: GPT-4o (premium)
- **Anthropic**: Claude 3.5 Sonnet (advanced)

### Analysis Tools

- **AST**: Python ast module for code analysis
- **Git**: Subprocess with sandboxing
- **PDF**: PyPDF2 for document parsing
- **Vision**: Google Gemini 2.5 Flash

---

## 📁 Project Structure

```
automaton-auditor/
├── src/
│   ├── state.py              # Pydantic state models with reducers
│   ├── graph.py              # LangGraph orchestration (fan-out/fan-in)
│   ├── main.py               # CLI entry point
│   ├── nodes/
│   │   ├── detectives.py     # RepoInvestigator, DocAnalyst, VisionInspector
│   │   ├── judges.py         # Prosecutor, Defense, TechLead
│   │   ├── justice.py        # ChiefJustice (deterministic synthesis)
│   │   └── aggregator.py     # Evidence aggregation (fan-in)
│   ├── tools/
│   │   ├── git_tools.py      # Sandboxed git operations
│   │   ├── ast_tools.py      # AST-based code analysis
│   │   ├── pdf_tools.py      # PDF parsing and concept extraction
│   │   └── vision_tools.py   # Gemini vision analysis
│   └── utils/
│       ├── config.py         # Configuration management
│       ├── llm_factory.py    # Multi-provider LLM factory
│       ├── prompts.py        # Judge persona prompts
│       └── rubric_loader.py  # Rubric JSON parser
├── rubric/
│   └── week2_rubric.json     # Evaluation criteria
├── reports/
│   ├── interim_report.md     # Source markdown
│   ├── interim_report.pdf    # Final PDF (17 pages, 664KB)
│   └── architecture_diagram.png
├── audit/                    # Generated audit reports
├── tests/                    # Unit and integration tests
├── app.py                    # Streamlit web UI
├── ARCHITECTURE.md           # System architecture details
├── SECURITY.md               # Security measures documentation
└── README.md                 # This file
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
python test_integration.py

# View test coverage
pytest --cov=src tests/
```

### Test Results

- ✅ Phase 1 Validation: PASS
- ✅ Phase 2 Detective: PASS
- ✅ Phase 3 Judicial: PASS
- ✅ Integration Tests: PASS (6/6 checks)
- ✅ Vision Setup: PASS

---

## 📖 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System design, state flow, execution patterns
- **[SECURITY.md](SECURITY.md)**: Security measures, sandboxing, threat model
- **[reports/interim_report.pdf](reports/interim_report.pdf)**: Comprehensive project report (17 pages)

---

## 🎓 Key Concepts

### Multi-Agent Principles

1. **Agent Autonomy**: Each agent operates independently
2. **Parallel Execution**: Fan-out/fan-in architecture
3. **State Synchronization**: CRDTs with reducers
4. **Dialectical Reasoning**: Adversarial collaboration
5. **Hierarchical Decision Making**: Deterministic synthesis

### Architectural Patterns

- **StateGraph Orchestration**: Declarative workflow with LangGraph
- **Fan-Out Pattern**: 1 → N parallel execution
- **Fan-In Pattern**: N → 1 synchronization
- **State Reducers**: Conflict-free replicated data types
- **Sandboxed Execution**: Isolated operations with tempfile

---

## 🤝 Contributing

This is a submission for the FDE Challenge Week 2. For questions or feedback, please open an issue.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Amir Ahmedin**

- GitHub: [@IbnuEyni](https://github.com/IbnuEyni)
- Project: FDE Challenge Week 2

---

## 🙏 Acknowledgments

- **LangChain/LangGraph**: For the amazing orchestration framework
- **Groq**: For free, fast LLM inference
- **DeepSeek**: For affordable, unlimited LLM access
- **Google**: For Gemini vision capabilities

---

**⭐ Star this repo if you find it useful!**
