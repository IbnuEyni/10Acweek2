# Quickstart Guide - Automaton Auditor

**One-command setup from clone to running audits.**

## Prerequisites

- Python 3.11+
- Git
- 5 minutes

## Setup (One-Time)

```bash
# 1. Clone repository
git clone https://github.com/IbnuEyni/10Acweek2.git
cd 10Acweek2/automatoin-auditor

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies (locked versions)
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your keys:
# - GROQ_API_KEY (get free at https://console.groq.com/keys)
# - GOOGLE_API_KEY (optional, for vision: https://aistudio.google.com/app/apikey)
# - DEEPSEEK_API_KEY (optional, alternative LLM)
```

## Run Audit (30 seconds)

```bash
# Option 1: CLI
python -m src.main \
  --repo-url https://github.com/user/repo \
  --pdf-path reports/interim_report.pdf \
  --output audit/report_generated/

# Option 2: Streamlit UI (recommended)
streamlit run app.py
# Then: Enter repo URL + PDF path in browser
```

## Verify Installation

```bash
# Run integration tests
python tests/integration/test_integration.py

# Expected output: ✅ All 6 checks passed
```

## Troubleshooting

**Error: "No module named 'langgraph'"**
```bash
pip install -r requirements.txt
```

**Error: "GROQ_API_KEY not found"**
```bash
# Get free key: https://console.groq.com/keys
# Add to .env: GROQ_API_KEY=gsk_...
```

**Error: "Repository not found"**
```bash
# Ensure repo URL is public and correct format:
# ✅ https://github.com/user/repo
# ❌ github.com/user/repo (missing https://)
```

## What Gets Audited?

1. **Code Analysis** (RepoInvestigator)
   - StateGraph usage
   - Pydantic models
   - State reducers
   - Git history

2. **Document Analysis** (DocAnalyst)
   - PDF parsing
   - Architectural keywords
   - Theoretical concepts

3. **Visual Analysis** (VisionInspector, optional)
   - Architecture diagrams
   - Flow detection

4. **Judicial Evaluation** (3 judges)
   - Prosecutor (critical)
   - Defense (generous)
   - Tech Lead (pragmatic)

5. **Final Report** (Chief Justice)
   - Synthesized scores
   - Detailed feedback
   - Evidence citations

## Output

```
audit/report_generated/
├── audit_report.md          # Full markdown report
├── audit_report.json        # Structured data
└── langsmith_trace_url.txt  # Observability link
```

## Next Steps

- Read [README.md](README.md) for architecture details
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical deep-dive
- Read [SECURITY.md](SECURITY.md) for sandboxing details
- Customize rubric in `rubric/week2_rubric.json`

## Support

- Issues: https://github.com/IbnuEyni/10Acweek2/issues
- Documentation: See README.md
