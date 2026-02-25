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

### Prerequisites

- Python 3.11+
- Git
- API keys (choose one):
  - **Groq** (free, fast) - [Get key](https://console.groq.com/keys)
  - **DeepSeek** (cheap, unlimited) - [Get key](https://platform.deepseek.com/api_keys)
  - OpenAI or Anthropic

### Installation

```bash
# Clone repository
git clone https://github.com/IbnuEyni/10Acweek2
cd 10Acweek2/automaton-auditor

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Run Your First Audit

```bash
# Audit a GitHub repository
python src/main.py \
  --repo-url https://github.com/username/repo \
  --pdf-path path/to/report.pdf \
  --output audit/my_audit.md
```

### Or Use Streamlit UI

```bash
streamlit run app.py
```

Then open http://localhost:8501 and select your LLM provider!

---

## 💡 Features

### 🔬 Forensic Analysis

- **AST Parsing**: Detects LangGraph patterns, Pydantic models, state reducers
- **Git Analysis**: Atomic commit verification, history analysis
- **PDF Analysis**: Concept extraction, keyword density, cross-referencing
- **Vision Analysis**: Diagram classification with Gemini 2.5 Flash

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
